import os
import json
from groq import Groq
from core.registry import SkillRegistry


class JarvisEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = "llama-3.3-70b-versatile"

        self.system_instruction = (
            "You are Jarvis, a helpful AI assistant. "
            "Use tools ONLY when necessary. "
            "Never invent placeholder values. "
            "If required information is missing, ask the user clearly."
        )

        self.INVALID_PLACEHOLDERS = {
            "user_provided_location",
            "user_location",
            "your_location",
            "location_here",
            "unknown",
            "null",
            ""
        }

    # =====================================================
    def run_conversation(self, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": self.system_instruction},
            {"role": "user", "content": user_prompt}
        ]

        try:
            tools_schema = self.registry.get_tools_schema()

            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 250
            }

            if tools_schema:
                kwargs["tools"] = tools_schema
                kwargs["tool_choice"] = "auto"

            response = self.client.chat.completions.create(**kwargs)

        except Exception:
            return "I am having trouble connecting to the brain, sir."

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # =====================================================
        # TOOL EXECUTION
        if tool_calls:
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.registry.get_function(function_name)

                if not function_to_call:
                    return "I tried to use a tool, but it was unavailable."

                try:
                    args = json.loads(tool_call.function.arguments or "{}")

                    # 🛑 SANITIZE PLACEHOLDERS
                    for key, value in list(args.items()):
                        if (
                            isinstance(value, str)
                            and value.lower() in self.INVALID_PLACEHOLDERS
                        ):
                            args[key] = None

                    # 🌍 WEATHER FALLBACK LOGIC
                    if function_name == "get_weather":
                        if not args.get("city") and not args.get("pincode"):
                            default_city = os.environ.get("DEFAULT_CITY")
                            if default_city:
                                args["city"] = default_city
                            else:
                                return "Which city would you like the weather for?"

                    result = function_to_call(**args)

                except Exception:
                    return "I encountered an error while executing the request."

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(result)
                })

            # =====================================================
            # FINAL RESPONSE (NO TOOLS, NO JSON)
            final_response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=200
            )

            return final_response.choices[0].message.content

        # =====================================================
        # NORMAL CHAT RESPONSE
        return response_message.content