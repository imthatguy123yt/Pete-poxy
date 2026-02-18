from flask import Flask, request, render_template, Response
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/proxy")
def proxy():
    url = request.args.get("url")

    if not url:
        return "No URL provided."

    if not url.startswith("http"):
        url = "http://" + url

    try:
        r = requests.get(url)
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        headers = [(name, value) for (name, value) in r.raw.headers.items()
                   if name.lower() not in excluded_headers]

        return Response(r.content, r.status_code, headers)

    except:
        return "Error loading site."

if __name__ == "__main__":
    app.run(debug=True)
