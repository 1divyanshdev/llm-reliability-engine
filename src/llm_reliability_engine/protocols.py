"""Provider protocols for LLM Reliability Engine."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """Async contract for sending a prompt to an LLM and receiving raw text.

    Any async callable with the signature ``(prompt: str) -> str`` satisfies
    this protocol — plain functions, lambdas, or classes implementing
    ``__call__``. The engine does not depend on any specific LLM SDK.
    """

    async def __call__(self, prompt: str) -> str:
        """Send a prompt to the LLM and return the unparsed text response.

        Args:
            prompt: The full prompt string to send to the LLM.

        Returns:
            The raw text response from the LLM, before extraction or validation.
        """
        ...
