"""
Agent 4: Legal Intelligence LLM
LLM prompt templates for obligation extraction.
"""

# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

EXTRACT_OBLIGATIONS_PROMPT = """You are a regulatory compliance AI assistant analyzing banking and financial regulations.

INPUT TEXT:
{regulatory_text}

SOURCE: {source_name}
CHANGE TYPE: {change_type}

TASK:
Extract all specific obligations, requirements, or mandates from the above text.

OUTPUT FORMAT (strict JSON):
{{
  "obligations": [
    {{
      "text": "exact quote from source showing the obligation",
      "summary": "concise 1-sentence summary of what must be done",
      "type": "disclosure|KYC|capital|reporting|conduct|licensing|sanctions|other",
      "affected_entities": ["Commercial Banks", "NBFCs", "Payment Banks", etc.],
      "deadline": "YYYY-MM-DD or 'not specified' or 'ongoing'",
      "confidence": 0.0-1.0
    }}
  ]
}}

RULES:
- Only extract explicit obligations (keywords: must, shall, required, mandatory, obligated, needs to)
- Include exact quotes from source text
- If unsure about any field, set confidence < 0.7
- Return empty array if no obligations found
- Focus on actionable requirements, not background information
"""

CLASSIFY_SEVERITY_PROMPT = """Rate the severity of this regulatory obligation:

OBLIGATION:
{obligation_text}

CONTEXT:
- Deadline: {deadline}
- Entities Affected: {entities}
- Type: {obligation_type}

OUTPUT (JSON):
{{
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "reasoning": "brief explanation",
  "confidence": 0.0-1.0
}}

SEVERITY GUIDELINES:
- CRITICAL: High penalties, wide scope, tight deadline, new requirement
- HIGH: Moderate penalties, significant operational impact
- MEDIUM: Standard compliance updates, reasonable timeline
- LOW: Minor procedural changes, informational
"""

GENERATE_ACTION_ITEMS_PROMPT = """You are a compliance officer creating an action plan.

OBLIGATION:
{obligation_text}

DEADLINE: {deadline}
AFFECTED: {entities}

Generate 3-5 specific, actionable tasks to ensure compliance.

OUTPUT (JSON):
{{
  "action_items": [
    "specific actionable task 1",
    "specific actionable task 2",
    ...
  ],
  "estimated_effort_hours": number,
  "departments_involved": ["Compliance", "IT", "Operations", etc.]
}}

Make tasks concrete and measurable.
"""

DETECT_AMBIGUITIES_PROMPT = """Analyze this regulatory text for ambiguities or unclear requirements:

TEXT:
{text}

OUTPUT (JSON):
{{
  "ambiguities": [
    {{
      "issue": "description of ambiguity",
      "location": "quote showing unclear part",
      "severity": "HIGH|MEDIUM|LOW"
    }}
  ],
  "requires_clarification": true/false,
  "confidence": 0.0-1.0
}}

Look for:
- Vague terms ("reasonable", "appropriate", "sufficient")
- Missing deadlines
- Unclear scope
- Contradictory statements
"""

MAP_TO_POLICY_PROMPT = """Map this regulatory obligation to relevant internal policy:

OBLIGATION:
{obligation_summary}
TYPE: {obligation_type}

INTERNAL POLICIES:
{policy_list}

OUTPUT (JSON):
{{
  "mapped_policy": "policy name or null",
  "relevance": "HIGH|MEDIUM|LOW|NONE",
  "requires_policy_update": true/false,
  "suggested_changes": "brief description if update needed",
  "confidence": 0.0-1.0
}}
"""
