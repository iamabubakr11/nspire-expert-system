"""Nspire Dev Expert System — Flask web application."""
import logging
from flask import Flask, jsonify, render_template, request
from expert.engine import evaluate

app = Flask(__name__)
app.json.ensure_ascii = False
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024
logging.basicConfig(level=logging.INFO)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "engine": "CLIPS via CLIPSPy"})


@app.post("/api/recommend")
def recommend():
    if not request.is_json:
        return jsonify({"error": "Отправьте ответы в формате JSON."}), 415
    try:
        result = evaluate(request.get_json(silent=True))
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Inference engine failed")
        return jsonify({"error": "Внутренняя ошибка экспертной системы."}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
