from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
)


@input_guardrail(run_in_parallel=False)
async def hr_domain_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:

    user_query = (input if isinstance(input, str) else str(input)).lower()

    allowed_keywords = [
        "leave",
        "absence",
        "time off",
        "employee",
        "hr",
        "balance",
        "application",
        "pending",
        "approve",
        "reject",
    ]

    is_hr_related = any(keyword in user_query for keyword in allowed_keywords)

    return GuardrailFunctionOutput(
        output_info="HR domain validation",
        tripwire_triggered=not is_hr_related,
    )
