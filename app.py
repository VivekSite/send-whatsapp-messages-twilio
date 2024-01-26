"""import statements"""
from flask import Flask
from routes import routes


# create flask instance and register all blueprints
app = Flask(__name__)
app.register_blueprint(routes)


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=8080)
