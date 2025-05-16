import os
import sys
import requests
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_URL = sys.argv[1]

def call_gemini_flash(youtube_url):
    prompt = f"Summarize the news in this YouTube video: {youtube_url}"
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    res = requests.post(url, headers=headers, params=params, json=body)
    res.raise_for_status()
    return res.json()["candidates"][0]["content"]["parts"][0]["text"]

def update_readme(summary, video_url):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    section_header = f"\n## 📰 News Summary ({video_url})\n"
    updated_content = section_header + summary + "\n\n" + content

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    if not re.match(r"^https://(www\.)?youtube\.com/watch\?v=", YOUTUBE_URL):
        print("Invalid YouTube URL")
        sys.exit(1)
    
    summary = call_gemini_flash(YOUTUBE_URL)
    update_readme(summary, YOUTUBE_URL)
