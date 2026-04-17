"""
Food Selection Agent
Selects the most suitable dish based on preferences, meal type, and regional relevance.
"""

from typing import Dict, List
import json


class FoodSelectorAgent:
    """Agent responsible for selecting the most suitable dish."""
    
    def __init__(self, llm_client):
        """
        Initialize the food selector agent.
        
        Args:
            llm_client: LLM client for dish selection
        """
        self.llm_client = llm_client
    
    def select_dish(self, preferences: Dict, meal_type: Dict, cuisines: Dict) -> Dict[str, any]:
        """
        Select the most suitable dish based on all criteria.
        
        Args:
            preferences: User's food preferences
            meal_type: Determined meal type
            cuisines: Mapped cuisines for location
            
        Returns:
            Dictionary containing selected dish information
        """
        prompt = f"""Select the most suitable dish that matches all the following criteria:

User Preferences:
- Detected preferences: {', '.join(preferences.get('detected_preferences', []))}
- Primary taste: {preferences.get('primary_taste', 'none')}
- Dietary type: {preferences.get('dietary_type', 'none')}
- Meal characteristic: {preferences.get('meal_characteristic', 'none')}

Meal Type: {meal_type.get('meal_type', 'lunch')}

Available Cuisines: {', '.join(cuisines.get('primary_cuisines', []))}
Location: {cuisines.get('location', {}).get('city', 'Unknown')}

Select ONE dish that:
1. Matches the user's dietary preferences (vegan/vegetarian/non-vegetarian)
2. Fits the meal type (breakfast/lunch/dinner/snack)
3. Is from one of the available cuisines or a fusion
4. Matches taste preferences (spicy/sweet/etc.)
5. Matches meal characteristics (light/heavy/healthy)

Return a JSON object with:
{{
    "dish_name": "Name of the dish",
    "cuisine": "Cuisine type",
    "meal_type": "{meal_type.get('meal_type', 'lunch')}",
    "dietary_type": "{preferences.get('dietary_type', 'none')}",
    "taste_profile": "Description of taste",
    "reasoning": "Why this dish was selected",
    "difficulty": "easy/medium/hard",
    "prep_time": "estimated preparation time in minutes"
}}

Return only valid JSON, no additional text."""

        try:
            response = self.llm_client.generate(prompt)
            # Clean response - remove markdown code blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            result = json.loads(cleaned_response)
            # Validate result has required fields
            if not result.get("dish_name") or result.get("dish_name") == "Unknown":
                raise ValueError("Invalid dish name in response")
            return result
        except Exception as e:
            print(f"Food selection error: {e}, using fallback")
            return self._fallback_selection(preferences, meal_type, cuisines)
    
    def _fallback_selection(self, preferences: Dict, meal_type: Dict, cuisines: Dict) -> Dict[str, any]:
        """Fallback dish selection using rule-based approach."""
        dietary = preferences.get("dietary_type", "non-vegetarian")
        meal = meal_type.get("meal_type", "lunch")
        taste = preferences.get("primary_taste", "none")
        
        # Simple rule-based selection
        dish_map = {
            ("breakfast", "vegetarian"): "Vegetarian Breakfast Bowl",
            ("breakfast", "vegan"): "Vegan Smoothie Bowl",
            ("breakfast", "non-vegetarian"): "Scrambled Eggs with Toast",
            ("lunch", "vegetarian"): "Vegetable Curry",
            ("lunch", "vegan"): "Lentil Soup",
            ("lunch", "non-vegetarian"): "Grilled Chicken Salad",
            ("dinner", "vegetarian"): "Vegetable Biryani",
            ("dinner", "vegan"): "Tofu Stir Fry",
            ("dinner", "non-vegetarian"): "Herb-Crusted Salmon",
            ("snack", "vegetarian"): "Vegetable Spring Rolls",
            ("snack", "vegan"): "Hummus with Vegetables",
            ("snack", "non-vegetarian"): "Chicken Wings",
        }
        
        dish_name = dish_map.get((meal, dietary), "Mixed Vegetable Stir Fry")
        
        return {
            "dish_name": dish_name,
            "cuisine": cuisines.get("primary_cuisines", ["International"])[0],
            "meal_type": meal,
            "dietary_type": dietary,
            "taste_profile": f"{taste} flavored" if taste != "none" else "balanced",
            "reasoning": f"Selected based on {meal} meal type and {dietary} dietary preference",
            "difficulty": "medium",
            "prep_time": "30"
        }

