import os
from flask import Flask, request, render_template, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

# Basic URL filtering - block dangerous sites
BLOCKED_KEYWORDS = [
    "malware", "phishing", "adult", "porn", "torrent"
]

def is_safe_url(url):
    url_lower = url.lower()
    return not any(keyword in url_lower for keyword in BLOCKED_KEYWORDS)

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Proxy route
@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    if not url:
        return "<h2 style='color:red;text-align:center;'>No URL provided</h2>"

    if not is_safe_url(url):
        return "<h2 style='color:red;text-align:center;'>Blocked URL for safety</h2>"

    if not url.startswith("http"):
        url = "https://" + url

    try:
        r = requests.get(url, timeout=10)
        content_type = r.headers.get("Content-Type", "")

        # Only rewrite HTML pages
        if "text/html" in content_type:
            soup = BeautifulSoup(r.text, "html.parser")
            # Rewrite all <a> and <form> links to pass through proxy
            for tag in soup.find_all(["a", "form"]):
                if tag.name == "a" and tag.has_attr("href"):
                    new_url = urljoin(url, tag["href"])
                    tag["href"] = "/proxy?url=" + new_url
                if tag.name == "form" and tag.has_attr("action"):
                    new_url = urljoin(url, tag["action"])
                    tag["action"] = "/proxy?url=" + new_url
            return str(soup)
        else:
            # For non-HTML, just return raw content
            excluded_headers = [
                "content-encoding",
                "content-length",
                "transfer-encoding",
                "connection",
                "x-frame-options",
                "content-security-policy"
            ]
            headers = [(name, value) for (name, value) in r.raw.headers.items()
                       if name.lower() not in excluded_headers]
            return Response(r.content, r.status_code, headers)

    except Exception as e:
        return f"<h2 style='color:red;text-align:center;'>Error loading site</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
