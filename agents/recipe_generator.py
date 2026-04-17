"""
Recipe Generation Agent
Generates a simple recipe including ingredients and preparation steps.
"""

from typing import Dict, List
import json


class RecipeGeneratorAgent:
    """Agent responsible for generating recipes."""
    
    def __init__(self, llm_client):
        """
        Initialize the recipe generator agent.
        
        Args:
            llm_client: LLM client for recipe generation
        """
        self.llm_client = llm_client
    
    def generate_all_in_one(self, preferences: Dict, location: Dict, meal_type: Dict) -> Dict[str, any]:
        """
        Generate cuisines, select dish, and generate recipe in a single LLM call.
        """
        prompt = f"""Based on the following user context, suggest cuisines, pick a specific dish, and provide a full recipe.

User Preferences: {json.dumps(preferences)}
Location Context: {json.dumps(location)}
Meal Type: {json.dumps(meal_type)}

Tasks:
1. Suggest appropriate cuisines based on location and preferences.
2. Select the most suitable dish.
3. Provide a full detailed recipe.

Return ONLY a JSON object with this exact structure:
{{
    "cuisines": {{
        "primary_cuisines": ["cuisine1", "cuisine2"]
    }},
    "dish_info": {{
        "dish_name": "Name of the dish",
        "cuisine": "Primary cuisine",
        "meal_type": "Breakfast/Lunch/Dinner/Snack",
        "dietary_type": "Vegetarian/Non-veg/etc",
        "taste_profile": "Spicy/Sweet/etc",
        "difficulty": "Easy/Medium/Hard",
        "prep_time": "30"
    }},
    "recipe": {{
        "dish_name": "Name of the dish",
        "description": "Brief description",
        "prep_time": "30",
        "cook_time": "45",
        "servings": "4",
        "ingredients": [
            {{"name": "ingredient name", "quantity": "amount", "unit": "unit"}}
        ],
        "instructions": [
            "Step 1: ...",
            "Step 2: ..."
        ],
        "tips": ["tip 1", "tip 2"],
        "nutrition_info": {{
            "calories": "500",
            "protein": "20g",
            "carbs": "50g",
            "fat": "15g"
        }}
    }}
}}
"""
        try:
            response = self.llm_client.generate(prompt, max_tokens=3000)
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            result = json.loads(cleaned_response)
            if not result.get("recipe") or not result.get("dish_info"):
                raise ValueError("Missing required fields in response")
            return result
        except Exception as e:
            print(f"Combined generation error: {e}, using fallback")
            # Create dummy cuisines and dish_info to pass to fallback
            dish_info = {"dish_name": "Vegetable Stir Fry", "cuisine": "Asian", "meal_type": meal_type.get("meal_type", "dinner"), "dietary_type": "vegetarian", "taste_profile": "savory"}
            recipe = self._fallback_recipe(dish_info)
            return {
                "cuisines": {"primary_cuisines": ["Asian", "International"]},
                "dish_info": dish_info,
                "recipe": recipe
            }

    def generate_recipe(self, dish_info: Dict, preferences: Dict = None) -> Dict[str, any]:
        """Generate a fallback recipe template."""
        dish_name = dish_info.get("dish_name", "Delicious Dish")
        cuisine = dish_info.get("cuisine", "International")
        meal_type = dish_info.get("meal_type", "meal")
        dietary = dish_info.get("dietary_type", "none")
        taste = dish_info.get("taste_profile", "balanced")
        
        # Enhanced fallback recipes based on dish type
        if "biryani" in dish_name.lower():
            return {
                "dish_name": dish_name,
                "description": f"A fragrant and flavorful {cuisine} rice dish with mixed vegetables and aromatic spices.",
                "prep_time": "20",
                "cook_time": "45",
                "servings": "4",
                "ingredients": [
                    {"name": "Basmati rice", "quantity": "2", "unit": "cups"},
                    {"name": "Mixed vegetables (carrots, beans, peas)", "quantity": "2", "unit": "cups"},
                    {"name": "Onions", "quantity": "2", "unit": "medium"},
                    {"name": "Ginger-garlic paste", "quantity": "1", "unit": "tbsp"},
                    {"name": "Biryani masala", "quantity": "2", "unit": "tsp"},
                    {"name": "Turmeric", "quantity": "1", "unit": "tsp"},
                    {"name": "Ghee or oil", "quantity": "3", "unit": "tbsp"},
                    {"name": "Yogurt", "quantity": "1/2", "unit": "cup"},
                    {"name": "Mint leaves", "quantity": "1/4", "unit": "cup"},
                    {"name": "Coriander leaves", "quantity": "1/4", "unit": "cup"},
                    {"name": "Salt", "quantity": "to taste", "unit": ""}
                ],
                "instructions": [
                    "Wash and soak basmati rice for 30 minutes, then parboil with whole spices.",
                    "Heat ghee/oil in a pan and sauté sliced onions until golden brown.",
                    "Add ginger-garlic paste and cook until fragrant.",
                    "Add mixed vegetables and cook for 5 minutes.",
                    "Add biryani masala, turmeric, and salt. Mix well.",
                    "Add yogurt and cook for 2-3 minutes.",
                    "Layer the parboiled rice over the vegetables.",
                    "Add mint and coriander leaves on top.",
                    "Cover and cook on low heat for 20-25 minutes (dum cooking).",
                    "Let it rest for 10 minutes, then fluff and serve hot."
                ],
                "tips": [
                    "Use aged basmati rice for best results",
                    "Don't skip the dum cooking step for authentic flavor",
                    "Serve with raita and pickle"
                ],
                "nutrition_info": {
                    "calories": "~450 per serving",
                    "protein": "12g",
                    "carbs": "75g",
                    "fat": "12g"
                }
            }
        
        # Generic fallback
        return {
            "dish_name": dish_name,
            "description": f"A delicious {cuisine} {meal_type} with {taste} flavors, perfect for {dietary} diets.",
            "prep_time": dish_info.get("prep_time", "30"),
            "cook_time": "20",
            "servings": "2-3",
            "ingredients": [
                {"name": "Main vegetables", "quantity": "2", "unit": "cups"},
                {"name": "Onions", "quantity": "1", "unit": "medium"},
                {"name": "Garlic", "quantity": "3", "unit": "cloves"},
                {"name": "Spices", "quantity": "1", "unit": "tbsp"},
                {"name": "Oil", "quantity": "2", "unit": "tbsp"},
                {"name": "Salt", "quantity": "to taste", "unit": ""}
            ],
            "instructions": [
                "Prepare all ingredients: chop vegetables and mince garlic.",
                "Heat oil in a pan over medium heat.",
                "Add onions and cook until translucent.",
                "Add garlic and cook for 1 minute.",
                "Add vegetables and cook for 5-7 minutes.",
                "Add spices and salt, mix well.",
                "Cook until vegetables are tender but still crisp.",
                "Serve hot with rice or bread."
            ],
            "tips": [
                "Adjust spices according to taste",
                "Serve immediately for best flavor",
                "You can add your favorite vegetables"
            ],
            "nutrition_info": {
                "calories": "~300",
                "protein": "15g",
                "carbs": "30g",
                "fat": "10g"
            }
        }

