"""
Meal Type Determination Agent
Determines appropriate meal type based on current time.
"""

from typing import Dict
from datetime import datetime


class MealTypeDeterminerAgent:
    """Agent responsible for determining meal type based on time."""
    
    def __init__(self):
        """Initialize the meal type determiner agent."""
        self.meal_time_ranges = {
            "breakfast": (6, 11),   # 6 AM to 11 AM
            "lunch": (11, 15),      # 11 AM to 3 PM
            "dinner": (17, 22),     # 5 PM to 10 PM
            "snack": (15, 17)       # 3 PM to 5 PM (afternoon snack)
        }
    
    def determine_meal_type(self, hour: int, context: Dict = None) -> Dict[str, any]:
        """
        Determine meal type based on current hour.
        
        Args:
            hour: Current hour (0-23)
            context: Optional additional context
            
        Returns:
            Dictionary containing meal type and reasoning
        """
        meal_type = None
        confidence = 0.8
        
        # Determine meal type based on hour
        if 6 <= hour < 11:
            meal_type = "breakfast"
        elif 11 <= hour < 15:
            meal_type = "lunch"
        elif 15 <= hour < 17:
            meal_type = "snack"
        elif 17 <= hour < 22:
            meal_type = "dinner"
        else:
            # Late night or early morning
            if hour >= 22 or hour < 6:
                meal_type = "snack"  # Late night snack
                confidence = 0.6
            else:
                meal_type = "breakfast"
                confidence = 0.7
        
        return {
            "meal_type": meal_type,
            "hour": hour,
            "confidence": confidence,
            "reasoning": f"Based on current hour ({hour}:00), the appropriate meal type is {meal_type}"
        }
    
    def determine_from_time_info(self, time_info: Dict) -> Dict[str, any]:
        """
        Determine meal type from time information dictionary.
        
        Args:
            time_info: Dictionary containing time information
            
        Returns:
            Dictionary containing meal type and reasoning
        """
        hour = time_info.get("hour", datetime.now().hour)
        return self.determine_meal_type(hour, time_info)

