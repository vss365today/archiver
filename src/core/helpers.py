import re
from html import unescape
from math import floor

import markupsafe


__all__ = [
    "format_content",
    "get_all_hashtags",
    "make_hashtags",
    "make_mentions",
    "make_urls",
    "duration",
]


def duration(seconds: int) -> str:
    # https://stackoverflow.com/a/3856312
    hours = floor(seconds / 3600)
    mins = floor(seconds / 60 % 60)
    secs = floor(seconds % 60)

    # Only display the hours if needed
    if hours > 0:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def format_content(text: str) -> str:
    # Wrap all non-blank lines in paragraphs
    split_text = text.split("\n")
    split_text = [
        f"<p>{para.strip()}</p>"
        for para in split_text
        if para  # false-y value means blank line
    ]

    # Rejoin the lines and make all links clickable
    new_text = "\n".join(split_text)
    new_text = unescape(new_text)
    new_text = make_hashtags(new_text)
    new_text = make_mentions(new_text)
    new_text = make_urls(new_text)
    return new_text


def get_all_hashtags(text: str) -> tuple:
    return tuple(re.findall(r"(#\w+)", text, re.I))


def make_hashtags(text: str) -> str:
    # Go through each hashtag and make it a clickable link
    for ht in get_all_hashtags(text):
        html = f'<a href="https://twitter.com/hashtag/{ht[1:]}">{ht}</a>'
        text = re.sub(rf"({ht})\b", html, text)
    return markupsafe.soft_str(markupsafe.Markup(text))


def make_mentions(text: str) -> str:
    # Start by finding all possible @mentions
    mentions = re.findall(r"(@\w+)", text, re.I)
    if not mentions:
        return text

    # Go through each mention and make it a clickable link
    for mention in mentions:
        html = markupsafe.Markup(f'<a href="https://twitter.com/{mention[1:]}">{mention}</a>')
        text = text.replace(mention, html)
    return markupsafe.soft_str(text)


def make_urls(text: str) -> str:
    """Convert all text links in a tweet into an HTML link."""
    # Start by finding all possible t.co text links
    links = re.findall(r"(https://t\.co/[a-z0-9]+)", text, re.I)
    if not links:
        return text

    # Go through each url and make it a clickable link
    for link in links:
        html = markupsafe.Markup(f'<a href="{link}">{link}</a>')
        text = text.replace(link, html)
    return markupsafe.soft_str(text)
