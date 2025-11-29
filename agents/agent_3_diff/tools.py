"""
Agent 3: Diff & Change Classifier
Tools for detecting and classifying changes in regulatory content.
"""

import hashlib
import difflib
from typing import Dict, List, Tuple
from datetime import datetime


# =============================================================================
# TOOL 1: section_chunk
# =============================================================================

def section_chunk(text: str, chunk_size: int = 500) -> List[str]:
    """
    Split text into semantic chunks for comparison.
    
    Args:
        text: Text to chunk
        chunk_size: Target size of each chunk
        
    Returns:
        List of text chunks
    """
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    print(f"[INFO] Created {len(chunks)} chunks from text")
    return chunks


# =============================================================================
# TOOL 2: structural_diff_html
# =============================================================================

def structural_diff_html(old_html: str, new_html: str) -> Dict:
    """
    Compare HTML structure (tags, hierarchy).
    
    For MVP: Simple line-based diff.
    Production: Parse DOM trees and compare structure.
    
    Args:
        old_html: Previous HTML
        new_html: Current HTML
        
    Returns:
        Structural diff result
    """
    from bs4 import BeautifulSoup
    
    print("[INFO] Computing structural diff...")
    
    # Parse HTML
    old_soup = BeautifulSoup(old_html, 'html.parser')
    new_soup = BeautifulSoup(new_html, 'html.parser')
    
    # Count tags
    old_tags = [tag.name for tag in old_soup.find_all()]
    new_tags = [tag.name for tag in new_soup.find_all()]
    
    # Compare tag counts
    from collections import Counter
    old_counts = Counter(old_tags)
    new_counts = Counter(new_tags)
    
    # Find differences
    added_tags = {tag: count for tag, count in new_counts.items() 
                  if count > old_counts.get(tag, 0)}
    removed_tags = {tag: count for tag, count in old_counts.items() 
                    if count > new_counts.get(tag, 0)}
    
    has_structural_change = bool(added_tags or removed_tags)
    
    return {
        "has_structural_change": has_structural_change,
        "added_tags": added_tags,
        "removed_tags": removed_tags,
        "old_tag_count": len(old_tags),
        "new_tag_count": len(new_tags)
    }


# =============================================================================
# TOOL 3: text_diff
# =============================================================================

def text_diff(old_text: str, new_text: str) -> Dict:
    """
    Compute line-by-line text diff.
    
    Args:
        old_text: Previous text
        new_text: Current text
        
    Returns:
        Diff result with added/removed lines
    """
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    
    # Use difflib to get diff
    diff = list(difflib.unified_diff(
        old_lines,
        new_lines,
        lineterm='',
        n=0  # No context lines
    ))
    
    # Count changes
    added_lines = [line for line in diff if line.startswith('+') and not line.startswith('+++')]
    removed_lines = [line for line in diff if line.startswith('-') and not line.startswith('---')]
    
    # Calculate similarity ratio
    similarity = difflib.SequenceMatcher(None, old_text, new_text).ratio()
    
    return {
        "similarity_ratio": round(similarity, 3),
        "added_lines": len(added_lines),
        "removed_lines": len(removed_lines),
        "total_changes": len(added_lines) + len(removed_lines),
        "sample_added": added_lines[:3] if added_lines else [],
        "sample_removed": removed_lines[:3] if removed_lines else []
    }


# =============================================================================
# TOOL 4: semantic_similarity (Simplified)
# =============================================================================

def semantic_similarity(text1: str, text2: str) -> float:
    """
    Compute semantic similarity between two texts.
    
    Uses sentence transformers if available, falls back to Jaccard.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score 0.0-1.0
    """
    try:
        # Try to use enhanced semantic similarity engine
        from utils.semantic_similarity import semantic_similarity as enhanced_sim
        return enhanced_sim(text1, text2)
    except ImportError:
        # Fallback to simple Jaccard similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union) if union else 0.0
        
        return round(similarity, 3)


# =============================================================================
# TOOL 5: classify_change_severity
# =============================================================================

def classify_change_severity(diff_result: Dict, similarity: float) -> str:
    """
    Classify severity of changes.
    
    Levels:
    - CRITICAL: Major structural changes, low similarity
    - MAJOR: Significant content changes
    - MINOR: Small tweaks, high similarity
    - NONE: No meaningful changes
    
    Args:
        diff_result: Result from text_diff()
        similarity: Similarity ratio
        
    Returns:
        Severity level
    """
    total_changes = diff_result.get("total_changes", 0)
    
    if similarity > 0.98:
        return "NONE"
    elif similarity > 0.90 and total_changes < 10:
        return "MINOR"
    elif similarity > 0.70 or total_changes < 50:
        return "MAJOR"
    else:
        return "CRITICAL"


# =============================================================================
# TOOL 6: extract_changed_sections
# =============================================================================

def extract_changed_sections(old_text: str, new_text: str, context_lines: int = 2) -> List[Dict]:
    """
    Extract sections that changed with context.
    
    Args:
        old_text: Previous text
        new_text: Current text
        context_lines: Lines of context around changes
        
    Returns:
        List of changed sections
    """
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    
    differ = difflib.Differ()
    diff = list(differ.compare(old_lines, new_lines))
    
    # Find change locations
    changes = []
    i = 0
    while i < len(diff):
        line = diff[i]
        if line.startswith('+ ') or line.startswith('- '):
            # Found a change
            start = max(0, i - context_lines)
            end = min(len(diff), i + context_lines + 1)
            
            change_context = diff[start:end]
            changes.append({
                "location": i,
                "context": [l[2:] for l in change_context if not l.startswith('?')]
            })
        i += 1
    
    print(f"[INFO] Found {len(changes)} changed sections")
    return changes[:10]  # Return top 10


# =============================================================================
# TOOL 7: detect_new_obligations
# =============================================================================

def detect_new_obligations(old_text: str, new_text: str) -> List[str]:
    """
    Detect new regulatory obligations in text.
    
    Looks for keywords like "must", "shall", "required", etc.
    Production: Use LLM to extract obligations.
    
    Args:
        old_text: Previous text
        new_text: Current text
        
    Returns:
        List of potential new obligations
    """
    obligation_keywords = ['must', 'shall', 'required', 'mandatory', 'obligated']
    
    old_lines = set(old_text.lower().splitlines())
    new_lines = set(new_text.lower().splitlines())
    
    # Find new lines with obligation keywords
    new_obligations = []
    for line in (new_lines - old_lines):
        if any(keyword in line for keyword in obligation_keywords):
            new_obligations.append(line.strip())
    
    print(f"[INFO] Detected {len(new_obligations)} potential new obligations")
    return new_obligations[:5]  # Top 5


# =============================================================================
# TOOL 8: compute_change_hash
# =============================================================================

def compute_change_hash(old_hash: str, new_hash: str) -> str:
    """
    Compute hash representing the change itself.
    
    Args:
        old_hash: Hash of old content
        new_hash: Hash of new content
        
    Returns:
        Change hash
    """
    change_data = f"{old_hash}:{new_hash}"
    change_hash = hashlib.sha256(change_data.encode()).hexdigest()
    
    return change_hash


# =============================================================================
# TOOL 9: classify_change_type
# =============================================================================

def classify_change_type(diff_result: Dict, structural_diff: Dict) -> List[str]:
    """
    Classify type of change.
    
    Types:
    - content: Text content changed
    - structure: HTML structure changed
    - formatting: Only formatting changed
    - metadata: Metadata changed
    
    Args:
        diff_result: Text diff result
        structural_diff: Structural diff result
        
    Returns:
        List of change types
    """
    types = []
    
    if diff_result["total_changes"] > 0:
        types.append("content")
    
    if structural_diff.get("has_structural_change", False):
        types.append("structure")
    
    # Simple heuristic for formatting
    if diff_result["total_changes"] < 5 and diff_result["similarity_ratio"] > 0.95:
        types.append("formatting")
    
    return types if types else ["no_change"]


# =============================================================================
# TOOL 10: generate_change_summary
# =============================================================================

def generate_change_summary(diff_result: Dict, severity: str, change_types: List[str]) -> str:
    """
    Generate human-readable change summary.
    
    Production: Use LLM to generate summary.
    
    Args:
        diff_result: Diff result
        severity: Severity level
        change_types: List of change types
        
    Returns:
        Summary text
    """
    summary_parts = []
    
    # Severity
    summary_parts.append(f"{severity} changes detected.")
    
    # Changes
    if diff_result["added_lines"] > 0:
        summary_parts.append(f"{diff_result['added_lines']} lines added.")
    if diff_result["removed_lines"] > 0:
        summary_parts.append(f"{diff_result['removed_lines']} lines removed.")
    
    # Types
    type_str = ", ".join(change_types)
    summary_parts.append(f"Change types: {type_str}.")
    
    # Similarity
    summary_parts.append(f"Similarity to previous version: {diff_result['similarity_ratio']*100:.1f}%.")
    
    return " ".join(summary_parts)
