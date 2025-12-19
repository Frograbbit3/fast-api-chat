import html
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin 
import html
def apply_text_coloring(text):
    regex = r"\[\[(#[0-9A-Fa-f]{6}|[a-zA-Z]+)\]\](.*?)\[\[\1\]\]"

    def replace_color(match):
        color = match.group(1)
        text = match.group(2)
        return f'<span style="color:{color};">{text}</span>'
    return re.sub(regex, replace_color, text)


def format_message(message):
    message = html.escape(message)
    message = apply_text_coloring(message)  # Assuming this is defined elsewhere

    # Embedded links [text](url)
    def replace_link(match):
        text, url = match.groups()
        embed_html = get_embed(url) or ""
        return f'<a href="{url}">{text}</a>{embed_html}'

    message = re.sub(r'\[(.*?)\]\((https?://[^\)]+)\)', replace_link, message)

    # Bold: *text*
    message = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', message)

    # Italic: _text_
    message = re.sub(r'_(.*?)_', r'<i>\1</i>', message)

    return message

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import html

def get_embed(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        res.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(res.text, "html.parser")
    meta = {
        tag.get("property") or tag.get("name"): tag.get("content")
        for tag in soup.find_all("meta")
        if tag.get("content")
    }

    raw_image = meta.get("og:image")
    image = urljoin(url, raw_image) if raw_image else ""

    title = meta.get("og:title") or (soup.title.string.strip() if soup.title else "")
    description = meta.get("og:description") or ""

    # Escape to avoid XSS
    title = html.escape(title)
    description = html.escape(description)
    image_tag = f'<img class="embed-image" src="{html.escape(image)}" />' if image else ""

    if not (title or description or image):
        return ""

    parts = ['<div class="embed">']
    if title:
        parts.append(f'<h3 class="embed-title">{title}</h3>')
    if image_tag:
        parts.append(image_tag)
    if description:
        parts.append(f'<p class="embed-text">{description}</p>')
    parts.append('</div>')

    return ''.join(parts)

