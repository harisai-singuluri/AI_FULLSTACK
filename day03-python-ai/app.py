# app.py
# Flask application entry point

from flask import Flask, jsonify
from flask_cors import CORS
from config import config

# Import route blueprints
from routes.sentiment import sentiment_bp
from routes.classifier import classifier_bp
from routes.summarizer import summarizer_bp

# ─────────────────────────
# App Initialization
# ─────────────────────────
app = Flask(__name__)
CORS(app)  # Allow all origins — restrict in production

# ─────────────────────────
# Register Blueprints
# ─────────────────────────
app.register_blueprint(sentiment_bp, url_prefix="/api/sentiment")
app.register_blueprint(classifier_bp, url_prefix="/api/classifier")
app.register_blueprint(summarizer_bp, url_prefix="/api/summarizer")

# ─────────────────────────
# Root & Health
# ─────────────────────────
@app.route("/")
def root():
    return jsonify({
        "service": "AI/ML Python Microservice",
        "status": "running",
        "version": "1.0.0",
        "environment": config.ENV,
        "endpoints": {
            "sentiment": {
                "analyze": "POST /api/sentiment/analyze",
                "batch": "POST /api/sentiment/batch"
            },
            "classifier": {
                "classify": "POST /api/classifier/classify",
                "presets": "GET /api/classifier/presets"
            },
            "summarizer": {
                "summarize": "POST /api/summarizer/summarize"
            }
        }
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "python-ai-service",
        "port": config.PORT
    })


# ─────────────────────────
# Global Error Handlers
# ─────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"success": False, "error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"success": False, "error": "Internal server error"}), 500


# ─────────────────────────
# Start Server
# ─────────────────────────
if __name__ == "__main__":
    print(f"\n🐍 Python AI Service starting on port {config.PORT}")
    print(f"📍 Environment: {config.ENV}")
    print(f"🌐 URL: http://localhost:{config.PORT}\n")

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )