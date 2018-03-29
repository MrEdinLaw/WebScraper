from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import signal

def signal_handler(signal, frame): #CTRL+C
    print(list(results));
signal.signal(signal.SIGINT, signal_handler) #Load It

processed_urls = set()

def do():
    while len(new_urls):
        url = new_urls.popleft()
        processed_urls.add(url)

        if not ("javascript" or "pdf") in url:
            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            banned = ['javascript', 'pdf', 'doc', 'docx', 'jpg','jpeg','png','JPG','JPEG','PNG','gif','GIF','ppt','rar','pptx','zip','http://Visoka']
            if any(c in url for c in banned):
                print("Link Skipped");
            else:
                print("Processing %s" % url)
                try:
                    response = requests.get(url)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError , UnicodeError):
                    continue

                new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
                results.update(new_emails)

                soup = BeautifulSoup(response.text)

                for anchor in soup.find_all("a"):
                    link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                    if limit_url in link:
                        if link.startswith('/'):
                            link = base_url + link
                        elif not link.startswith('http'):
                            link = path + link
                        if not link in new_urls and not link in processed_urls:
                            new_urls.append(link)

limit_save = ['']

custom_urls = ['']             
Count = 0;
for c_url in custom_urls:
    results = set()
    f= open("emails_"+str(Count)+".txt","w+")
    new_urls = deque([c_url])
    limit_url = limit_save[Count];
    do();
    c_list = list(results);
    for c_email in c_list:
        f.write(c_email+"\n");
        print(c_email);
    Count +=1;
    f.close() 
    
