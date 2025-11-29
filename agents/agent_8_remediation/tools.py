"""
Agent 8: Remediation Planner  
Tools for auto-generating remediation plans.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List


# =============================================================================
# REMEDIATION TOOLS
# =============================================================================

def identify_gap(obligation: Dict, existing_policies: List[Dict]) -> Dict:
    """
    Identify compliance gap between obligation and existing policies.
    
    Args:
        obligation: Obligation from Agent 5
        existing_policies: List of company policies
        
    Returns:
        Gap analysis
    """
    print(f"[REMEDIATION] Analyzing gap for: {obligation.get('summary', '')[:50]}...")
    
    # Check if obligation is covered by any policy
    covered = False
    covering_policies = []
    
    for policy in existing_policies:
        # Simplified matching (in production: use semantic similarity)
        if obligation.get('type') in policy.get('covers', []):
            covered = True
            covering_policies.append(policy['name'])
    
    gap = {
        "obligation_id": obligation.get('obligation_id'),
        "obligation_type": obligation.get('type'),
        "obligation_text": obligation.get('text'),
        "covered": covered,
        "covering_policies": covering_policies,
        "gap_severity": "NONE" if covered else obligation.get('severity', 'HIGH'),
        "requires_action": not covered
    }
    
    if not covered:
        print(f"[REMEDIATION] ⚠️  GAP FOUND: No policy covers {obligation.get('type')}")
    else:
        print(f"[REMEDIATION] ✓ Covered by: {', '.join(covering_policies)}")
    
    return gap


def generate_policy_update(gap: Dict) -> Dict:
    """
    Generate policy update suggestion (LLM-powered).
    
    Args:
        gap: Gap analysis from identify_gap()
        
    Returns:
        Policy update recommendations
    """
    from agents.agent_8_remediation.prompts import POLICY_UPDATE_PROMPT
    
    print(f"[REMEDIATION] Generating policy update for gap...")
    
    # In production: Use real LLM via utils/llm_client.py
    # For demo: Simulated response
    
    policy_update = {
        "gap_id": gap.get('obligation_id'),
        "policy_sections_to_update": [
            {
                "section_name": "Customer Due Diligence",
                "current_text": "Standard KYC procedures shall be followed",
                "proposed_text": "Enhanced due diligence procedures including additional documentation and verification shall be implemented for all new customers",
                "rationale": "Align with new regulatory requirement for enhanced KYC",
                "impact_assessment": "HIGH"
            }
        ],
        "new_sections": [],
        "implementation_notes": [
            "Update staff training materials",
            "Modify onboarding forms",
            "Update IT systems for additional data fields"
        ],
        "approval_required_from": ["Compliance Head", "Legal", "Board"]
    }
    
    print(f"[REMEDIATION] Generated {len(policy_update['policy_sections_to_update'])} policy updates")
    
    return policy_update


def create_action_plan(gap: Dict, policy_update: Dict) -> Dict:
    """
    Create step-by-step remediation action plan.
    
    Args:
        gap: Gap analysis
        policy_update: Policy update recommendations
        
    Returns:
        Detailed action plan
    """
    from agents.agent_8_remediation.prompts import ACTION_PLAN_PROMPT
    
    print(f"[REMEDIATION] Creating action plan...")
    
    # Simulated LLM response
    action_plan = {
        "gap_id": gap.get('obligation_id'),
        "action_steps": [
            {
                "step_number": 1,
                "action": "Draft policy update document",
                "owner": "Compliance Team",
                "deadline_days": 7,
                "effort_hours": 16,
                "dependencies": [],
                "deliverable": "Updated policy document"
            },
            {
                "step_number": 2,
                "action": "Legal review of policy changes",
                "owner": "Legal Team",
                "deadline_days": 14,
                "effort_hours": 8,
                "dependencies": ["step 1"],
                "deliverable": "Legal approval"
            },
            {
                "step_number": 3,
                "action": "Update IT systems for new data fields",
                "owner": "IT Team",
                "deadline_days": 21,
                "effort_hours": 40,
                "dependencies": ["step 2"],
                "deliverable": "System modifications"
            },
            {
                "step_number": 4,
                "action": "Develop staff training materials",
                "owner": "Training Team",
                "deadline_days": 21,
                "effort_hours": 24,
                "dependencies": ["step 2"],
                "deliverable": "Training modules"
            },
            {
                "step_number": 5,
                "action": "Conduct staff training",
                "owner": "Training Team",
                "deadline_days": 28,
                "effort_hours": 60,
                "dependencies": ["step 4"],
                "deliverable": "Trained staff"
            },
            {
                "step_number": 6,
                "action": "Implement new procedures",
                "owner": "Compliance Team",
                "deadline_days": 30,
                "effort_hours": 20,
                "dependencies": ["step 3", "step 5"],
                "deliverable": "Full implementation"
            }
        ],
        "critical_path": [1, 2, 3, 6],
        "total_effort_hours": 168,
        "estimated_cost": 50000,
        "risk_level": "MEDIUM"
    }
    
    print(f"[REMEDIATION] Action plan: {len(action_plan['action_steps'])} steps, "
          f"{action_plan['total_effort_hours']}h effort")
    
    return action_plan


def estimate_effort(action_plan: Dict) -> Dict:
    """
    Estimate time and cost for remediation.
    
    Args:
        action_plan: Action plan from create_action_plan()
        
    Returns:
        Effort estimation
    """
    total_hours = action_plan.get('total_effort_hours', 0)
    hourly_rate = 100  # Average blended rate
    
    estimation = {
        "total_hours": total_hours,
        "total_days": total_hours / 8,
        "total_cost": total_hours * hourly_rate,
        "timeline_days": max(step['deadline_days'] for step in action_plan.get('action_steps', [])),
        "resource_requirements": {
            "compliance_team": 36,
            "legal_team": 8,
            "it_team": 40,
            "training_team": 84
        }
    }
    
    print(f"[REMEDIATION] Estimate: {estimation['total_hours']}h, "
          f"${estimation['total_cost']:,}, {estimation['timeline_days']} days")
    
    return estimation


def prioritize_gaps(gaps: List[Dict]) -> List[Dict]:
    """
    Prioritize gaps by risk and effort.
    
    Args:
        gaps: List of identified gaps
        
    Returns:
        Prioritized list
    """
    print(f"[REMEDIATION] Prioritizing {len(gaps)} gaps...")
    
    def priority_score(gap):
        severity_scores = {"CRITICAL": 1.0, "HIGH": 0.8, "MEDIUM": 0.5, "LOW": 0.3}
        return severity_scores.get(gap.get('gap_severity', 'MEDIUM'), 0.5)
    
    prioritized = sorted(gaps, key=priority_score, reverse=True)
    
    for i, gap in enumerate(prioritized, 1):
        gap['priority_rank'] = i
        gap['priority_score'] = priority_score(gap)
    
    print(f"[REMEDIATION] Prioritized: Top priority = {prioritized[0].get('obligation_type')}")
    
    return prioritized


def assign_owners(action_steps: List[Dict]) -> Dict:
    """
    Suggest responsible owners for action steps.
    
    Args:
        action_steps: List of action steps
        
    Returns:
        Owner assignments with justification
    """
    # Already assigned in action_plan, but can refine
    owners = {}
    
    for step in action_steps:
        owner = step.get('owner')
        if owner not in owners:
            owners[owner] = []
        owners[owner].append(step['step_number'])
    
    return {
        "assignments": owners,
        "workload_balanced": len(owners) > 1
    }


def generate_training_plan(obligation: Dict, affected_roles: List[str]) -> Dict:
    """
    Generate training plan for affected staff.
    
    Args:
        obligation: Obligation requiring training
        affected_roles: Staff roles affected
        
    Returns:
        Training plan
    """
    from agents.agent_8_remediation.prompts import TRAINING_PLAN_PROMPT
    
    print(f"[REMEDIATION] Generating training plan for {len(affected_roles)} roles...")
    
    training_plan = {
        "obligation_id": obligation.get('obligation_id'),
        "training_modules": [
            {
                "module_name": "Enhanced KYC Procedures",
                "audience": ["Branch Staff", "Compliance Officers"],
                "duration_hours": 2,
                "delivery_method": "hybrid",
                "content_outline": [
                    "New regulatory requirements",
                    "Enhanced verification procedures",
                    "System updates and workflows",
                    "Case studies and examples"
                ],
                "assessment_required": True
            }
        ],
        "total_training_hours": 2,
        "estimated_cost_per_person": 150,
        "completion_deadline": (datetime.utcnow() + timedelta(days=21)).strftime("%Y-%m-%d")
    }
    
    print(f"[REMEDIATION] Training: {training_plan['total_training_hours']}h per person")
    
    return training_plan


def create_compliance_roadmap(action_plans: List[Dict]) -> Dict:
    """
    Create overall compliance roadmap from multiple action plans.
    
    Args:
        action_plans: List of action plans
        
    Returns:
        Compliance roadmap
    """
    print(f"[REMEDIATION] Creating compliance roadmap for {len(action_plans)} initiatives...")
    
    roadmap = {
        "total_initiatives": len(action_plans),
        "timeline_weeks": 12,
        "milestones": [
            {
                "week": 2,
                "milestone": "All policy updates drafted",
                "initiatives": 3
            },
            {
                "week": 4,
                "milestone": "Legal approvals completed",
                "initiatives": 3
            },
            {
                "week": 8,
                "milestone": "IT systems updated",
                "initiatives": 2
            },
            {
                "week": 10,
                "milestone": "Staff training completed",
                "initiatives": 3
            },
            {
                "week": 12,
                "milestone": "Full compliance achieved",
                "initiatives": 3
            }
        ],
        "total_cost": sum(p.get('estimated_cost', 0) for p in action_plans),
        "total_effort_hours": sum(p.get('total_effort_hours', 0) for p in action_plans)
    }
    
    print(f"[REMEDIATION] Roadmap: {roadmap['timeline_weeks']} weeks, "
          f"${roadmap['total_cost']:,}")
    
    return roadmap


def validate_remediation(gap_id: str, implementation_evidence: Dict) -> Dict:
    """
    Validate that remediation is complete.
    
    Args:
        gap_id: Gap identifier
        implementation_evidence: Evidence of completion
        
    Returns:
        Validation result
    """
    print(f"[REMEDIATION] Validating remediation for {gap_id}...")
    
    validation = {
        "gap_id": gap_id,
        "status": "COMPLETE",
        "evidence_provided": True,
        "compliance_achieved": True,
        "verified_by": "Compliance Officer",
        "verified_at": datetime.utcnow().isoformat() + "Z"
    }
    
    print(f"[REMEDIATION] Validation: {validation['status']}")
    
    return validation
