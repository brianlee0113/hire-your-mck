"""Base agent class for the multi-agent pipeline."""
from src.api_client import call_claude, parse_json_response, MODEL, MODEL_OPUS, MODEL_HAIKU


class BaseAgent:
    """Base class for all pipeline agents.

    Subclasses set name, model, system_prompt, and max_tokens.
    """

    name = "base"
    model = MODEL
    system_prompt = ""
    max_tokens = 4096

    def run(self, user_message):
        """Call Claude API with this agent's prompt and parse JSON response.

        Args:
            user_message: The user message to send

        Returns:
            dict or list: Parsed JSON response
        """
        text = call_claude(
            self.system_prompt,
            user_message,
            max_tokens=self.max_tokens,
            model=self.model,
        )
        return parse_json_response(text)

    def run_raw(self, user_message):
        """Call Claude API and return raw text (no JSON parsing).

        Args:
            user_message: The user message to send

        Returns:
            str: Raw response text
        """
        return call_claude(
            self.system_prompt,
            user_message,
            max_tokens=self.max_tokens,
            model=self.model,
        )
