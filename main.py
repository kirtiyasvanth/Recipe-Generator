"""
Main entry point for the Multi-Agent Recipe Suggestion System
"""

import os
import sys
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from orchestrator import RecipeOrchestrator


def main():
    """Main function to run the recipe suggestion system."""
    # Load environment variables from .env file
    load_dotenv()
    
    print("=" * 60)
    print("Multi-Agent AI Recipe Suggestion System")
    print("=" * 60)
    
    # Initialize orchestrator
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY1")
    if not api_key:
        print("\n[WARNING] GEMINI_API_KEY not set. Using mock responses.")
        print("   Set GEMINI_API_KEY environment variable in your .env file for better results.\n")
    
    orchestrator = RecipeOrchestrator(api_key=api_key)
    
    # Example usage
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        location_override = None
    else:
        # Interactive mode
        print("\nEnter your food preferences (or 'quit' to exit):")
        user_input = input("> ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            return
        
        print("\nEnter your location (city, country) - press Enter to auto-detect:")
        location_input = input("> ").strip()
        location_override = location_input if location_input else None
    
    if not user_input:
        print("No input provided. Exiting.")
        return
    
    try:
        # Get recipe suggestion
        result = orchestrator.suggest_recipe(user_input, location_override)
        
        # Display formatted output
        print(orchestrator.format_output(result))
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

