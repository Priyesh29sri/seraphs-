"""
Enhanced semantic similarity using sentence transformers.
Production-ready implementation with caching and optimization.
"""

import hashlib
from typing import List, Tuple
import numpy as np

# Try to import sentence transformers, fall back to Jaccard if not available
try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[WARNING] sentence-transformers not installed. Using Jaccard similarity.")
    print("[INFO] Install with: pip install sentence-transformers torch")


class SemanticSimilarityEngine:
    """
    Production semantic similarity engine using sentence embeddings.
    
    Features:
    - Sentence transformers for semantic understanding
    - Embedding caching for performance
    - Fallback to Jaccard similarity
    - Batch processing support
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize similarity engine.
        
        Args:
            model_name: HuggingFace model name (default: fast 384-dim model)
        """
        self.model_name = model_name
        self.embedding_cache = {}
        
        if TRANSFORMERS_AVAILABLE:
            print(f"[INFO] Loading sentence transformer model: {model_name}")
            self.model = SentenceTransformer(model_name)
            print(f"[SUCCESS] Model loaded (embedding dim: {self.model.get_sentence_embedding_dimension()})")
        else:
            self.model = None
            print("[INFO] Using Jaccard similarity (word overlap)")
    
    def compute_embedding(self, text: str) -> np.ndarray:
        """
        Compute embedding for text with caching.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        # Check cache
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        if text_hash in self.embedding_cache:
            return self.embedding_cache[text_hash]
        
        # Compute embedding
        if self.model:
            embedding = self.model.encode(text, convert_to_numpy=True)
        else:
            # Fallback: use simple word count vector (very basic)
            embedding = self._simple_embedding(text)
        
        # Cache
        self.embedding_cache[text_hash] = embedding
        
        return embedding
    
    def _simple_embedding(self, text: str) -> np.ndarray:
        """Fallback: simple word-count based embedding"""
        words = text.lower().split()
        # Use character codes as basic features
        features = []
        for word in words[:100]:  # Limit to 100 words
            features.extend([ord(c) for c in word[:10]])  # First 10 chars
        
        # Pad to fixed size
        while len(features) < 1000:
            features.append(0)
        
        return np.array(features[:1000], dtype=float)
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score 0.0-1.0
        """
        if TRANSFORMERS_AVAILABLE and self.model:
            # Use sentence transformers
            emb1 = self.compute_embedding(text1)
            emb2 = self.compute_embedding(text2)
            
            # Cosine similarity
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            
            # Normalize to 0-1 range
            return float((similarity + 1) / 2)
        
        else:
            # Fallback: Jaccard similarity (word overlap)
            return self._jaccard_similarity(text1, text2)
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """Fallback Jaccard similarity for word overlap"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def batch_similarity(self, text_pairs: List[Tuple[str, str]]) -> List[float]:
        """
        Compute similarities for multiple text pairs efficiently.
        
        Args:
            text_pairs: List of (text1, text2) tuples
            
        Returns:
            List of similarity scores
        """
        results = []
        
        for text1, text2 in text_pairs:
            sim = self.semantic_similarity(text1, text2)
            results.append(sim)
        
        return results
    
    def find_most_similar(self, query: str, candidates: List[str], top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Find most similar texts from candidates.
        
        Args:
            query: Query text
            candidates: List of candidate texts
            top_k: Number of top results to return
            
        Returns:
            List of (index, similarity_score) tuples
        """
        query_emb = self.compute_embedding(query)
        
        similarities = []
        for i, candidate in enumerate(candidates):
            cand_emb = self.compute_embedding(candidate)
            
            # Cosine similarity
            if self.model:
                sim = np.dot(query_emb, cand_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(cand_emb))
                sim = (sim + 1) / 2  # Normalize to 0-1
            else:
                sim = self._jaccard_similarity(query, candidate)
            
            similarities.append((i, float(sim)))
        
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def clear_cache(self):
        """Clear embedding cache"""
        self.embedding_cache.clear()
        print("[INFO] Embedding cache cleared")
    
    def get_cache_size(self) -> int:
        """Get number of cached embeddings"""
        return len(self.embedding_cache)


# Global instance (singleton)
_engine = None

def get_similarity_engine() -> SemanticSimilarityEngine:
    """Get global similarity engine instance"""
    global _engine
    if _engine is None:
        _engine = SemanticSimilarityEngine()
    return _engine


# Convenience functions
def semantic_similarity(text1: str, text2: str) -> float:
    """
    Compute semantic similarity (convenience function).
    
    Args:
        text1, text2: Texts to compare
        
    Returns:
        Similarity score 0.0-1.0
    """
    engine = get_similarity_engine()
    return engine.semantic_similarity(text1, text2)


def find_similar_documents(query: str, documents: List[str], top_k: int = 5) -> List[Tuple[int, float]]:
    """
    Find most similar documents to query.
    
    Args:
        query: Query text
        documents: List of candidate documents
        top_k: Number of results
        
    Returns:
        List of (document_index, similarity_score)
    """
    engine = get_similarity_engine()
    return engine.find_most_similar(query, documents, top_k)
