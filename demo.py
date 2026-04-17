"""
Demo script to showcase the Multi-Agent Recipe Suggestion System
"""

from orchestrator import RecipeOrchestrator
import os
from dotenv import load_dotenv


def demo():
    """Run demo examples."""
    # Load environment variables from .env file
    load_dotenv()
    
    print("=" * 70)
    print("🎬 Multi-Agent Recipe Suggestion System - Demo")
    print("=" * 70)
    
    # Initialize orchestrator
    api_key = os.getenv("GEMINI_API_KEY")
    orchestrator = RecipeOrchestrator(api_key=api_key)
    
    # Demo examples
    examples = [
        {
            "input": "I want something spicy and vegetarian for dinner",
            "location": None
        },
        {
            "input": "Looking for a light, healthy breakfast",
            "location": "Mumbai, India"
        },
        {
            "input": "Need a quick vegan snack",
            "location": None
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n\n{'='*70}")
        print(f"📝 Example {i}: {example['input']}")
        print(f"{'='*70}\n")
        
        try:
            result = orchestrator.suggest_recipe(
                user_input=example["input"],
                location_override=example["location"]
            )
            print(orchestrator.format_output(result))
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")


if __name__ == "__main__":
    demo()

