import os
import datetime
import re
from google import genai

# Initialize the Gemini client using the repository secret
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

today = datetime.date.today().strftime("%Y-%m-%d")

prompt = f"""
Write a 400-500 word insightful blog post for 'That Digital Human' dated {today}.
Topic: A practical take at the intersection of AI agents, growth marketing, or digital productivity.
Tone: Grounded, authentic, sharp, and actionable. Avoid generic fluff.

Format strictly as:
TITLE: <A short, punchy title>
SLUG: <hyphenated-lowercase-slug-derived-from-title>
---
<Blog body in Markdown with clear subheadings, bullets, and bold takeaways>
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

text = response.text.strip()

title_match = re.search(r"TITLE:\s*(.+)", text)
slug_match = re.search(r"SLUG:\s*(.+)", text)

title = title_match.group(1).strip() if title_match else "Daily Digital Insight"
slug = slug_match.group(1).strip() if slug_match else "daily-insight"
body = text.split("---", 1)[-1].strip()

# Jekyll requires posts to live in a '_posts' folder with a 'YYYY-MM-DD-title.md' format
os.makedirs("_posts", exist_ok=True)
filename = f"_posts/{today}-{slug}.md"

post_content = f"""---
layout: post
title: "{title}"
date: {today}
---

{body}
"""

with open(filename, "w", encoding="utf-8") as f:
    f.write(post_content)

print(f"Generated post: {filename}")
