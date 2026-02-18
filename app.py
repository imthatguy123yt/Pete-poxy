from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    content = ""
    if request.method == "POST":
        url = request.form.get("url")

        if not url.startswith("http"):
            url = "http://" + url

        try:
            response = requests.get(url)
            content = response.text
        except:
            content = "Error fetching the website."

    return render_template("index.html", content=content)

if __name__ == "__main__":
    app.run(debug=True)
