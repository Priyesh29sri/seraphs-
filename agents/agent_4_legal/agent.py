"""
Agent 4: Legal Intelligence LLM
Main agent logic for extracting obligations from regulatory changes.
"""

import json
from datetime import datetime
from typing import Dict, List
from agents.agent_4_legal import tools


class LegalAgent:
    """
    Agent 4: Legal Intelligence LLM
    
    Extracts legal obligations from regulatory changes using LLM.
    """
    
    def __init__(self, internal_policies: List[str] = None):
        self.internal_policies = internal_policies or [
            "KYC-Policy-v2.1",
            "AML-Policy-v3.0",
            "Capital-Adequacy-Policy-v1.5",
            "Reporting-Standards-v2.2",
            "Conduct-Guidelines-v1.8"
        ]
        self.confidence_threshold = 0.7
        print("[INFO] Agent 4 initialized (Legal Intelligence LLM)")
        print(f"  Internal policies loaded: {len(self.internal_policies)}")
    
    def extract_obligations(self, change_analysis: Dict) -> Dict:
        """
        Extract obligations from a change analysis (from Agent 3).
        
        Args:
            change_analysis: Change analysis from Agent 3
            
        Returns:
            Legal analysis with extracted obligations
        """
        snapshot_id = change_analysis.get("snapshot_id")
        source = change_analysis.get("source", "unknown")
        
        print(f"\n[INFO] Extracting obligations: {snapshot_id}")
        print(f"  Source: {source}")
        
        # If no changes detected, skip
        if not change_analysis.get("change_detected", False):
            print("  Status: NO CHANGES - Skipping extraction")
            
            return {
                "snapshot_id": snapshot_id,
                "source": source,
                "obligations_extracted": [],
                "llm_confidence": 1.0,
                "hitl_required": False,
                "analysis_summary": "No changes detected - no extraction needed",
                "analyzed_at": datetime.utcnow().isoformat() + "Z"
            }
        
        # Get changed text (in production, would have full diff context)
        text_sample = change_analysis.get("summary", "")
        change_types = change_analysis.get("change_types", [])
        severity = change_analysis.get("severity", "NONE")
        
        print(f"  Change Severity: {severity}")
        print(f"  Change Types: {', '.join(change_types)}")
        
        # Step 1: Extract obligations using LLM
        raw_obligations = tools.llm_extract_obligations(
            text=text_sample,
            source=source,
            change_type=", ".join(change_types)
        )
        
        if not raw_obligations:
            print("  Status: NO OBLIGATIONS FOUND")
            
            return {
                "snapshot_id": snapshot_id,
                "source": source,
                "obligations_extracted": [],
                "llm_confidence": 0.95,
                "hitl_required": False,
                "analysis_summary": "Changes detected but no new obligations identified",
                "analyzed_at": datetime.utcnow().isoformat() + "Z"
            }
        
        # Step 2: Process each obligation
        processed_obligations = []
        total_confidence = 0
        
        for i, raw_obl in enumerate(raw_obligations, 1):
            print(f"\n  Processing obligation {i}/{len(raw_obligations)}...")
            
            # Enhance with additional analysis
            obligation_id = f"OBL-{source[:3].upper()}-{datetime.utcnow().strftime('%Y%m%d')}-{i:03d}"
            
            # Extract/enhance fields
            if not raw_obl.get("type"):
                raw_obl["type"] = tools.classify_obligation_type(raw_obl.get("text", ""))
            
            if not raw_obl.get("deadline"):
                raw_obl["deadline"] = tools.extract_deadline(raw_obl.get("text", ""))
            
            if not raw_obl.get("affected_entities"):
                raw_obl["affected_entities"] = tools.extract_entities(raw_obl.get("text", ""))
            
            # Assess severity
            severity_level, severity_confidence = tools.assess_obligation_severity(raw_obl)
            
            # Generate action items
            action_items = tools.generate_action_items(raw_obl)
            
            # Map to policies
            policy_mapping = tools.map_to_policies(raw_obl, self.internal_policies)
            
            # Detect ambiguities
            ambiguities = tools.detect_ambiguities(raw_obl.get("text", ""))
            
            # Extract penalties
            penalties = tools.extract_penalties(raw_obl.get("text", ""))
            
            # Build processed obligation
            processed = {
                "obligation_id": obligation_id,
                "text": raw_obl.get("text", ""),
                "summary": raw_obl.get("summary", ""),
                "type": raw_obl.get("type", "other"),
                "affected_entities": raw_obl.get("affected_entities", []),
                "deadline": raw_obl.get("deadline", "not specified"),
                "severity": severity_level,
                "confidence": raw_obl.get("confidence", 0.8),
                "action_items": action_items,
                "policy_mapping": policy_mapping,
                "penalties": penalties,
                "ambiguities": ambiguities,
                "requires_review": len(ambiguities) > 0 or raw_obl.get("confidence", 1.0) < self.confidence_threshold
            }
            
            processed_obligations.append(processed)
            total_confidence += processed["confidence"]
            
            print(f"    ✓ Type: {processed['type']}, Severity: {severity_level}")
            print(f"    ✓ Confidence: {processed['confidence']:.2f}, Actions: {len(action_items)}")
        
        # Calculate overall confidence
        avg_confidence = total_confidence / len(processed_obligations) if processed_obligations else 0
        
        # Determine HITL requirement
        hitl_required = self._should_escalate_to_hitl(processed_obligations, avg_confidence)
        
        # Generate compliance checklist
        checklist = tools.generate_compliance_checklist(processed_obligations)
        
        result = {
            "snapshot_id": snapshot_id,
            "source": source,
            "obligations_extracted": processed_obligations,
            "obligations_count": len(processed_obligations),
            "llm_confidence": round(avg_confidence, 2),
            "hitl_required": hitl_required,
            "compliance_checklist": checklist,
            "analysis_summary": self._generate_summary(processed_obligations, severity),
            "analyzed_at": datetime.utcnow().isoformat() + "Z"
        }
        
        print(f"\n[SUCCESS] Extracted {len(processed_obligations)} obligations")
        print(f"  Avg Confidence: {avg_confidence:.2f}")
        print(f"  HITL Required: {hitl_required}")
        
        return result
    
    def _should_escalate_to_hitl(self, obligations: List[Dict], avg_confidence: float) -> bool:
        """Determine if human review is needed"""
        
        # Escalate if low confidence
        if avg_confidence < self.confidence_threshold:
            print(f"[WARNING] HITL escalation: Low confidence ({avg_confidence:.2f})")
            return True
        
        # Escalate if any CRITICAL severity
        critical_count = sum(1 for o in obligations if o.get("severity") == "CRITICAL")
        if critical_count > 0:
            print(f"[WARNING] HITL escalation: {critical_count} CRITICAL obligations")
            return True
        
        # Escalate if many ambiguities
        total_ambiguities = sum(len(o.get("ambiguities", [])) for o in obligations)
        if total_ambiguities > 2:
            print(f"[WARNING] HITL escalation: {total_ambiguities} ambiguities detected")
            return True
        
        return False
    
    def _generate_summary(self, obligations: List[Dict], change_severity: str) -> str:
        """Generate human-readable summary"""
        if not obligations:
            return "No obligations extracted from changes."
        
        count = len(obligations)
        types = list(set(o.get("type") for o in obligations))
        critical = sum(1 for o in obligations if o.get("severity") == "CRITICAL")
        
        summary = f"Extracted {count} obligation(s) from {change_severity} regulatory changes. "
        summary += f"Types: {', '.join(types)}. "
        
        if critical > 0:
            summary += f"{critical} CRITICAL obligation(s) require immediate attention. "
        
        return summary
    
    def process_batch(self, change_analyses: List[Dict]) -> Dict:
        """
        Process batch of change analyses.
        
        Args:
            change_analyses: List from Agent 3
            
        Returns:
            Batch legal analysis
        """
        print(f"\n[INFO] Processing batch of {len(change_analyses)} change analyses...")
        
        results = []
        
        for analysis in change_analyses:
            try:
                legal_result = self.extract_obligations(analysis)
                results.append(legal_result)
            except Exception as e:
                print(f"[ERROR] Extraction failed for {analysis.get('snapshot_id')}: {e}")
                results.append({
                    "snapshot_id": analysis.get("snapshot_id"),
                    "error": str(e),
                    "hitl_required": True
                })
        
        # Aggregate stats
        total_obligations = sum(r.get("obligations_count", 0) for r in results)
        hitl_count = sum(1 for r in results if r.get("hitl_required", False))
        
        output = {
            "agent": "agent-4-legal-llm",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_snapshots": len(change_analyses),
            "total_obligations": total_obligations,
            "hitl_count": hitl_count,
            "legal_analyses": results
        }
        
        print(f"\n[SUCCESS] Batch processing complete:")
        print(f"  Total Snapshots: {output['total_snapshots']}")
        print(f"  Total Obligations: {total_obligations}")
        print(f"  HITL Required: {hitl_count}")
        
        return output
