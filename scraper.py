import requests
from bs4 import BeautifulSoup
import colorama
import time
import json
import csv

colorama.init()

def scraper(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        #Check content type
        if 'text/html' not in response.headers['Content-Type']:
            raise requests.exceptions.RequestException(f"Unexpected content type: {response.headers['Content-Type']}")

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []

        # This part needs adjustment based on the actual HTML structure of the target page.
        #  Inspect the page source to find the correct selectors for headlines and links.
        for headline in soup.select('h2 a'): #Example selector - adjust as needed.
            title = headline.text.strip()
            link = url + headline['href']
            # Add a summary extraction here if needed.  This will require more sophisticated parsing.
            summary = get_summary(link)
            articles.append({'title': title, 'link': link, 'summary': summary})

        return articles

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_summary(article_url):
    try:
        article_response = requests.get(article_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, timeout=10)
        article_response.raise_for_status()
        #Check content type
        if 'text/html' not in article_response.headers['Content-Type']:
            raise requests.exceptions.RequestException(f"Unexpected content type: {article_response.headers['Content-Type']}")
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        #This will need to be adjusted based on the target page
        summary_element = article_soup.select_one('p')
        if summary_element:
            return summary_element.text.strip()[:200] # Limit summary length
        else:
            return "Summary not available"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article summary: {e}")
        return "Summary not available"

if __name__ == "__main__":
    url = input("Enter the base URL of the web page to scrape: ")
    format = input("Enter desired output format (json or csv): ")
    scraped_data = scraper(url)

    if scraped_data:
        print(colorama.Fore.GREEN + "Articles found:")
        if format.lower() == "json":
            print(json.dumps(scraped_data, indent=4))
        elif format.lower() == "csv":
            with open('output.csv', 'w', newline='', encoding = 'utf-8') as csvfile:
                fieldnames = ['title', 'link', 'summary']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for article in scraped_data:
                    writer.writerow(article)
        else:
            print("Invalid format specified.")
            for article in scraped_data:
                print(colorama.Style.BRIGHT + colorama.Fore.CYAN + f"  Title: <a href='{article['link']}' target='_blank'>{article['title']}</a>")
                print(colorama.Style.RESET_ALL + f"  Summary: {article['summary']}")
                print("---")
    else:
        print(colorama.Fore.RED + "No data could be scraped.")

