from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

# Define the home page route
@app.route("/")
def home():
    return "<h1>Welcome to the AI Resume Builder!</h1><p>My first Flask application is running successfully.</p>"

# Run the application
if __name__ == "__main__":
    app.run(debug=True)