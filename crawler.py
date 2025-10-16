import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

#Checks if the discovered link has the same domain as the seed url.
def same_domain(domain,current_domain):
    return urlparse(domain).netloc==urlparse(current_domain).netloc

# Derives the html of the current web-page and returns it.
async def fetch_and_parse(url,session):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

# Takes the seed url, aiohttp.ClientSession as inputs and uses the above function to get the html,from which the children links are discovered.
async def urls_fetching(url,session):
    html=await fetch_and_parse(url,session)
    discovered=html.find_all('a')
    links=[urljoin(url,link.get('href')) for link in discovered if link.get('href')]
    links=[link for link in links if same_domain(link, url)]
    return links

#This is the main funciton, this will use the BFS algorithm and stores all the discovered links in an array.
async def main(url):
    q=deque([url])
    visited=set()
    max_links=50
    async with aiohttp.ClientSession() as session:
        all_links=[]
        while q and len(visited)<max_links:
            discovered=q.popleft()
            if discovered not in visited:
                visited.add(discovered)
                discovered_links=await urls_fetching(discovered,session)
                all_links.extend(discovered_links)
                for link in discovered_links:
                    if link not in visited:
                        q.append(link)
        print(all_links)
        print(len(all_links)==len(set(all_links)))

asyncio.run(main("https://www.iana.org/"))