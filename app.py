import os
from flask import Flask, request, render_template, Response
import requests

app = Flask(__name__)

# Home page with iframe embed
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Proxy route
@app.route("/proxy")
def proxy():
    url = request.args.get("url")

    if not url:
        return "No URL provided."

    # Add http if missing
    if not url.startswith("http"):
        url = "http://" + url

    try:
        r = requests.get(url)
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        headers = [(name, value) for (name, value) in r.raw.headers.items()
                   if name.lower() not in excluded_headers]

        return Response(r.content, r.status_code, headers)
    except Exception as e:
        return f"Error loading site: {e}"

# For local testing and Render deployment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
