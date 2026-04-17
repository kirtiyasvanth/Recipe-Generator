from flask import Flask, request, render_template, redirect, url_for
import os
from dotenv import load_dotenv
from orchestrator import RecipeOrchestrator

# Load environment variables
load_dotenv()

# Initialize Flask app
# Map templates and static files to the frontend folder
app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='')

# Initialize orchestrator
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY1")
orchestrator = RecipeOrchestrator(api_key=api_key)

@app.route('/')
@app.route('/index.html')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/input.html')
def input_page():
    """Render the input form."""
    return render_template('input.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handle form submission and generate recipe."""
    preferences = request.form.get('preferences')
    location = request.form.get('location')
    
    if not preferences:
        return redirect(url_for('input_page'))
    
    try:
        # Run the multi-agent orchestrator
        result = orchestrator.suggest_recipe(
            user_input=preferences, 
            location_override=location if location else None
        )
        return render_template('result.html', result=result)
    except Exception as e:
        # In a production app we'd render an error page
        return f"<h1>Error generating recipe</h1><p>{str(e)}</p><a href='/input.html'>Go back</a>"

if __name__ == '__main__':
    print("=" * 60)
    print("Starting AI Chef Web Application...")
    print("Open http://127.0.0.1:5000 in your browser.")
    print("=" * 60)
    app.run(debug=True, port=5000)
