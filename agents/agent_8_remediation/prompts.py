"""
Agent 8: Remediation Planner
LLM prompts for auto-generating remediation plans.
"""

# =============================================================================
# REMEDIATION PLANNING PROMPTS
# =============================================================================

POLICY_UPDATE_PROMPT = """
You are a compliance remediation specialist generating policy updates.

COMPLIANCE GAP:
{gap_description}

OBLIGATION (from regulator):
{obligation_text}

CURRENT POLICY:
{current_policy}

TASK: Generate a detailed policy update to close this compliance gap.

OUTPUT (strict JSON):
{{
  "policy_sections_to_update": [
    {{
      "section_name": "...",
      "current_text": "...",
      "proposed_text": "...",
      "rationale": "why this update is needed",
      "impact_assessment": "HIGH|MEDIUM|LOW"
    }}
  ],
  "new_sections": [
    {{
      "section_name": "...",
      "proposed_text": "...",
      "rationale": "why this new section is needed"
    }}
  ],
  "implementation_notes": ["..."],
  "approval_required_from": ["Compliance Head", "Legal", "..."]
}}

RULES:
- Be specific and actionable
- Cite regulatory requirements
- Consider practical implementation
- Assess business impact
"""

ACTION_PLAN_PROMPT = """
You are creating a step-by-step remediation action plan.

COMPLIANCE GAP:
{gap_description}

OBLIGATION:
{obligation_text}

DEADLINE: {deadline}

TASK: Create detailed action plan to achieve compliance.

OUTPUT (strict JSON):
{{
  "action_steps": [
    {{
      "step_number": 1,
      "action": "specific action to take",
      "owner": "responsible team/role",
      "deadline_days": 0,
      "effort_hours": 0,
      "dependencies": ["step 2", "..."],
      "deliverable": "what will be produced"
    }}
  ],
  "critical_path": [1, 3, 5],
  "total_effort_hours": 0,
  "estimated_cost": 0,
  "risk_level": "HIGH|MEDIUM|LOW"
}}

RULES:
- Steps must be sequential and logical
- Assign realistic effort estimates
- Identify critical path
- Include verification steps
"""

TRAINING_PLAN_PROMPT = """
You are designing compliance training to support remediation.

OBLIGATION:
{obligation_text}

AFFECTED_STAFF:
{affected_roles}

TASK: Create training plan for staff impacted by this obligation.

OUTPUT (strict JSON):
{{
  "training_modules": [
    {{
      "module_name": "...",
      "audience": ["Branch Staff", "Compliance Officers", "..."],
      "duration_hours": 0,
      "delivery_method": "online|classroom|hybrid",
      "content_outline": ["topic 1", "topic 2", "..."],
      "assessment_required": true/false
    }}
  ],
  "total_training_hours": 0,
  "estimated_cost_per_person": 0,
  "completion_deadline": "YYYY-MM-DD"
}}
"""

GAP_PRIORITIZATION_PROMPT = """
You are prioritizing multiple compliance gaps by risk.

GAPS:
{gaps_json}

TASK: Prioritize gaps by risk, impact, and effort.

OUTPUT (strict JSON):
{{
  "prioritized_gaps": [
    {{
      "gap_id": "...",
      "priority_score": 0.0-1.0,
      "risk_level": "CRITICAL|HIGH|MEDIUM|LOW",
      "business_impact": "description",
      "effort_required": "HIGH|MEDIUM|LOW",
      "recommended_sequence": 1
    }}
  ],
  "rationale": "overall prioritization strategy"
}}

RULES:
- CRITICAL regulatory deadlines = highest priority
- High business impact + low effort = quick wins
- Dependencies affect sequence
"""
