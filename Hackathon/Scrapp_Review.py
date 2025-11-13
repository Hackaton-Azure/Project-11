import requests
import csv
import datetime
import time

API_KEY = "nG3e6j2lEg2QnijkKIpQo0YG9caafwIK"
CSV_FILENAME = "nyt_ai_subject_articles_2025.csv"
BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
subject_tag = "Artificial Intelligence"

start_year = 2025
articles = []

def daterange(start_date, end_date, delta):
    current = start_date
    while current < end_date:
        yield current, min(end_date, current + delta)
        current += delta

start_date = datetime.date(start_year, 1, 1)
end_date = datetime.date(start_year, 12, 31)

# Use 1 month intervals to chunk queries
chunk_delta = datetime.timedelta(days=30)

for chunk_start, chunk_end in daterange(start_date, end_date, chunk_delta):
    begin_date_str = chunk_start.strftime('%Y%m%d')
    end_date_str = chunk_end.strftime('%Y%m%d')
    print(f"Fetching articles from {begin_date_str} to {end_date_str}")

    for page in range(0, 10):
        params = {
            "api-key": API_KEY,
            "q": subject_tag,
            "begin_date": begin_date_str,
            "end_date": end_date_str,
            "sort": "newest",
            "fl": "headline,snippet,web_url,pub_date",
            "page": page
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 429:  # Rate limit hit
            print("Rate limit reached. Sleeping for 60 seconds...")
            time.sleep(60)
            response = requests.get(BASE_URL, params=params)  # Retry

        if response.status_code != 200:
            print(f"Failed to fetch page {page} for dates {begin_date_str}-{end_date_str}: Status {response.status_code}")
            break

        data = response.json()

        if "response" not in data or not data["response"]["docs"]:
            print("No more articles in this date chunk.")
            break

        for doc in data["response"]["docs"]:
            articles.append({
                "headline": doc["headline"]["main"],
                "snippet": doc.get("snippet", ""),
                "url": doc["web_url"],
                "pub_date": doc["pub_date"]
            })

        time.sleep(6)  # Delay to prevent too many rapid requests

# Save to CSV
with open(CSV_FILENAME, mode='w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["headline", "snippet", "url", "pub_date"])
    writer.writeheader()
    for article in articles:
        writer.writerow(article)

print(f"Saved {len(articles)} articles tagged '{subject_tag}' from {start_year} to '{CSV_FILENAME}'.")
