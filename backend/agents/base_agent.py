# backend/agents/base_agent.py
import os
import json
from abc import ABC, abstractmethod
from typing import Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"


class BaseAgent(ABC):
    name: str
    department: str
    description: str

    @property
    @abstractmethod
    def system_prompt(self) -> str: ...

    @property
    @abstractmethod
    def tools(self) -> list[dict]: ...

    def dispatch_tool(self, tool_name: str, tool_input: dict) -> Any:
        raise NotImplementedError(f"Tool {tool_name} not implemented in {self.name}")

    def _tools_as_prompt(self) -> str:
        lines = [
            "You have access to these tools.",
            "To call a tool respond ONLY with valid JSON — no markdown, no explanation, no extra text:",
            '{"tool": "<name>", "input": {<args>}}',
            "When you have enough info to give a final answer, respond with plain text only (not JSON).",
            "\nAvailable tools:",
        ]
        for t in self.tools:
            props = list(t["input_schema"].get("properties", {}).keys())
            lines.append(f"- {t['name']}({', '.join(props)}): {t['description']}")
        return "\n".join(lines)

    def run(self, task: str) -> dict:
        system = f"{self.system_prompt}\n\n{self._tools_as_prompt()}"
        messages = [{"role": "user", "content": task}]
        steps = []
        final_response = ""

        for _ in range(8):  # max 8 tool call iterations
            response = client.chat.completions.create(
                model=MODEL,
                max_tokens=1024,
                messages=[{"role": "system", "content": system}] + messages,
            )

            content = response.choices[0].message.content.strip()

            # Strip markdown fences if model wraps JSON anyway
            clean = content.strip("` \n")
            if clean.startswith("json"):
                clean = clean[4:].strip()

            try:
                parsed = json.loads(clean)
                if "tool" in parsed and "input" in parsed:
                    tool_name = parsed["tool"]
                    tool_input = parsed["input"]
                    result = self.dispatch_tool(tool_name, tool_input)
                    steps.append(
                        {
                            "tool": tool_name,
                            "input": tool_input,
                            "output": result,
                        }
                    )
                    messages.append({"role": "assistant", "content": content})
                    messages.append(
                        {
                            "role": "user",
                            "content": f"Tool result for {tool_name}: {json.dumps(result)}\n\nContinue.",
                        }
                    )
                    continue
            except (json.JSONDecodeError, KeyError):
                pass

            # Not JSON — final answer
            final_response = content
            break

        return {
            "agent": self.name,
            "department": self.department,
            "task": task,
            "steps": steps,
            "response": final_response,
        }
