"""
LLM Client Wrapper
Provides a unified interface for LLM interactions.
"""

import os
import json
import time
from typing import Optional

# Global variables for rate limiting
LAST_CALL_TIME = 0
CALL_INTERVAL = 12  # 12 seconds between calls to respect free tier rate limits (5 RPM -> 12s)

class LLMClient:
    """Wrapper for LLM API interactions."""
    
    # Class level variable for round-robin
    _api_keys = []
    _key_index = 0
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-3.1-flash-lite-preview"):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key for LLM service
            model: Model name to use
        """
        # Load API keys from env if class keys are empty
        if not self._api_keys:
            from dotenv import load_dotenv
            load_dotenv()
            
            # Standardize on GEMINI_API_KEY as requested
            env_key = os.getenv("GEMINI_API_KEY")
            key = api_key or env_key
            
            if not key:
                raise ValueError("Missing GEMINI_API_KEY")
            
            self.__class__._api_keys = [key]
            
        self.model = model
        self._cache = {}
    
    def _get_next_client(self):
        """Get the next genai client in the round-robin."""
        if not self._api_keys:
            return None
            
        try:
            from google import genai
            
            # Round robin selection
            current_key = self._api_keys[self._key_index]
            self.__class__._key_index = (self._key_index + 1) % len(self._api_keys)
            
            return genai.Client(api_key=current_key)
        except ImportError:
            print("Warning: google-genai library not installed. Using mock responses.")
            return None
    
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        """
        Generate a response from the LLM.
        """
        if not self._api_keys:
            return self._mock_response(prompt)
            
        # 1. Check cache first
        if prompt in self._cache:
            return self._cache[prompt]
            
        try:
            from google.genai import types
            
            system_prompt = "You are a helpful food and recipe assistant. Always return valid JSON when requested."
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
            
            # 2. Add retry with delay logic and rate limit
            global LAST_CALL_TIME
            
            last_error = None
            # Use models confirmed to be available in this environment
            models_to_try = [self.model, "gemini-3-flash-preview", "gemini-2.5-flash-native-audio-latest"]
            
            for attempt in range(len(models_to_try)):
                current_model = models_to_try[attempt]
                try:
                    # Enforce rate limit across all instances
                    now = time.time()
                    time_since_last = now - LAST_CALL_TIME
                    if time_since_last < CALL_INTERVAL:
                        sleep_time = CALL_INTERVAL - time_since_last
                        print(f"[Rate Limit] Sleeping for {sleep_time:.2f}s...")
                        time.sleep(sleep_time)
                    
                    LAST_CALL_TIME = time.time()
                    
                    client = self._get_next_client()
                    if not client:
                        return self._mock_response(prompt)
                    
                    print(f"[LLM] Attempting with model: {current_model}...")
                    response = client.models.generate_content(
                        model=current_model,
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            max_output_tokens=max_tokens,
                            temperature=0.7,
                            response_mime_type="application/json"
                        )
                    )
                    
                    result_text = response.text.strip()
                    
                    # 3. Cache the successful result
                    self._cache[prompt] = result_text
                    
                    return result_text
                    
                except Exception as e:
                    last_error = e
                    error_str = str(e)
                    print(f"[Attempt {attempt+1}] Model {current_model} failed: {error_str[:100]}...")
                    
                    # If quota exhausted, sleep longer
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        print(f"[Rate Limit Error] Sleeping for 16s before retry...")
                        time.sleep(16)
                        LAST_CALL_TIME = time.time()
                    elif "404" in error_str:
                        print(f"[Not Found] Model {current_model} not available. Trying next model...")
                        continue # Try next model immediately
                    else:
                        time.sleep(2)
            
            # If all models failed
            raise last_error

        except Exception as e:
            print(f"[Warning] LLM API error after retries: {e}. Falling back to mock response.")
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> str:
        """Generate a mock response when LLM is not available."""
        prompt_lower = prompt.lower()
        
        # Match based on the main action requested in the prompt
        if "classify the preferences into these categories" in prompt_lower or "classify their food preferences" in prompt_lower:
            return json.dumps({
                "detected_preferences": ["spicy", "vegetarian"],
                "primary_taste": "spicy",
                "dietary_type": "vegetarian",
                "meal_characteristic": "light",
                "confidence": 0.8
            })
        
        elif "map the following location to relevant cuisines" in prompt_lower:
            return json.dumps({
                "primary_cuisines": ["Indian", "North Indian", "South Indian"],
                "all_cuisines": ["Indian", "North Indian", "South Indian", "Punjabi"],
                "reasoning": "Based on location, Indian cuisines are most relevant"
            })
        
        elif "select the most suitable dish" in prompt_lower:
            return json.dumps({
                "dish_name": "Vegetable Biryani",
                "cuisine": "Indian",
                "meal_type": "dinner",
                "dietary_type": "vegetarian",
                "taste_profile": "spicy and aromatic",
                "reasoning": "Matches vegetarian preference, dinner meal type, and Indian cuisine",
                "difficulty": "medium",
                "prep_time": "45"
            })
        
        elif "generate a detailed recipe" in prompt_lower:
            return json.dumps({
                "dish_name": "Vegetable Biryani",
                "description": "A fragrant and flavorful rice dish with mixed vegetables and aromatic spices.",
                "prep_time": "20",
                "cook_time": "45",
                "servings": "4",
                "ingredients": [
                    {"name": "Basmati rice", "quantity": "2", "unit": "cups"},
                    {"name": "Mixed vegetables", "quantity": "2", "unit": "cups"},
                    {"name": "Onions", "quantity": "2", "unit": "medium"},
                    {"name": "Ginger-garlic paste", "quantity": "1", "unit": "tbsp"},
                    {"name": "Biryani masala", "quantity": "2", "unit": "tsp"},
                    {"name": "Turmeric", "quantity": "1", "unit": "tsp"},
                    {"name": "Ghee", "quantity": "3", "unit": "tbsp"},
                    {"name": "Yogurt", "quantity": "1/2", "unit": "cup"},
                    {"name": "Mint leaves", "quantity": "1/4", "unit": "cup"},
                    {"name": "Coriander leaves", "quantity": "1/4", "unit": "cup"}
                ],
                "instructions": [
                    "Step 1: Wash and soak basmati rice for 30 minutes, then parboil with whole spices.",
                    "Step 2: Heat ghee in a pan and sauté sliced onions until golden brown.",
                    "Step 3: Add ginger-garlic paste and cook until fragrant.",
                    "Step 4: Add mixed vegetables and cook for 5 minutes.",
                    "Step 5: Add biryani masala, turmeric, and salt. Mix well.",
                    "Step 6: Add yogurt and cook for 2-3 minutes.",
                    "Step 7: Layer the parboiled rice over the vegetables.",
                    "Step 8: Add mint and coriander leaves on top.",
                    "Step 9: Cover and cook on low heat for 20-25 minutes (dum cooking).",
                    "Step 10: Let it rest for 10 minutes, then fluff and serve hot."
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
            })
        
        # Default response
        return json.dumps({"message": "Mock response", "status": "ok"})

