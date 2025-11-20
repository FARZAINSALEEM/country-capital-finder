from flask import Flask, render_template, request, jsonify
import wikipedia

# The Flask application object must be defined at the top level
app = Flask(__name__)

# Route to serve the main HTML page
@app.route('/')
def home():
    # Flask automatically looks in the 'templates' folder for index.html
    return render_template('index.html')

# API Route to handle the capital search request
@app.route('/api/capital', methods=['POST'])
def get_capital():
    data = request.get_json()
    country_name = data.get('country')

    if not country_name:
        return jsonify({"error": "No country provided"}), 400

    try:
        # --- Your Capital Search Logic ---
        # Note: Large Wikipedia pages might cause issues, but this setup works generally.
        page = wikipedia.page(country_name)
        summary = page.summary
        capital_info = "Capital not found in Wikipedia summary."

        for sentence in summary.split('. '):
            if 'capital' in sentence.lower():
                capital_info = sentence
                break
        # --------------------------------

        return jsonify({"country": country_name, "info": capital_info})

    except wikipedia.exceptions.DisambiguationError as e:
        return jsonify({"error": f"'{country_name}' is ambiguous. Options: {e.options[:3]}"}), 404
    except wikipedia.exceptions.PageError:
        return jsonify({"error": f"Country '{country_name}' not found on Wikipedia."}), 404
    except Exception as e:
        # A generic error handler for unexpected Wikipedia or network issues
        return jsonify({"error": f"An unexpected error occurred during search: {e}"}), 500
