"""
Context Detection Agent
Automatically obtains user's current time and location.
"""

from datetime import datetime
from typing import Dict
import requests
import json


class ContextDetectorAgent:
    """Agent responsible for detecting user's current time and location."""
    
    def __init__(self):
        """Initialize the context detector agent."""
        pass
    
    def detect_context(self) -> Dict[str, any]:
        """
        Detect user's current time and location.
        
        Returns:
            Dictionary containing time and location information
        """
        # Get current time
        current_time = datetime.now()
        time_info = {
            "hour": current_time.hour,
            "minute": current_time.minute,
            "timezone": str(current_time.astimezone().tzinfo),
            "timestamp": current_time.isoformat()
        }
        
        # Get location (using IP geolocation as fallback)
        location_info = self._get_location()
        
        return {
            "time": time_info,
            "location": location_info
        }
    
    def _get_location(self) -> Dict[str, any]:
        """
        Get user's location using IP geolocation.
        
        Returns:
            Dictionary containing location information
        """
        try:
            # Add User-Agent to avoid being blocked by ipapi.co
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get("https://ipapi.co/json/", headers=headers, timeout=5)
            
            # If ipapi fails or rate limits, fallback to ip-api
            if response.status_code != 200:
                response = requests.get("http://ip-api.com/json/", timeout=5)
                data = response.json()
                return {
                    "city": data.get("city", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "country": data.get("country", "Unknown"),
                    "country_code": data.get("countryCode", "Unknown"),
                    "latitude": data.get("lat"),
                    "longitude": data.get("lon"),
                    "timezone": data.get("timezone", "Unknown")
                }
                
            data = response.json()
            # If ipapi returns error field (like rate limit exceeded)
            if "error" in data:
                raise Exception(data.get("reason", "API Error"))
                
            return {
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country_name", "Unknown"),
                "country_code": data.get("country_code", "Unknown"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone": data.get("timezone", "Unknown")
            }
        except Exception as e:
            print(f"Location detection error: {e}")
        
        # Fallback to default location
        return {
            "city": "Unknown",
            "region": "Unknown",
            "country": "Unknown",
            "country_code": "US",
            "latitude": None,
            "longitude": None,
            "timezone": "UTC"
        }
    
    def get_location_by_input(self, location_input: str) -> Dict[str, any]:
        """
        Get location information from user input (city/country name).
        
        Args:
            location_input: User-provided location string
            
        Returns:
            Dictionary containing location information
        """
        # For simplicity, return structured location info
        # In production, use geocoding API
        return {
            "city": location_input.split(",")[0].strip() if "," in location_input else location_input,
            "region": location_input.split(",")[1].strip() if "," in location_input else "Unknown",
            "country": "Unknown",
            "country_code": "Unknown",
            "latitude": None,
            "longitude": None,
            "timezone": "Unknown"
        }

