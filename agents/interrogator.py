import json
import os

from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"


def get_groq_client() -> Groq:
    """
    Create a Groq client using the GROQ_API_KEY
    environment variable.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(api_key=api_key)


def build_investigation_prompt(
    exception: dict,
) -> str:
    """
    Build a structured investigation prompt
    for the Groq model.
    """

    return f"""
You are the Interrogator Agent in CloseLoop,
an autonomous month-end finance reconciliation system.

Your job is to investigate a financial reconciliation
exception using ONLY the evidence provided below.

Do not invent transactions, documents, policies,
people, dates, or explanations that are not supported
by the evidence.

Exception evidence:

{json.dumps(exception, indent=2, default=str)}

Analyze the exception and return a concise investigation.

Your response MUST be valid JSON with exactly these fields:

{{
    "issue_type": "...",
    "finding": "...",
    "likely_cause": "...",
    "recommended_action": "...",
    "risk_level": "low|medium|high",
    "requires_human_review": true
}}

Guidelines:

- Explain what the evidence shows.
- If the evidence is insufficient to determine the cause,
  explicitly say so.
- Do not claim that an action was completed.
- Recommended actions should be practical finance
  operations actions.
- High-risk or uncertain cases should require human review.
"""


def investigate_exception(
    exception: dict,
) -> dict:
    """
    Send one reconciliation exception to Groq
    for investigation.
    """

    client = get_groq_client()

    prompt = build_investigation_prompt(
        exception
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful financial "
                    "operations investigation agent."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
        max_tokens=800,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "issue_type": exception.get(
                "match_status",
                "unknown",
            ),
            "finding": content,
            "likely_cause": (
                "The model returned a non-JSON "
                "investigation response."
            ),
            "recommended_action": (
                "Review the exception manually."
            ),
            "risk_level": "medium",
            "requires_human_review": True,
        }


def select_exceptions(
    reconciliation_results,
) -> list[dict]:
    """
    Select reconciliation results that require
    investigation.
    """

    if reconciliation_results is None:
        return []

    exceptions = []

    for _, row in reconciliation_results.iterrows():

        status = row.get(
            "match_status",
            "",
        )

        if status not in [
            "matched",
            "matched_by_vendor_amount",
        ]:

            exceptions.append(
                {
                    "bank_transaction_id": row.get(
                        "bank_transaction_id"
                    ),
                    "accounting_transaction_id": row.get(
                        "accounting_transaction_id"
                    ),
                    "match_status": status,
                    "bank_amount": row.get(
                        "bank_amount"
                    ),
                    "accounting_amount": row.get(
                        "accounting_amount"
                    ),
                    "difference": row.get(
                        "difference"
                    ),
                    "vendor": row.get(
                        "vendor"
                    ),
                    "reference": row.get(
                        "reference"
                    ),
                    "reconciliation_explanation": row.get(
                        "explanation"
                    ),
                }
            )

    return exceptions


def run_interrogator(
    reconciliation_results,
) -> list[dict]:
    """
    Investigate all reconciliation exceptions.
    """

    exceptions = select_exceptions(
        reconciliation_results
    )

    investigations = []

    for exception in exceptions:

        investigation = investigate_exception(
            exception
        )

        investigation["exception"] = exception

        investigations.append(
            investigation
        )

    return investigations
