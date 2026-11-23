import logging

from flask import Blueprint, jsonify, request

from app.guardrails import detect_injection, validate_output

bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 500
REFUSAL = "I can only help with general personal finance questions."


def generate_mock_response(message: str) -> str:
    # Mock AI: no real LLM, always returns a safe canned answer
    return "You can start by tracking your income and expenses."


@bp.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@bp.post("/api/chat")
def chat():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a valid JSON object"}), 400

    message = data.get("message")
    if message is None:
        return jsonify({"error": "Field 'message' is required"}), 400
    if not isinstance(message, str):
        return jsonify({"error": "Field 'message' must be a string"}), 400

    message = message.strip()
    if not message:
        return jsonify({"error": "Message must not be empty"}), 400
    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": f"Message too long (max {MAX_MESSAGE_LENGTH} characters)"}), 400

    # Log only metadata, never the user's message itself
    logger.info("Chat request received, length=%d", len(message))

    if detect_injection(message):
        logger.warning("Possible prompt injection blocked")
        return jsonify({"response": REFUSAL}), 200

    reply = validate_output(generate_mock_response(message))
    return jsonify({"response": reply}), 200


@bp.app_errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404


@bp.app_errorhandler(405)
def method_not_allowed(_):
    return jsonify({"error": "Method not allowed"}), 405


@bp.app_errorhandler(500)
def internal_error(_):
    return jsonify({"error": "Internal server error"}), 500