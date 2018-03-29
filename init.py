# Imports
import re
import signal
from collections import deque
from urllib.parse import urlsplit

import requests
import requests.exceptions
from bs4 import BeautifulSoup


# Press CTRL+C to check for results in the meantime
def signal_handler(signal, frame):
    print(list(results))


# Load the signal Handler
signal.signal(signal.SIGINT, signal_handler)

# Storage for processed addresses
processed_urls = set()

# Load files with information about websites
with open("domains.txt") as f:
    limit_save = f.readlines()  # Load domain limits (The scraper won't leave the domain in the search for new links)
with open("websites.txt") as f:
    custom_urls = f.readlines()  # Load urls (Starting urls from which the scraper will continue searching for more)
with open("banned.txt") as f:
    banned = f.readlines()  # Load banned urls (Do not send requests for .jpg .zip and such downloads)
Count = 0  # Counter for place in list
# Will also be used to name files for multiple website scraping


# Actual function
def do():
    while len(new_urls):
        url = new_urls.popleft()
        processed_urls.add(url)

        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        if any(c in url for c in banned):
            print("Link Skipped")
        else:
            print("Processing %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, UnicodeError):
                continue

            new_emails = set(re.findall(r'[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+', response.text, re.I))
            results.update(new_emails)  # Add the found emails to the set

            soup = BeautifulSoup(response.text, "lxml")

            for anchor in soup.find_all("a"):
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                if limit_url in link:
                    if link.startswith('/'):
                        link = base_url + link
                    elif not link.startswith('http'):
                        link = path + link
                    if link not in new_urls and link not in processed_urls:
                        new_urls.append(link)


for c_url in custom_urls:
    results = set()
    f = open("emails_" + str(Count) + ".txt", "w+")
    new_urls = deque([c_url])
    limit_url = limit_save[Count]
    do()
    c_list = list(results)
    for c_email in c_list:
        f.write(c_email + "\n")
        print(c_email)
    Count += 1
    f.close()
