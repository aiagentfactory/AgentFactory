"""
Data Cleaner for Data Factory
Handles PII removal, garbage filtering, and anomaly detection.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel
import re


class CleaningRule(BaseModel):
    """Data cleaning rule definition"""
    rule_id: str
    name: str
    pattern: str
    replacement: str = "[REDACTED]"
    enabled: bool = True


class DataCleaner:
    """Cleans and preprocesses data"""
    
    def __init__(self):
        # Default PII detection patterns
        self.pii_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        self.custom_rules: List[CleaningRule] = []
    
    def remove_pii(self, text: str) -> str:
        """
        Remove personally identifiable information from text.
        
        Args:
            text: Input text
            
        Returns:
            Sanitized text
        """
        cleaned = text
        for pii_type, pattern in self.pii_patterns.items():
            cleaned = re.sub(pattern, f"[{pii_type.upper()}]", cleaned)
        return cleaned
    
    def filter_garbage(self, text: str, min_length: int = 10) -> bool:
        """
        Check if text is garbage (too short, nonsensical, etc.)
        
        Args:
            text: Input text
            min_length: Minimum acceptable length
            
        Returns:
            True if text should be filtered out
        """
        if len(text.strip()) < min_length:
            return True
        
        # Check for excessive special characters
        special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
        if special_chars / len(text) > 0.5:
            return True
        
        return False
    
    def detect_anomalies(self, texts: List[str]) -> List[int]:
        """
        Detect anomalous texts in a batch.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Indices of anomalous texts
        """
        anomalies = []
        
        if not texts:
            return anomalies
        
        # Calculate average length
        avg_length = sum(len(t) for t in texts) / len(texts)
        
        for i, text in enumerate(texts):
            # Flag texts that are extremely different in length
            if len(text) > avg_length * 3 or len(text) < avg_length / 3:
                anomalies.append(i)
        
        return anomalies
    
    def cluster_similar(self, texts: List[str], threshold: float = 0.8) -> Dict[str, List[int]]:
        """
        Cluster similar texts together.
        
        Args:
            texts: List of texts to cluster
            threshold: Similarity threshold (0-1)
            
        Returns:
            Dictionary mapping cluster ID to text indices
        """
        # Simple clustering based on first words (mock implementation)
        clusters: Dict[str, List[int]] = {}
        
        for i, text in enumerate(texts):
            words = text.lower().split()
            if not words:
                continue
            
            # Use first 3 words as cluster key
            key = " ".join(words[:3])
            if key not in clusters:
                clusters[key] = []
            clusters[key].append(i)
        
        return clusters
    
    def add_custom_rule(self, rule: CleaningRule):
        """Add a custom cleaning rule"""
        self.custom_rules.append(rule)
    
    def apply_custom_rules(self, text: str) -> str:
        """
        Apply custom cleaning rules.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        cleaned = text
        for rule in self.custom_rules:
            if rule.enabled:
                cleaned = re.sub(rule.pattern, rule.replacement, cleaned)
        return cleaned
    
    def clean_text(self, text: str, remove_pii: bool = True) -> Optional[str]:
        """
        Full cleaning pipeline.
        
        Args:
            text: Input text
            remove_pii: Whether to remove PII
            
        Returns:
            Cleaned text, or None if filtered out
        """
        # Filter garbage
        if self.filter_garbage(text):
            return None
        
        # Remove PII
        cleaned = text
        if remove_pii:
            cleaned = self.remove_pii(cleaned)
        
        # Apply custom rules
        cleaned = self.apply_custom_rules(cleaned)
        
        return cleaned
