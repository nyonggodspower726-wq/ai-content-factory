import os
from flask import Flask, send_from_directory

app = Flask(__name__)

OUTPUT_DIR = os.path.abspath("output")


@app.route("/")
def home():
    return "PromptProHub Video Server Online"


@app.route("/videos/<path:filename>")
def video(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
