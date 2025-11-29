"""
Agent 5: MAAD (Multi-Agent Adversarial Debate)
Main agent orchestrating prosecutor, defender, and judge debate.
"""

import json
from datetime import datetime
from typing import Dict, List
from agents.agent_5_maad import tools


class MAADAgent:
    """
    Agent 5: Multi-Agent Adversarial Debate
    
    Verifies Agent 4's obligation extractions through adversarial debate.
    
    Sub-Agents:
    - Prosecutor: Challenges claims
    - Defender: Provides evidence
    - Judge: Issues verdict
    """
    
    def __init__(self):
        self.confidence_threshold = 0.65
        print("[INFO] Agent 5 initialized (MAAD - Adversarial Debate)")
        print("  Sub-agents: Prosecutor, Defender, Judge")
    
    def verify_obligation(self, obligation: Dict, source_text: str = "") -> Dict:
        """
        Verify a single obligation through adversarial debate.
        
        Args:
            obligation: Obligation from Agent 4
            source_text: Original regulatory text (for evidence)
            
        Returns:
            DEBATE_RESULT with verdict and verified obligation
        """
        obligation_id = obligation.get("obligation_id", "unknown")
        
        print(f"\n{'='*80}")
        print(f"MAAD DEBATE: {obligation_id}")
        print(f"{'='*80}")
        
        print(f"\nObligation: {obligation.get('summary', '')[:80]}...")
        print(f"Initial Confidence: {obligation.get('confidence', 0):.2f}")
        
        # Round 1: Prosecutor challenges
        print(f"\n--- Round 1: Prosecutor ---")
        prosecutor_result = tools.challenge_claim(obligation, source_text)
        
        challenges = prosecutor_result.get('challenges', [])
        prosecutor_confidence = prosecutor_result.get('confidence_in_challenge', 0.5)
        
        # Show challenges
        for i, challenge in enumerate(challenges, 1):
            print(f"  Challenge {i} [{challenge.get('severity')}]: {challenge.get('issue')}")
        
        # Round 2: Defender responds
        print(f"\n--- Round 2: Defender ---")
        defender_result = tools.provide_evidence(obligation, source_text, challenges)
        
        evidence_count = len(defender_result.get('evidence', []))
        refutation_count = len(defender_result.get('refutations', []))
        defender_confidence = defender_result.get('confidence_in_claim', 0.8)
        
        print(f"  Evidence pieces: {evidence_count}")
        print(f"  Refutations: {refutation_count}")
        
        # Round 3: Judge decides
        print(f"\n--- Round 3: Judge ---")
        verdict_result = tools.issue_verdict(
            obligation,
            prosecutor_result,
            defender_result,
            source_text
        )
        
        verdict = verdict_result.get('verdict')
        judge_confidence = verdict_result.get('confidence', 0)
        
        # Calculate final confidence
        initial_confidence = obligation.get('confidence', 0.5)
        final_confidence = tools.calculate_final_confidence(
            initial_confidence,
            prosecutor_confidence,
            defender_confidence,
            judge_confidence
        )
        
        # Determine HITL requirement
        concerns = verdict_result.get('concerns', [])
        hitl_required, hitl_reason = tools.determine_hitl_requirement(
            verdict, final_confidence, concerns
        )
        
        # Weigh arguments for analysis
        argument_weights = tools.weigh_arguments(prosecutor_result, defender_result)
        
        # Generate summary
        debate_summary = tools.generate_debate_summary(
            prosecutor_result,
            defender_result,
            verdict_result
        )
        
        # Build result
        result = {
            "obligation_id": obligation_id,
            "original_obligation": obligation,
            "verdict": verdict,
            "final_confidence": final_confidence,
            "debate_transcript": {
                "prosecutor": {
                    "challenges": challenges,
                    "alternative_interpretation": prosecutor_result.get('alternative_interpretation'),
                    "confidence": prosecutor_confidence
                },
                "defender": {
                    "evidence": defender_result.get('evidence', []),
                    "refutations": defender_result.get('refutations', []),
                    "context": defender_result.get('additional_context'),
                    "confidence": defender_confidence
                },
                "judge": {
                    "verdict": verdict,
                    "reasoning": verdict_result.get('reasoning'),
                    "key_evidence": verdict_result.get('key_evidence', []),
                    "concerns": concerns,
                    "confidence": judge_confidence
                }
            },
            "verified_obligation": verdict_result.get('verified_obligation'),
            "amendments": verdict_result.get('amendments', []),
            "argument_weights": argument_weights,
            "hitl_required": hitl_required,
            "hitl_reason": hitl_reason,
            "debate_summary": debate_summary,
            "verified_at": datetime.utcnow().isoformat() + "Z"
        }
        
        # Display result
        print(f"\n{'='*80}")
        print(f"VERDICT: {verdict} (Confidence: {final_confidence:.2f})")
        if amendments := result.get('amendments'):
            print(f"Amendments: {len(amendments)}")
        if hitl_required:
            print(f"⚠️  HITL Required: {hitl_reason}")
        print(f"{'='*80}\n")
        
        return result
    
    def verify_batch(self, legal_analyses: List[Dict]) -> Dict:
        """
        Verify batch of obligations from Agent 4.
        
        Args:
            legal_analyses: List of legal analysis results from Agent 4
            
        Returns:
            Batch MAAD results
        """
        print(f"\n[INFO] MAAD batch verification: {len(legal_analyses)} obligations")
        
        results = []
        
        verdict_counts = {
            "VERIFIED": 0,
            "MODIFIED": 0,
            "NEEDS_CLARIFICATION": 0,
            "REJECTED": 0
        }
        
        hitl_count = 0
        total_confidence_gain = 0
        
        for analysis in legal_analyses:
            obligations = analysis.get('obligations_extracted', [])
            source = analysis.get('source', 'unknown')
            
            # For demo, use summary as source text (in production, would fetch full source)
            source_text = analysis.get('analysis_summary', '')
            
            for obligation in obligations:
                try:
                    # Run MAAD verification
                    debate_result = self.verify_obligation(obligation, source_text)
                    
                    # Track stats
                    verdict = debate_result.get('verdict')
                    verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
                    
                    if debate_result.get('hitl_required'):
                        hitl_count += 1
                    
                    # Calculate confidence improvement
                    original_conf = obligation.get('confidence', 0)
                    final_conf = debate_result.get('final_confidence', 0)
                    confidence_gain = final_conf - original_conf
                    total_confidence_gain += confidence_gain
                    
                    results.append(debate_result)
                    
                except Exception as e:
                    print(f"[ERROR] MAAD verification failed: {e}")
                    results.append({
                        "obligation_id": obligation.get("obligation_id"),
                        "error": str(e),
                        "verdict": "NEEDS_CLARIFICATION",
                        "hitl_required": True
                    })
        
        # Calculate average confidence improvement
        avg_confidence_gain = total_confidence_gain / len(results) if results else 0
        
        output = {
            "agent": "agent-5-maad",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_obligations": len(results),
            "verdict_breakdown": verdict_counts,
            "hitl_count": hitl_count,
            "avg_confidence_improvement": round(avg_confidence_gain, 3),
            "debate_results": results
        }
        
        print(f"\n[SUCCESS] MAAD batch complete:")
        print(f"  Total Obligations: {len(results)}")
        print(f"  Verdicts: {verdict_counts}")
        print(f"  HITL Required: {hitl_count}")
        print(f"  Avg Confidence Gain: {avg_confidence_gain:+.3f}")
        
        return output
