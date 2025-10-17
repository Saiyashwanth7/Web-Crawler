import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from database import engine, LocalSession, Base
from sqlalchemy.orm import Session
import models
from models import ContentStorage
from collections import deque
from sqlalchemy.exc import IntegrityError

models.Base.metadata.create_all(bind=engine)

# This is similar to the GhostDrop, and ToDo projects of mine 
def store_in_db(url, html_content, status):
    db = LocalSession()
    try:
        new_record = ContentStorage(
            html_content=html_content,
            url=url,
            status_code=status,
        )
        db.add(new_record)
        db.commit()
        print('Record created for the url:',url)
    except IntegrityError: # To avoid crawling duplicate urls.
        db.rollback()
        print(f"⚠ URL already exists (skipping): {url}")
    except Exception as e:
        db.rollback()
        print("Exception :", e)
    finally:
        db.close()


# Checks if the discovered link has the same domain as the seed url.
def same_domain(domain, current_domain):
    return urlparse(domain).netloc == urlparse(current_domain).netloc


# Derives the html of the current web-page and returns it.
async def fetch_and_parse(url, session):
    async with session.get(url) as response:
        status_code=response.status
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        return soup,status_code,html


# Takes the seed url, aiohttp.ClientSession as inputs and uses the above function to get the html,from which the children links are discovered.
async def urls_fetching(url, html):
    #html = await fetch_and_parse(url, session)
    discovered = html.find_all("a")
    links = [urljoin(url, link.get("href")) for link in discovered if link.get("href")]
    links = [link for link in links if same_domain(link, url)]
    return links


# This is the main funciton, this will use the BFS algorithm and stores all the discovered links in an array.
async def main(url):
    q = deque([url])
    visited = set()
    max_links = 50
    async with aiohttp.ClientSession() as session:
        all_links = []
        while q and len(visited) < max_links:
            discovered = q.popleft()
            if discovered not in visited:
                visited.add(discovered)
                soup,status,html= await fetch_and_parse(discovered,session)
                store_in_db(discovered,html,status)
                discovered_links = await urls_fetching(discovered, soup)
                all_links.extend(discovered_links)
                for link in discovered_links:
                    if link not in visited:
                        q.append(link)
        #print(all_links)


asyncio.run(main("http://quotes.toscrape.com/")) # Replace with any url, html heavy for now, to use this
