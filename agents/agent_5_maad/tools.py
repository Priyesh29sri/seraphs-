"""
Agent 5: MAAD (Multi-Agent Adversarial Debate)
Tools for prosecutor, defender, and judge agents.
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List
import random


# =============================================================================
# Simulated LLM for MAAD (Demo Mode)
# =============================================================================

def simulate_maad_llm(prompt: str, role: str) -> str:
    """
    Simulate MAAD agent responses.
    Replace with real Claude API in production.
    """
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    seed = int(prompt_hash[:8], 16)
    random.seed(seed)
    
    if "PROSECUTOR" in role:
        return json.dumps({
            "challenges": [
                {
                    "issue": "Missing explicit deadline for implementation",
                    "evidence": "Source does not specify 'by when' this must be completed",
                    "severity": "HIGH",
                    "type": "missing_info"
                },
                {
                    "issue": "Ambiguous definition of 'enhanced due diligence'",
                    "evidence": "Source uses general term without specific procedures",
                    "severity": "MEDIUM",
                    "type": "ambiguity"
                }
            ],
            "alternative_interpretation": "This may be guidance rather than mandatory requirement",
            "confidence_in_challenge": 0.72,
            "recommend_rejection": False
        })
    
    elif "DEFENDER" in role:
        return json.dumps({
            "evidence": [
                {
                    "supports": "mandatory nature",
                    "quote": "institutions are required to implement enhanced procedures",
                    "explanation": "Use of 'required' indicates mandatory obligation",
                    "page_reference": "Section 3.2"
                },
                {
                    "supports": "scope of application",
                    "quote": "all commercial banks and NBFCs shall comply",
                    "explanation": "Explicitly lists affected entities",
                    "page_reference": "Section 1.1"
                }
            ],
            "refutations": [
                {
                    "challenge_id": 0,
                    "refutation": "Deadline is implicit - effective immediately per regulatory practice",
                    "counter_evidence": "Unless otherwise stated, RBI circulars take effect on date of issue",
                    "clarification": "Standard 30-day implementation period applies"
                }
            ],
            "additional_context": "RBI has authority under Banking Regulation Act to issue binding circulars",
            "confidence_in_claim": 0.85
        })
    
    elif "JUDGE" in role:
        return json.dumps({
            "verdict": "MODIFIED",
            "confidence": 0.82,
            "reasoning": "The obligation is valid and supported by source text, but requires clarifications on deadline and specific procedures. Both prosecutor and defender made valid points.",
            "key_evidence": [
                "Source uses mandatory language ('required', 'shall')",
                "Explicitly lists affected entities",
                "Part of binding regulatory circular"
            ],
            "concerns": [
                "Deadline needs explicit statement",
                "'Enhanced' procedures need definition"
            ],
            "verified_obligation": {
                "text": "All commercial banks and NBFCs must implement enhanced due diligence procedures (as defined in Section 3.2) within 30 days",
                "summary": "Implement enhanced KYC due diligence within standard compliance period",
                "type": "KYC",
                "severity": "HIGH",
                "deadline": "30 days from circular date",
                "conditions": ["Applies to all commercial banks and NBFCs", "Procedures defined in Section 3.2"]
            },
            "amendments": [
                {
                    "field": "text",
                    "original": "All banks must implement enhanced due diligence",
                    "amended": "All commercial banks and NBFCs must implement enhanced due diligence procedures within 30 days",
                    "reason": "Added deadline and specific entity types"
                },
                {
                    "field": "severity",
                    "original": "CRITICAL",
                    "amended": "HIGH",
                    "reason": "Standard compliance update, not emergency directive"
                }
            ],
            "hitl_required": False,
            "hitl_reason": None
        })
    
    return "{}"


# =============================================================================
# PROSECUTOR TOOLS
# =============================================================================

def challenge_claim(obligation: Dict, source_text: str) -> Dict:
    """
    Prosecutor: Generate challenges to the obligation claim.
    """
    from agents.agent_5_maad.prompts import PROSECUTOR_CHALLENGE_PROMPT
    
    print(f"[PROSECUTOR] 🔴 Challenging claim: {obligation.get('summary', '')[:50]}...")
    
    prompt = PROSECUTOR_CHALLENGE_PROMPT.format(
        obligation_text=obligation.get('text', ''),
        obligation_summary=obligation.get('summary', ''),
        obligation_type=obligation.get('type', ''),
        severity=obligation.get('severity', ''),
        source_excerpt=source_text[:1000]  # First 1000 chars
    )
    
    response = simulate_maad_llm(prompt, "PROSECUTOR")
    result = json.loads(response)
    
    print(f"[PROSECUTOR] Found {len(result.get('challenges', []))} challenges")
    
    return result


def find_contradictions(obligation: Dict, source_text: str) -> List[Dict]:
    """
    Prosecutor: Find contradictions in source text.
    """
    # Simplified: look for conflicting keywords
    contradictions = []
    
    text_lower = source_text.lower()
    if 'may' in text_lower and 'must' in text_lower:
        contradictions.append({
            "type": "modal_verb_conflict",
            "description": "Source uses both 'may' (optional) and 'must' (mandatory)"
        })
    
    return contradictions


# =============================================================================
# DEFENDER TOOLS
# =============================================================================

def provide_evidence(obligation: Dict, source_text: str, challenges: List[Dict]) -> Dict:
    """
    Defender: Provide evidence supporting the claim.
    """
    from agents.agent_5_maad.prompts import DEFENDER_RESPONSE_PROMPT
    
    print(f"[DEFENDER] 🟢 Defending claim with evidence...")
    
    prompt = DEFENDER_RESPONSE_PROMPT.format(
        obligation_text=obligation.get('text', ''),
        prosecutor_challenges=json.dumps(challenges, indent=2),
        source_text=source_text[:2000]  # Up to 2000 chars
    )
    
    response = simulate_maad_llm(prompt, "DEFENDER")
    result = json.loads(response)
    
    print(f"[DEFENDER] Provided {len(result.get('evidence', []))} pieces of evidence")
    print(f"[DEFENDER] Refuted {len(result.get('refutations', []))} challenges")
    
    return result


def extract_supporting_quotes(obligation_text: str, source_text: str) -> List[str]:
    """
    Defender: Extract quotes that support the obligation.
    """
    # Simplified: find sentences containing key obligation terms
    quotes = []
    
    key_terms = ['must', 'shall', 'required', 'mandatory', 'obligat']
    sentences = source_text.split('.')
    
    for sentence in sentences[:10]:  # First 10 sentences
        if any(term in sentence.lower() for term in key_terms):
            quotes.append(sentence.strip())
    
    return quotes[:3]  # Top 3


# =============================================================================
# JUDGE TOOLS
# =============================================================================

def issue_verdict(
    obligation: Dict,
    prosecutor_args: Dict,
    defender_args: Dict,
    source_text: str
) -> Dict:
    """
    Judge: Issue final verdict after reviewing debate.
    """
    from agents.agent_5_maad.prompts import JUDGE_VERDICT_PROMPT
    
    print(f"[JUDGE] ⚖️  Reviewing debate and issuing verdict...")
    
    prompt = JUDGE_VERDICT_PROMPT.format(
        obligation_text=obligation.get('text', ''),
        prosecutor_arguments=json.dumps(prosecutor_args, indent=2),
        defender_arguments=json.dumps(defender_args, indent=2),
        source_text=source_text[:2000]
    )
    
    response = simulate_maad_llm(prompt, "JUDGE")
    result = json.loads(response)
    
    print(f"[JUDGE] Verdict: {result.get('verdict')} (confidence: {result.get('confidence', 0):.2f})")
    
    return result


def calculate_final_confidence(
    initial_confidence: float,
    prosecutor_confidence: float,
    defender_confidence: float,
    judge_confidence: float
) -> float:
    """
    Calculate final confidence score combining all agents.
    
    Formula: weighted average favoring judge's assessment
    """
    final = (
        initial_confidence * 0.25 +
        defender_confidence * 0.25 +
        (1 - prosecutor_confidence) * 0.20 +
        judge_confidence * 0.30
    )
    
    return round(final, 3)


def weigh_arguments(prosecutor_args: Dict, defender_args: Dict) -> Dict:
    """
    Judge: Weigh strength of arguments from both sides.
    """
    prosecutor_score = len(prosecutor_args.get('challenges', [])) * 0.3
    prosecutor_score += prosecutor_args.get('confidence_in_challenge', 0) * 0.7
    
    defender_score = len(defender_args.get('evidence', [])) * 0.3
    defender_score += defender_args.get('confidence_in_claim', 0) * 0.7
    
    return {
        "prosecutor_strength": round(prosecutor_score, 2),
        "defender_strength": round(defender_score, 2),
        "advantage": "defender" if defender_score > prosecutor_score else "prosecutor"
    }


# =============================================================================
# UTILITY TOOLS
# =============================================================================

def determine_hitl_requirement(verdict: str, confidence: float, concerns: List[str]) -> tuple:
    """
    Determine if human-in-the-loop review is needed.
    
    Returns: (hitl_required: bool, reason: str)
    """
    if verdict == "NEEDS_CLARIFICATION":
        return True, "Verdict requires clarification"
    
    if verdict == "REJECTED":
        return True, "Obligation rejected - human should confirm"
    
    if confidence < 0.65:
        return True, f"Low confidence ({confidence:.2f})"
    
    if len(concerns) > 2:
        return True, f"Multiple concerns ({len(concerns)})"
    
    return False, None


def generate_debate_summary(
    prosecutor_args: Dict,
    defender_args: Dict,
    verdict_result: Dict
) -> str:
    """
    Generate human-readable debate summary.
    """
    summary_parts = []
    
    # Prosecutor
    challenges = prosecutor_args.get('challenges', [])
    summary_parts.append(f"Prosecutor raised {len(challenges)} challenge(s):")
    for i, ch in enumerate(challenges[:2], 1):  # Top 2
        summary_parts.append(f"  {i}. {ch.get('issue', '')}")
    
    # Defender
    refutations = defender_args.get('refutations', [])
    summary_parts.append(f"\nDefender provided {len(refutations)} refutation(s) with evidence.")
    
    # Judge
    verdict = verdict_result.get('verdict', '')
    confidence = verdict_result.get('confidence', 0)
    summary_parts.append(f"\nJudge Verdict: {verdict} ({confidence:.0%} confidence)")
    
    return "\n".join(summary_parts)
