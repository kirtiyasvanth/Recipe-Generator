"""
Preference Classification Agent
Classifies user food preferences from text input.
"""

from typing import Dict, List
import json


class PreferenceClassifierAgent:
    """Agent responsible for classifying user food preferences from text."""
    
    def __init__(self, llm_client):
        """
        Initialize the preference classifier agent.
        
        Args:
            llm_client: LLM client for text analysis
        """
        self.llm_client = llm_client
        self.preference_categories = [
            "spicy", "sweet", "sour", "bitter", "umami",
            "light", "heavy", "healthy", "comfort",
            "vegan", "vegetarian", "non-vegetarian",
            "gluten-free", "dairy-free", "low-carb", "high-protein"
        ]
    
    def classify_preferences(self, user_input: str) -> Dict[str, any]:
        """Classify food preferences from user text input using keyword matching."""
        return self._fallback_classification(user_input)
    
    def _fallback_classification(self, user_input: str) -> Dict[str, any]:
        """Fallback classification using keyword matching."""
        user_lower = user_input.lower()
        detected = []
        
        # Taste preferences
        if any(word in user_lower for word in ["spicy", "hot", "chili", "pepper"]):
            detected.append("spicy")
        if any(word in user_lower for word in ["sweet", "dessert", "sugar"]):
            detected.append("sweet")
        if any(word in user_lower for word in ["sour", "tangy", "citrus"]):
            detected.append("sour")
        
        # Dietary types
        if "vegan" in user_lower:
            detected.append("vegan")
        elif "vegetarian" in user_lower or "veg" in user_lower:
            detected.append("vegetarian")
        elif any(word in user_lower for word in ["meat", "chicken", "beef", "fish", "non-veg"]):
            detected.append("non-vegetarian")
        
        # Meal characteristics
        if any(word in user_lower for word in ["light", "simple", "easy"]):
            detected.append("light")
        if any(word in user_lower for word in ["healthy", "nutritious"]):
            detected.append("healthy")
        
        return {
            "detected_preferences": detected,
            "primary_taste": detected[0] if detected else None,
            "dietary_type": next((p for p in detected if p in ["vegan", "vegetarian", "non-vegetarian"]), None),
            "meal_characteristic": next((p for p in detected if p in ["light", "heavy", "healthy", "comfort"]), None),
            "confidence": 0.7 if detected else 0.3
        }

