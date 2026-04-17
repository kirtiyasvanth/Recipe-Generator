# Quick Start Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set API key for better results:
   
   **The system works WITHOUT an API key** - it uses intelligent mock responses with fallback mechanisms. However, using an API key provides more accurate and personalized results.
   
   **For OpenAI (default):**
   ```bash
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # Windows (CMD)
   set OPENAI_API_KEY=your-api-key-here
   
   # Linux/Mac
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   **Note:** Currently, the system supports OpenAI by default. The architecture is modular and can be extended to support other LLM providers (Anthropic Claude, Google Gemini, etc.) by modifying `agents/llm_client.py`.

## Usage Examples

### Command Line

```bash
# Basic usage
python main.py "I want spicy vegetarian food"

# With location
python main.py "Looking for a light breakfast" "Mumbai, India"
```

### Interactive Mode

```bash
python main.py
# Then enter your preferences when prompted
```

### Python Code

```python
from orchestrator import RecipeOrchestrator

orchestrator = RecipeOrchestrator(api_key="your-key")
result = orchestrator.suggest_recipe(
    "I want a healthy vegan lunch",
    location_override="New York, USA"
)
print(orchestrator.format_output(result))
```

## Example Inputs

- "I want something spicy and vegetarian"
- "Looking for a light, healthy breakfast"
- "Need a quick vegan snack"
- "I want traditional Indian food for dinner"
- "Something sweet for dessert"

## System Architecture

The system uses 6 specialized agents:

1. **PreferenceClassifierAgent**: Analyzes text to extract food preferences
2. **ContextDetectorAgent**: Detects current time and location
3. **MealTypeDeterminerAgent**: Determines meal type from time
4. **CuisineMapperAgent**: Maps location to local cuisines
5. **FoodSelectorAgent**: Selects suitable dish
6. **RecipeGeneratorAgent**: Generates complete recipe

## Notes

- **API Key is OPTIONAL** - The system works without an API key using intelligent mock responses
- **Current LLM Support:** OpenAI (default). Can be extended to support other providers
- Location auto-detected via IP geolocation
- All agents have fallback mechanisms for reliability

## Using Other LLM Providers

To use a different LLM provider (e.g., Anthropic Claude, Google Gemini), modify `agents/llm_client.py`:

```python
# Example for Anthropic Claude
from anthropic import Anthropic

class LLMClient:
    def _initialize_client(self):
        if self.api_key:
            self._client = Anthropic(api_key=self.api_key)
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        response = self._client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
```

