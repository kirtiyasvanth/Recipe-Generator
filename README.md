# Multi-Agent AI Recipe Suggestion System

An intelligent multi-agent AI system that suggests suitable food recipes by analyzing user preferences, current context (time and location), and generating personalized recipe recommendations.

## 🎯 Features

1. **Preference Classification**: Analyzes text input to classify food preferences (spicy, sweet, vegan, vegetarian, etc.)
2. **Context Detection**: Automatically detects user's current time and location
3. **Meal Type Determination**: Determines appropriate meal type (breakfast, lunch, dinner, snack) based on time
4. **Cuisine Mapping**: Maps user location to relevant local cuisines
5. **Intelligent Food Selection**: Selects the most suitable dish matching all criteria
6. **Recipe Generation**: Generates complete recipes with ingredients, instructions, and nutrition info

## 🏗️ Architecture

The system uses a hierarchical multi-agent architecture:

```
RecipeOrchestrator (Main Coordinator)
├── PreferenceClassifierAgent (Agent 1)
├── ContextDetectorAgent (Agent 2)
├── MealTypeDeterminerAgent (Agent 3)
├── CuisineMapperAgent (Agent 4)
├── FoodSelectorAgent (Agent 5)
└── RecipeGeneratorAgent (Agent 6)
```

### Agent Responsibilities

1. **PreferenceClassifierAgent**: Classifies user food preferences from text input
2. **ContextDetectorAgent**: Detects current time and location (IP-based geolocation)
3. **MealTypeDeterminerAgent**: Determines meal type based on current hour
4. **CuisineMapperAgent**: Maps location to relevant local cuisines
5. **FoodSelectorAgent**: Selects the most suitable dish based on all criteria
6. **RecipeGeneratorAgent**: Generates detailed recipe with ingredients and steps

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MULTIAGENT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (OPTIONAL - system works without it):
   
   **Important:** The API key is OPTIONAL. The system works without it using intelligent mock responses with fallback mechanisms. However, using an API key provides more accurate and personalized results.
   
   **For OpenAI (default):**
   ```bash
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # Windows (CMD)
   set OPENAI_API_KEY=your-api-key-here
   
   # Linux/Mac
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
   
   **Note:** Currently supports OpenAI by default. The architecture is modular and can be extended to support other LLM providers (Anthropic Claude, Google Gemini, etc.) - see Configuration section below.

## 🚀 Usage

### Basic Usage

```bash
python main.py "I want something spicy and vegetarian for dinner"
```

### Interactive Mode

```bash
python main.py
```

Then enter your preferences when prompted.

### Programmatic Usage

```python
from orchestrator import RecipeOrchestrator

# Initialize orchestrator
orchestrator = RecipeOrchestrator(api_key="your-api-key")

# Get recipe suggestion
result = orchestrator.suggest_recipe(
    user_input="I want a light, healthy vegetarian lunch",
    location_override="New York, USA"  # Optional
)

# Format and display
print(orchestrator.format_output(result))
```

## 📝 Example Inputs

- "I want something spicy and vegetarian"
- "Looking for a light, healthy breakfast"
- "Need a quick vegan snack"
- "I want traditional Indian food for dinner"
- "Something sweet for dessert"

## 🔧 Configuration

### LLM Provider

**Current Support:** OpenAI (default)

**API Key Requirement:** OPTIONAL - The system works without an API key using intelligent mock responses. However, using an API key provides significantly better, more personalized results.

**Using Other LLM Providers:**

The system architecture is modular and can be extended to support other providers. To use a different LLM provider (e.g., Anthropic Claude, Google Gemini, Hugging Face):

1. Install the provider's SDK:
   ```bash
   # For Anthropic Claude
   pip install anthropic
   
   # For Google Gemini
   pip install google-generativeai
   
   # For Hugging Face
   pip install transformers
   ```

2. Modify `agents/llm_client.py` to implement your preferred LLM API:

   ```python
   # Example: Anthropic Claude
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

3. Update environment variable name if needed (e.g., `ANTHROPIC_API_KEY`)

### Location Detection

Location is detected automatically using IP geolocation. You can override it by:
- Providing location in interactive mode
- Passing `location_override` parameter in programmatic usage

## 📊 Output Format

The system provides:
- **Dish Information**: Name, cuisine, meal type, dietary type
- **Recipe Details**: Description, prep/cook time, servings
- **Ingredients**: Complete list with quantities
- **Instructions**: Step-by-step cooking instructions
- **Tips**: Cooking tips and suggestions
- **Nutrition Info**: Approximate nutritional information

## 🛠️ Project Structure

```
MULTIAGENT/
├── agents/
│   ├── __init__.py
│   ├── preference_classifier.py
│   ├── context_detector.py
│   ├── meal_type_determiner.py
│   ├── cuisine_mapper.py
│   ├── food_selector.py
│   ├── recipe_generator.py
│   └── llm_client.py
├── orchestrator.py
├── main.py
├── requirements.txt
└── README.md
```

## 🔍 How It Works

1. **User Input**: User provides food preferences as text
2. **Preference Analysis**: Agent 1 classifies preferences (spicy, vegan, etc.)
3. **Context Detection**: Agent 2 detects current time and location
4. **Meal Type**: Agent 3 determines meal type from time
5. **Cuisine Mapping**: Agent 4 maps location to local cuisines
6. **Dish Selection**: Agent 5 selects the most suitable dish
7. **Recipe Generation**: Agent 6 generates complete recipe
8. **Output**: Formatted recipe with all details

## 🎨 Features

- **Intelligent Analysis**: Uses LLM for nuanced preference understanding
- **Context-Aware**: Considers time and location automatically
- **Fallback Mechanisms**: Works even without API keys (mock responses)
- **Comprehensive Recipes**: Includes ingredients, steps, tips, and nutrition
- **Modular Design**: Easy to extend or modify individual agents

## ⚠️ Notes

- **API Key is OPTIONAL** - Without an API key, the system uses intelligent mock responses (fully functional)
- **LLM Support:** Currently OpenAI by default, but architecture supports extension to other providers
- Location detection requires internet connection
- For production use, consider adding error handling and rate limiting
- Recipe accuracy depends on LLM quality and training data (better with API key)

## 🤝 Contributing

Feel free to extend the system by:
- Adding more agents for specific tasks
- Improving cuisine mapping accuracy
- Adding support for dietary restrictions
- Enhancing recipe generation quality

## 📄 License

This project is open source and available for educational and commercial use.

## 🙏 Acknowledgments

Built with:
- OpenAI API for LLM capabilities
- IP Geolocation services for location detection
- Python for agent orchestration

"# Recipe-Generator" 
