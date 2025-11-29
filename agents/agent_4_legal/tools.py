"""
Agent 4: Legal Intelligence LLM
Tools for extracting obligations using LLM (simulated for MVP).
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random


# =============================================================================
# Simulated LLM Responses (for MVP/demo without API keys)
# In production, replace with actual Claude API calls
# =============================================================================

def simulate_llm_call(prompt: str, context: Dict) -> str:
    """
    Simulate LLM response for demo purposes.
    In production: Replace with actual Anthropic API call.
    """
    # Generate deterministic but varied responses based on prompt hash
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    seed = int(prompt_hash[:8], 16)
    random.seed(seed)
    
    # Return simulated JSON responses
    if "extract" in prompt.lower() and "obligations" in prompt.lower():
        return json.dumps({
            "obligations": [
                {
                    "text": "All financial institutions must implement enhanced due diligence procedures",
                    "summary": "Implement enhanced due diligence for customer verification",
                    "type": "KYC",
                    "affected_entities": ["Commercial Banks", "NBFCs"],
                    "deadline": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
                    "confidence": 0.85
                }
            ]
        })
    elif "severity" in prompt.lower():
        return json.dumps({
            "severity": random.choice(["CRITICAL", "HIGH", "MEDIUM"]),
            "reasoning": "Based on scope and deadline analysis",
            "confidence": 0.82
        })
    elif "action" in prompt.lower():
        return json.dumps({
            "action_items": [
                "Review current KYC procedures",
                "Update verification system",
                "Train staff on new requirements",
                "Conduct internal audit"
            ],
            "estimated_effort_hours": 120,
            "departments_involved": ["Compliance", "IT", "Training"]
        })
    elif "ambiguities" in prompt.lower():
        return json.dumps({
            "ambiguities": [],
            "requires_clarification": False,
            "confidence": 0.90
        })
    elif "policy" in prompt.lower():
        return json.dumps({
            "mapped_policy": "KYC-Policy-v2.1",
            "relevance": "HIGH",
            "requires_policy_update": True,
            "suggested_changes": "Add enhanced due diligence section",
            "confidence": 0.78
        })
    else:
        return "{}"


# =============================================================================
# TOOL 1: llm_extract_obligations
# =============================================================================

def llm_extract_obligations(text: str, source: str, change_type: str = "content") -> List[Dict]:
    """
    Extract obligations from regulatory text using LLM.
    
    Args:
        text: Regulatory text to analyze
        source: Source name (e.g., "RBI", "SEBI")
        change_type: Type of change detected
        
    Returns:
        List of extracted obligations
    """
    from agents.agent_4_legal.prompts import EXTRACT_OBLIGATIONS_PROMPT
    
    print(f"[INFO] Extracting obligations from {source}...")
    
    prompt = EXTRACT_OBLIGATIONS_PROMPT.format(
        regulatory_text=text[:2000],  # Limit to avoid token limits
        source_name=source,
        change_type=change_type
    )
    
    # Simulated LLM call
    response = simulate_llm_call(prompt, {"source": source})
    result = json.loads(response)
    
    obligations = result.get("obligations", [])
    print(f"[SUCCESS] Extracted {len(obligations)} obligations")
    
    return obligations


# =============================================================================
# TOOL 2: classify_obligation_type
# =============================================================================

def classify_obligation_type(obligation_text: str) -> str:
    """
    Classify obligation into standard categories.
    
    Categories: disclosure, KYC, capital, reporting, conduct, licensing, sanctions
    """
    # Simple keyword-based classification (LLM would be better)
    text_lower = obligation_text.lower()
    
    if any(word in text_lower for word in ['kyc', 'know your customer', 'due diligence', 'verification']):
        return "KYC"
    elif any(word in text_lower for word in ['report', 'filing', 'submit', 'disclosure']):
        return "reporting"
    elif any(word in text_lower for word in ['capital', 'reserve', 'liquidity', 'ratio']):
        return "capital"
    elif any(word in text_lower for word in ['license', 'authorization', 'approval']):
        return "licensing"
    elif any(word in text_lower for word in ['sanction', 'penalty', 'prohibition']):
        return "sanctions"
    elif any(word in text_lower for word in ['conduct', 'behavior', 'ethics', 'conflict']):
        return "conduct"
    else:
        return "other"


# =============================================================================
# TOOL 3: extract_deadline
# =============================================================================

def extract_deadline(text: str) -> Optional[str]:
    """
    Extract compliance deadline from text.
    
    Returns:
        ISO date string or "not specified" or "ongoing"
    """
    import re
    
    text_lower = text.lower()
    
    # Look for specific dates
    date_patterns = [
        r'by\s+(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
        r'(\d{4})-(\d{2})-(\d{2})',
        r'(q[1-4])\s+(\d{4})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text_lower)
        if match:
            # Simplified: return a date 6 months from now
            deadline = (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")
            return deadline
    
    # Check for relative deadlines
    if "within" in text_lower or "days" in text_lower or "months" in text_lower:
        return "not specified - relative deadline"
    
    if "ongoing" in text_lower or "continuous" in text_lower:
        return "ongoing"
    
    return "not specified"


# =============================================================================
# TOOL 4: extract_entities
# =============================================================================

def extract_entities(text: str) -> List[str]:
    """Extract affected entity types"""
    entities = []
    
    entity_keywords = {
        "Commercial Banks": ["banks", "commercial bank", "scheduled bank"],
        "NBFCs": ["nbfc", "non-banking financial"],
        "Payment Banks": ["payment bank"],
        "Mutual Funds": ["mutual fund", "asset management"],
        "Insurance Companies": ["insurance", "insurer"],
        "All Financial Institutions": ["all financial institutions", "financial sector"]
    }
    
    text_lower = text.lower()
    
    for entity, keywords in entity_keywords.items():
        if any(kw in text_lower for kw in keywords):
            entities.append(entity)
    
    return entities if entities else ["All Financial Institutions"]


# =============================================================================
# TOOL 5: assess_obligation_severity
# =============================================================================

def assess_obligation_severity(obligation: Dict) -> tuple[str, float]:
    """
    Assess severity of obligation.
    
    Returns:
        (severity_level, confidence_score)
    """
    from agents.agent_4_legal.prompts import CLASSIFY_SEVERITY_PROMPT
    
    prompt = CLASSIFY_SEVERITY_PROMPT.format(
        obligation_text=obligation.get("text", ""),
        deadline=obligation.get("deadline", "not specified"),
        entities=", ".join(obligation.get("affected_entities", [])),
        obligation_type=obligation.get("type", "other")
    )
    
    response = simulate_llm_call(prompt, obligation)
    result = json.loads(response)
    
    return result["severity"], result["confidence"]


# =============================================================================
# TOOL 6-12: Additional Tools
# =============================================================================

def generate_action_items(obligation: Dict) -> List[str]:
    """Generate actionable tasks"""
    from agents.agent_4_legal.prompts import GENERATE_ACTION_ITEMS_PROMPT
    
    prompt = GENERATE_ACTION_ITEMS_PROMPT.format(
        obligation_text=obligation.get("summary", ""),
        deadline=obligation.get("deadline", ""),
        entities=", ".join(obligation.get("affected_entities", []))
    )
    
    response = simulate_llm_call(prompt, obligation)
    result = json.loads(response)
    
    return result.get("action_items", [])


def detect_ambiguities(text: str) -> List[Dict]:
    """Detect unclear requirements"""
    from agents.agent_4_legal.prompts import DETECT_AMBIGUITIES_PROMPT
    
    prompt = DETECT_AMBIGUITIES_PROMPT.format(text=text[:1000])
    response = simulate_llm_call(prompt, {"text": text})
    result = json.loads(response)
    
    return result.get("ambiguities", [])


def map_to_policies(obligation: Dict, available_policies: List[str]) -> Optional[str]:
    """Map obligation to internal policy"""
    from agents.agent_4_legal.prompts import MAP_TO_POLICY_PROMPT
    
    prompt = MAP_TO_POLICY_PROMPT.format(
        obligation_summary=obligation.get("summary", ""),
        obligation_type=obligation.get("type", ""),
        policy_list="\n".join(available_policies)
    )
    
    response = simulate_llm_call(prompt, obligation)
    result = json.loads(response)
    
    return result.get("mapped_policy")


def extract_penalties(text: str) -> Optional[str]:
    """Extract penalty information"""
    import re
    
    # Look for monetary penalties
    penalty_pattern = r'₹\s*[\d,]+|penalty|fine|sanction'
    
    if re.search(penalty_pattern, text, re.IGNORECASE):
        return "Penalties specified in regulation"
    
    return None


def generate_compliance_checklist(obligations: List[Dict]) -> List[Dict]:
    """Generate structured compliance checklist"""
    checklist = []
    
    for i, obl in enumerate(obligations, 1):
        checklist.append({
            "item_id": f"CHK-{i:03d}",
            "obligation": obl.get("summary", ""),
            "deadline": obl.get("deadline", ""),
            "owner": "Compliance Team",
            "status": "pending",
            "priority": obl.get("severity", "MEDIUM")
        })
    
    return checklist


def validate_extraction(original_text: str, extracted_obligations: List[Dict]) -> float:
    """Validate extraction quality"""
    if not extracted_obligations:
        return 0.0
    
    # Simple validation: check if obligation text exists in source
    valid_count = 0
    for obl in extracted_obligations:
        if obl.get("text", "").lower() in original_text.lower():
            valid_count += 1
    
    return valid_count / len(extracted_obligations) if extracted_obligations else 0.0
