"""Configuration models for LLM Reliability Engine."""

from pydantic import BaseModel, Field


class ReliabilityConfig(BaseModel):
    """Controls retry, repair, prompt, and failure behavior for the engine.

    Defaults are production-sensible for V1. Override individual fields when
    constructing ``ReliabilityEngine``.
    """

    max_retries: int = Field(
        default=3,
        ge=0,
        description="Maximum number of LLM repair retries after the initial attempt.",
    )
    include_schema_in_prompt: bool = Field(
        default=True,
        description="When True, inject the Pydantic JSON schema into the prompt.",
    )
    enable_deterministic_repair: bool = Field(
        default=True,
        description=(
            "When True, attempt syntax repair with json-repair before LLM retry."
        ),
    )
    enable_llm_repair: bool = Field(
        default=True,
        description=(
            "When True, send repair prompts to the LLM on parse/validation failure."
        ),
    )
    retry_on_validation_failure: bool = Field(
        default=True,
        description=(
            "When True, retry with a repair prompt after Pydantic validation errors."
        ),
    )
    retry_backoff_seconds: float = Field(
        default=0.5,
        ge=0,
        description="Base delay in seconds between retries (exponential backoff).",
    )
    include_raw_response: bool = Field(
        default=True,
        description="When True, attach the last raw LLM response to the result.",
    )
    raise_on_failure: bool = Field(
        default=True,
        description=(
            "When True, raise ReliabilityExhaustedError after all retries fail; "
            "when False, return a StructuredResult with success=False."
        ),
    )
    repair_prompt_template: str | None = Field(
        default=None,
        description="Optional override for the default LLM repair prompt template.",
    )
    system_prompt: str | None = Field(
        default=None,
        description="Optional system-level instruction prepended to prompts.",
    )
