"""
Main Orchestrator
Coordinates all agents to provide recipe suggestions.
"""

from typing import Dict, Optional
from agents.preference_classifier import PreferenceClassifierAgent
from agents.context_detector import ContextDetectorAgent
from agents.meal_type_determiner import MealTypeDeterminerAgent
from agents.cuisine_mapper import CuisineMapperAgent
from agents.food_selector import FoodSelectorAgent
from agents.recipe_generator import RecipeGeneratorAgent
from agents.llm_client import LLMClient

from dotenv import load_dotenv
load_dotenv()   


class RecipeOrchestrator:
    """Main orchestrator that coordinates all agents."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the orchestrator with all agents.
        
        Args:
            api_key: Optional API key for LLM services
        """
        # Initialize a single LLM client (handles round-robin and rate limits internally)
        self.llm_client = LLMClient(api_key=api_key)
        
        # Initialize agents
        self.preference_classifier = PreferenceClassifierAgent(self.llm_client)
        self.context_detector = ContextDetectorAgent()
        self.meal_type_determiner = MealTypeDeterminerAgent()
        self.recipe_generator = RecipeGeneratorAgent(self.llm_client)
    
    def suggest_recipe(self, user_input: str, location_override: Optional[str] = None) -> Dict[str, any]:
        """
        Main method to suggest a recipe based on user input.
        
        Args:
            user_input: User's text describing preferences
            location_override: Optional location override (city, country)
            
        Returns:
            Complete recipe suggestion with all context
        """
        print("Multi-Agent Recipe Suggestion System")
        print("=" * 50)
        
        # Step 1: Classify user preferences
        print("\n[Agent 1] Classifying user preferences...")
        preferences = self.preference_classifier.classify_preferences(user_input)
        print(f"[OK] Detected preferences: {', '.join(preferences.get('detected_preferences', []))}")
        
        # Step 2: Detect context (time and location)
        print("\n[Agent 2] Detecting user context...")
        context = self.context_detector.detect_context()
        if location_override:
            context["location"] = self.context_detector.get_location_by_input(location_override)
        print(f"[OK] Time: {context['time']['hour']}:{context['time']['minute']:02d}")
        print(f"[OK] Location: {context['location'].get('city', 'Unknown')}, {context['location'].get('country', 'Unknown')}")
        
        # Step 3: Determine meal type
        print("\n[Agent 3] Determining meal type...")
        meal_type = self.meal_type_determiner.determine_from_time_info(context["time"])
        print(f"[OK] Meal type: {meal_type['meal_type']}")
        
        # Step 4-6: Generate Cuisines, Dish, and Recipe in ONE call
        print("\n[Agent 4, 5, 6] Generating Cuisines, Dish, and Recipe (Combined LLM Call)...")
        combined_result = self.recipe_generator.generate_all_in_one(preferences, context["location"], meal_type)
        
        cuisines = combined_result.get("cuisines", {})
        dish_info = combined_result.get("dish_info", {})
        recipe = combined_result.get("recipe", {})
        
        print(f"[OK] Primary cuisines: {', '.join(cuisines.get('primary_cuisines', []))}")
        print(f"[OK] Selected dish: {dish_info.get('dish_name', 'Unknown')}")
        print("[OK] Recipe generated successfully!")
        
        # Compile final result
        dish_name = recipe.get("dish_name", "Unknown")
        import urllib.parse
        search_query = f"how to make {dish_name}"
        youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
        
        result = {
            "user_input": user_input,
            "preferences": preferences,
            "context": context,
            "meal_type": meal_type,
            "cuisines": cuisines,
            "selected_dish": dish_info,
            "recipe": recipe,
            "youtube_url": youtube_url,
            "summary": {
                "dish": recipe.get("dish_name", "Unknown"),
                "cuisine": dish_info.get("cuisine", "Unknown"),
                "meal_type": meal_type.get("meal_type", "Unknown"),
                "dietary_type": preferences.get("dietary_type", "Unknown"),
                "prep_time": recipe.get("prep_time", "Unknown"),
                "cook_time": recipe.get("cook_time", "Unknown")
            }
        }
        
        return result
    
    def format_output(self, result: Dict[str, any]) -> str:
        """
        Format the result for display.
        
        Args:
            result: Result dictionary from suggest_recipe
            
        Returns:
            Formatted string output
        """
        recipe = result["recipe"]
        summary = result["summary"]
        
        output = []
        output.append("\n" + "=" * 60)
        output.append("RECIPE SUGGESTION")
        output.append("=" * 60)
        output.append(f"\nDish: {summary['dish']}")
        output.append(f"Cuisine: {summary['cuisine']}")
        output.append(f"Meal Type: {summary['meal_type'].title()}")
        output.append(f"Dietary: {summary['dietary_type'].title()}")
        output.append(f"Prep Time: {summary['prep_time']} min | Cook Time: {summary['cook_time']} min")
        output.append(f"Servings: {recipe.get('servings', 'N/A')}")
        
        output.append("\n" + "-" * 60)
        output.append("Description")
        output.append("-" * 60)
        output.append(recipe.get("description", "No description available."))
        
        output.append("\n" + "-" * 60)
        output.append("Ingredients")
        output.append("-" * 60)
        for ingredient in recipe.get("ingredients", []):
            name = ingredient.get("name", "Unknown")
            quantity = ingredient.get("quantity", "")
            unit = ingredient.get("unit", "")
            output.append(f"  - {quantity} {unit} {name}")
        
        output.append("\n" + "-" * 60)
        output.append("Instructions")
        output.append("-" * 60)
        for i, instruction in enumerate(recipe.get("instructions", []), 1):
            output.append(f"\n{i}. {instruction}")
        
        if recipe.get("tips"):
            output.append("\n" + "-" * 60)
            output.append("Tips")
            output.append("-" * 60)
            for tip in recipe["tips"]:
                output.append(f"  - {tip}")
        
        if recipe.get("nutrition_info"):
            output.append("\n" + "-" * 60)
            output.append("Nutrition (per serving)")
            output.append("-" * 60)
            nutrition = recipe["nutrition_info"]
            output.append(f"  Calories: {nutrition.get('calories', 'N/A')}")
            output.append(f"  Protein: {nutrition.get('protein', 'N/A')}")
            output.append(f"  Carbs: {nutrition.get('carbs', 'N/A')}")
            output.append(f"  Fat: {nutrition.get('fat', 'N/A')}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)

