from typing import TypedDict
import json

import requests
from bs4 import BeautifulSoup


class Article(TypedDict):
    """Defines the structure of the data for each article."""

    url: str
    infobox: dict[str, str] | None
    body: str
    references: list[str]
    other_articles: list[str]


def scrape_wikipedia_article(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:  # 200 = successful
            return parse_wikipedia_article(response.text)
        else:
            return f"Failed to retrieve content, status code: {response.status_code}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


def parse_wikipedia_article(response_text: str) -> Article:
    """Parses the response text from an articles HTML page into a structured article"""
    soup = BeautifulSoup(response_text, "lxml")

    # Scrape the body
    # The body is comprised of <h2> & <h3> tags for headers, <p> tags for content, & <ul> tags for bullet points
    # We can structure this data more uniformly in the future but for now it'll just be stored in a single string
    body = ""
    body_tag = soup.select_one(".mw-content-ltr.mw-parser-output")

    for tag in body_tag:
        if tag.name == "h2" or tag.name == "h3":
            # When we get to the references section break since we want to scrape that section separately
            if tag.select_one("#References"):
                break

            body = f"{body}\n{tag.text.strip()}\n"

        if tag.name == "p":
            body = f"{body}{tag.text.strip()}"

        if tag.name == "ul":
            list_tags = tag.select("li")
            for list_tag in list_tags:
                body = f"{body}\n{list_tag.text}"

    # Scrape the contents of the infobox into key value pairs
    infobox = None
    infobox_tag = soup.select_one("table.infobox")

    if infobox_tag:
        infobox = {}
        tr_tags = infobox_tag.select("tr")

        for tr_tag in tr_tags:
            label = tr_tag.select_one(".infobox-label")
            data = tr_tag.select_one(".infobox-data")

            if label and data:
                infobox[label.text] = data.text

    # Scrape the references
    references = []

    # Find the ordered references section
    references_section = soup.find("ol", class_="references")

    if references_section:
        # Extract all the references
        for reference in references_section.find_all("li"):
            ref_text = reference.get_text()
            references.append(ref_text.strip())

    # Scrape the links to other wikipedia articles
    a_tags = body_tag.select("a[href]")
    other_articles = set()  # A set will prevent duplicate articles

    for a_tag in a_tags:
        href = a_tag.get("href")
        if href.startswith("/wiki/") and ":" not in href:
            other_articles.add(href)

    article: Article = {
        "url": url,
        "infobox": infobox,
        "body": body,
        "references": references,
        "other_articles": list(other_articles),
    }
    return article


# Testing
urls = [
    "https://en.wikipedia.org/wiki/Web_scraping",
    "https://en.wikipedia.org/wiki/World_Wide_Web",
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
]
scraped_articles: list[Article] = []

for url in urls:
    print(f"Scraping {url}")

    article = scrape_wikipedia_article(url)

    if type(article) == str:
        print(f"Failed to scrape {url}, reason: {article}")
        continue

    apprx_word_count = len(article["body"].split(" "))
    reference_count = len(article["references"])
    other_article_count = len(article["other_articles"])

    print(
        f"Found apprx. {apprx_word_count} words, {reference_count} references, & {other_article_count} links to other articles"
    )

    scraped_articles.append(article)


# We can use a DB later if we're scraping enough articles but for now a JSON file is fine
with open("output.json", "w") as output_file:
    output_file.write(json.dumps(scraped_articles, indent=2))

print(f"Succesfully scraped & stored {len(scraped_articles)} articles")
