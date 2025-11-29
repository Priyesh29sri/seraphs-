"""
Agent 3: Diff & Change Classifier
Main agent logic for detecting and classifying changes.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from agents.agent_3_diff import tools


class DiffAgent:
    """
    Agent 3: Diff & Change Classifier
    
    Analyzes changes between document versions and classifies significance.
    """
    
    def __init__(self):
        self.version_history = {}  # Store previous versions (in-memory for MVP)
        print("[INFO] Agent 3 initialized (Diff & Change Classifier)")
    
    def analyze_changes(self, snapshot: Dict, previous_snapshot: Optional[Dict] = None) -> Dict:
        """
        Analyze changes in a snapshot compared to previous version.
        
        Args:
            snapshot: Current snapshot (from Agent 2)
            previous_snapshot: Previous version (None for first fetch)
            
        Returns:
            Change analysis result
        """
        snapshot_id = snapshot.get("snapshot_id")
        source = snapshot.get("source", "unknown")
        
        print(f"\n[INFO] Analyzing changes: {snapshot_id}")
        print(f"  Source: {source}")
        
        # If no previous version, mark as first fetch
        if previous_snapshot is None:
            print("  Status: FIRST FETCH (no comparison)")
            
            return {
                "snapshot_id": snapshot_id,
                "change_detected": False,
                "is_first_fetch": True,
                "severity": "NONE",
                "change_types": ["first_fetch"],
                "summary": "First fetch of this regulatory source. No previous version to compare.",
                "analyzed_at": datetime.utcnow().isoformat() + "Z"
            }
        
        # Get text content
        current_text = snapshot.get("text", "")
        previous_text = previous_snapshot.get("text", "")
        
        current_hash = snapshot.get("sha256", "")
        previous_hash = previous_snapshot.get("sha256", "")
        
        # Quick check: identical hashes = no change
        if current_hash == previous_hash:
            print("  Status: NO CHANGE (identical hash)")
            
            return {
                "snapshot_id": snapshot_id,
                "change_detected": False,
                "is_first_fetch": False,
                "severity": "NONE",
                "change_types": ["no_change"],
                "summary": "Content unchanged from previous version.",
                "analyzed_at": datetime.utcnow().isoformat() + "Z"
            }
        
        # Perform diff analysis
        print("  Status: CHANGES DETECTED - analyzing...")
        
        # Text diff
        diff_result = tools.text_diff(previous_text, current_text)
        
        # Structural diff (if HTML available)
        structural_diff = {"has_structural_change": False}
        # Note: Would need raw_html from snapshot for full structural diff
        
        # Semantic similarity
        similarity = tools.semantic_similarity(previous_text, current_text)
        
        # Classify severity
        severity = tools.classify_change_severity(diff_result, similarity)
        
        # Classify change types
        change_types = tools.classify_change_type(diff_result, structural_diff)
        
        # Extract changed sections
        changed_sections = tools.extract_changed_sections(
            previous_text,
            current_text,
            context_lines=2
        )
        
        # Detect new obligations
        new_obligations = tools.detect_new_obligations(previous_text, current_text)
        
        # Generate summary
        summary = tools.generate_change_summary(diff_result, severity, change_types)
        
        # Compute change hash
        change_hash = tools.compute_change_hash(previous_hash, current_hash)
        
        # Determine if HITL required
        hitl_required = severity in ["CRITICAL", "MAJOR"] or len(new_obligations) > 0
        
        result = {
            "snapshot_id": snapshot_id,
            "change_detected": True,
            "is_first_fetch": False,
            "severity": severity,
            "change_types": change_types,
            "diff_stats": {
                "similarity_ratio": diff_result["similarity_ratio"],
                "added_lines": diff_result["added_lines"],
                "removed_lines": diff_result["removed_lines"],
                "total_changes": diff_result["total_changes"]
            },
            "semantic_similarity": similarity,
            "changed_sections_count": len(changed_sections),
            "new_obligations_detected": len(new_obligations),
            "new_obligations": new_obligations,
            "change_hash": change_hash,
            "summary": summary,
            "hitl_required": hitl_required,
            "analyzed_at": datetime.utcnow().isoformat() + "Z"
        }
        
        print(f"  Severity: {severity}")
        print(f"  Changes: +{diff_result['added_lines']} / -{diff_result['removed_lines']} lines")
        print(f"  Similarity: {similarity:.1%}")
        print(f"  New Obligations: {len(new_obligations)}")
        print(f"  HITL Required: {hitl_required}")
        
        return result
    
    def analyze_batch(
        self,
        current_snapshots: List[Dict],
        previous_snapshots: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Analyze changes for a batch of snapshots.
        
        Args:
            current_snapshots: List of current snapshots (from Agent 2)
            previous_snapshots: List of previous snapshots (None for first run)
            
        Returns:
            Batch analysis result
        """
        print(f"\n[INFO] Analyzing batch of {len(current_snapshots)} snapshots...")
        
        # Build lookup for previous snapshots by source
        previous_by_source = {}
        if previous_snapshots:
            for snap in previous_snapshots:
                source = snap.get("source")
                if source:
                    previous_by_source[source] = snap
        
        results = []
        
        for current_snap in current_snapshots:
            try:
                source = current_snap.get("source")
                previous_snap = previous_by_source.get(source)
                
                analysis = self.analyze_changes(current_snap, previous_snap)
                results.append(analysis)
                
            except Exception as e:
                print(f"[ERROR] Analysis failed for {current_snap.get('snapshot_id')}: {e}")
                results.append({
                    "snapshot_id": current_snap.get("snapshot_id"),
                    "error": str(e),
                    "hitl_required": True
                })
        
        # Aggregate statistics
        total_changes = sum(1 for r in results if r.get("change_detected", False))
        critical_changes = sum(1 for r in results if r.get("severity") == "CRITICAL")
        major_changes = sum(1 for r in results if r.get("severity") == "MAJOR")
        hitl_count = sum(1 for r in results if r.get("hitl_required", False))
        
        output = {
            "agent": "agent-3-diff-classifier",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_snapshots": len(current_snapshots),
            "changes_detected": total_changes,
            "severity_breakdown": {
                "critical": critical_changes,
                "major": major_changes,
                "minor": len(results) - critical_changes - major_changes
            },
            "hitl_count": hitl_count,
            "analyses": results
        }
        
        print(f"\n[SUCCESS] Batch analysis complete:")
        print(f"  Total: {output['total_snapshots']}")
        print(f"  Changes: {total_changes}")
        print(f"  Critical: {critical_changes}, Major: {major_changes}")
        print(f"  HITL Required: {hitl_count}")
        
        return output
