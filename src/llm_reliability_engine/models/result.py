"""Result and metadata models for LLM Reliability Engine."""

from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

ParseMethod = Literal[
    "direct",
    "extracted",
    "deterministic_repair",
    "llm_repair",
]

T = TypeVar("T")


class ReliabilityMetadata(BaseModel):
    """Diagnostic information about a single ``generate()`` run.

    This is the shared source of truth for both successful results and
    exhausted failures (attached to ``ReliabilityExhaustedError`` later).
    """

    success: bool = Field(
        description="Whether a validated schema instance was produced.",
    )
    attempts: int = Field(
        ge=0,
        description="Total LLM invocations made during this run.",
    )
    total_latency_ms: float = Field(
        ge=0,
        description="Wall-clock time for the full generate() call, in milliseconds.",
    )
    llm_latency_ms: float = Field(
        ge=0,
        description="Sum of time spent waiting on LLM calls, in milliseconds.",
    )
    validation_passed: bool = Field(
        description="Whether the final attempt passed Pydantic validation.",
    )
    parse_method: ParseMethod | None = Field(
        default=None,
        description=(
            "How JSON was obtained on the successful (or last) attempt: "
            "direct, extracted, deterministic_repair, or llm_repair."
        ),
    )
    repair_strategies_used: list[str] = Field(
        default_factory=list,
        description="Ordered list of repair strategies applied during the run.",
    )
    validation_errors: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Structured field errors from the last failed validation, if any.",
    )
    retry_reasons: list[str] = Field(
        default_factory=list,
        description="Why each retry was triggered (e.g. json_parse_error).",
    )


class StructuredResult(BaseModel, Generic[T]):
    """Primary return type from ``ReliabilityEngine.generate()``.

    On success, ``data`` is a validated schema instance. On failure with
    ``raise_on_failure=False``, ``data`` is ``None`` and ``metadata.success``
    is ``False``.
    """

    data: T | None = Field(
        default=None,
        description="Validated Pydantic model instance, or None on failure.",
    )
    metadata: ReliabilityMetadata = Field(
        description="Attempt, latency, repair, and validation diagnostics.",
    )
    raw_response: str | None = Field(
        default=None,
        description="Last raw LLM text, when include_raw_response is enabled.",
    )
