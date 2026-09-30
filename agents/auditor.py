import json
import os

from groq import Groq

from tools.audit_tools import (
    build_audit_summary,
)


MODEL_NAME = "openai/gpt-oss-20b"


def get_groq_client() -> Groq:
    """
    Create a Groq client using the
    GROQ_API_KEY environment variable.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(api_key=api_key)


def build_audit_prompt(
    audit_summary: dict,
    reconciliation_summary: dict,
    investigations: list[dict],
) -> str:
    """
    Build the prompt used by the Auditor LLM.
    """

    return f"""
You are the Auditor Agent in CloseLoop,
an autonomous month-end finance closing system.

Your job is to review the results of the
financial reconciliation and investigation process.

Use ONLY the evidence provided below.

Do not invent transactions, policies,
documents, people, or financial facts.

AUDIT SUMMARY:
{json.dumps(audit_summary, indent=2, default=str)}

RECONCILIATION SUMMARY:
{json.dumps(reconciliation_summary, indent=2, default=str)}

INVESTIGATIONS:
{json.dumps(investigations, indent=2, default=str)}

Return a concise audit assessment.

Your response MUST be valid JSON with exactly
these fields:

{{
    "overall_assessment": "...",
    "key_findings": [
        "...",
        "..."
    ],
    "control_concerns": [
        "...",
        "..."
    ],
    "recommended_next_steps": [
        "...",
        "..."
    ],
    "human_approval_required": true
}}

Rules:

- Base every finding on the supplied evidence.
- Do not claim that an issue has been resolved
  unless the evidence explicitly says so.
- If exceptions remain unresolved, clearly state this.
- If human review is needed, explain why.
- Do not invent compliance requirements.
"""


def generate_audit_assessment(
    audit_summary: dict,
    reconciliation_summary: dict,
    investigations: list[dict],
) -> dict:
    """
    Ask Groq to generate an audit assessment.
    """

    client = get_groq_client()

    prompt = build_audit_prompt(
        audit_summary,
        reconciliation_summary,
        investigations,
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful financial "
                    "audit review agent."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
        max_tokens=1000,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)

    except json.JSONDecodeError:

        return {
            "overall_assessment": content,
            "key_findings": [],
            "control_concerns": [
                "The model returned a non-JSON response."
            ],
            "recommended_next_steps": [
                "Review the audit output manually."
            ],
            "human_approval_required": True,
        }


def run_auditor(
    ingestion_result: dict,
    reconciliation_result: dict,
    investigations: list[dict],
) -> dict:
    """
    Run the complete audit process.
    """

    reconciliation_summary = (
        reconciliation_result.get(
            "summary",
            {},
        )
        if reconciliation_result
        else {}
    )

    audit_summary = build_audit_summary(
        ingestion_result,
        reconciliation_result,
        investigations,
    )

    assessment = generate_audit_assessment(
        audit_summary,
        reconciliation_summary,
        investigations,
    )

    return {
        "audit_summary": audit_summary,
        "assessment": assessment,
    }
