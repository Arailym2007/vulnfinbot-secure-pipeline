from app import create_app
from app.routes import MAX_MESSAGE_LENGTH


def get_client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health_check():
    resp = get_client().get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "healthy"}


def test_chat_success():
    resp = get_client().post("/api/chat", json={"message": "How can I manage my monthly budget?"})
    assert resp.status_code == 200
    assert "response" in resp.get_json()


def test_chat_empty_message():
    resp = get_client().post("/api/chat", json={"message": "   "})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_chat_missing_message():
    resp = get_client().post("/api/chat", json={"text": "hello"})
    assert resp.status_code == 400


def test_chat_invalid_json():
    resp = get_client().post("/api/chat", data="{bad json", content_type="application/json")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_chat_message_too_long():
    resp = get_client().post("/api/chat", json={"message": "a" * (MAX_MESSAGE_LENGTH + 1)})
    assert resp.status_code == 400


def test_chat_unexpected_input_type():
    client = get_client()
    for bad_value in [123, ["hi"], {"a": 1}, True]:
        resp = client.post("/api/chat", json={"message": bad_value})
        assert resp.status_code == 400
