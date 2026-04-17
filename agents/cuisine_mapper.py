"""
Cuisine Mapping Agent
Maps user's location to relevant local cuisines.
"""

from typing import Dict, List
import json


class CuisineMapperAgent:
    """Agent responsible for mapping location to local cuisines."""
    
    def __init__(self, llm_client):
        """
        Initialize the cuisine mapper agent.
        
        Args:
            llm_client: LLM client for cuisine analysis
        """
        self.llm_client = llm_client
        self.cuisine_mapping = {
            "IN": ["Indian", "North Indian", "South Indian", "Punjabi", "Gujarati", "Bengali"],
            "CN": ["Chinese", "Sichuan", "Cantonese", "Hunan"],
            "IT": ["Italian", "Sicilian", "Tuscan", "Roman"],
            "JP": ["Japanese", "Sushi", "Ramen", "Teriyaki"],
            "TH": ["Thai", "Pad Thai", "Tom Yum", "Green Curry"],
            "MX": ["Mexican", "Tex-Mex", "Yucatecan"],
            "FR": ["French", "Provencal", "Normandy"],
            "US": ["American", "Southern", "Tex-Mex", "Californian"],
            "GB": ["British", "English", "Scottish"],
            "GR": ["Greek", "Mediterranean"],
            "TR": ["Turkish", "Mediterranean", "Middle Eastern"],
            "VN": ["Vietnamese", "Pho", "Banh Mi"],
            "KR": ["Korean", "Kimchi", "Bibimbap"],
            "ES": ["Spanish", "Tapas", "Paella"],
        }
    
    def map_location_to_cuisines(self, location_info: Dict) -> Dict[str, any]:
        """
        Map location to relevant local cuisines.
        
        Args:
            location_info: Dictionary containing location information
            
        Returns:
            Dictionary containing mapped cuisines
        """
        country_code = location_info.get("country_code", "US")
        city = location_info.get("city", "Unknown")
        region = location_info.get("region", "Unknown")
        
        # Get base cuisines from country code
        base_cuisines = self.cuisine_mapping.get(country_code, ["International", "Fusion"])
        
        # Use LLM for more nuanced mapping if available
        if self.llm_client:
            try:
                enhanced_cuisines = self._enhance_cuisine_mapping(location_info, base_cuisines)
                return enhanced_cuisines
            except Exception as e:
                print(f"LLM cuisine mapping error: {e}")
        
        return {
            "primary_cuisines": base_cuisines[:3],  # Top 3 cuisines
            "all_cuisines": base_cuisines,
            "location": {
                "city": city,
                "region": region,
                "country_code": country_code
            },
            "confidence": 0.8
        }
    
    def _enhance_cuisine_mapping(self, location_info: Dict, base_cuisines: List[str]) -> Dict[str, any]:
        """Enhance cuisine mapping using LLM."""
        prompt = f"""Based on the location information, suggest relevant local cuisines.

Location: {location_info.get('city')}, {location_info.get('region')}, {location_info.get('country_name', 'Unknown')}
Base cuisines: {', '.join(base_cuisines)}

Suggest 3-5 most relevant cuisines for this location, considering:
1. Traditional local cuisines
2. Popular regional dishes
3. Cultural food influences

Return a JSON object with:
{{
    "primary_cuisines": ["cuisine1", "cuisine2", "cuisine3"],
    "all_cuisines": ["cuisine1", "cuisine2", ...],
    "reasoning": "brief explanation"
}}

Return only valid JSON, no additional text."""

        try:
            response = self.llm_client.generate(prompt)
            result = json.loads(response.strip())
            result["location"] = {
                "city": location_info.get("city"),
                "region": location_info.get("region"),
                "country_code": location_info.get("country_code")
            }
            return result
        except Exception as e:
            # Fallback to base cuisines
            return {
                "primary_cuisines": base_cuisines[:3],
                "all_cuisines": base_cuisines,
                "location": {
                    "city": location_info.get("city"),
                    "region": location_info.get("region"),
                    "country_code": location_info.get("country_code")
                },
                "confidence": 0.7
            }

