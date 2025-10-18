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
import time

models.Base.metadata.create_all(bind=engine)

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
    except IntegrityError:
        db.rollback()
        print(f"⚠ URL already exists (skipping): {url}")
    except Exception as e:
        db.rollback()
        print("Exception :", e)
    finally:
        db.close()


def same_domain(domain, current_domain):
    return urlparse(domain).netloc == urlparse(current_domain).netloc


async def fetch_and_parse(url, session,sem):
    try:
        async with sem:
            async with session.get(url, timeout=10) as response:
                status_code = response.status
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                return soup, status_code, html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None, None


async def urls_fetching(url, html,sem):
    async with sem:
        if not html:
            return []
        discovered = html.find_all("a")
        links = [urljoin(url, link.get("href")) for link in discovered if link.get("href")]
        links = [link for link in links if same_domain(link, url)]
        return links

sem=asyncio.Semaphore(10)
async def main(url, max_links=50):
    q = deque([url])
    visited = set()
    all_links = []
    
    # Performance tracking
    start_time = time.time()
    fetch_times = []
    parse_times = []
    db_times = []
    
    async with aiohttp.ClientSession() as session:
        while q and len(visited) < max_links:
            discovered = q.popleft()
            if discovered not in visited:
                visited.add(discovered)
                
                # Fetch timing
                fetch_start = time.time()
                soup, status, html = await fetch_and_parse(discovered, session,sem)
                fetch_time = time.time() - fetch_start
                fetch_times.append(fetch_time)
                
                if not html:
                    continue
                
                # DB storage timing
                db_start = time.time()
                store_in_db(discovered, html, status)
                db_time = time.time() - db_start
                db_times.append(db_time)
                
                # Parse timing
                parse_start = time.time()
                discovered_links = await urls_fetching(discovered, soup,sem)
                parse_time = time.time() - parse_start
                parse_times.append(parse_time)
                
                all_links.extend(discovered_links)
                for link in discovered_links:
                    if link not in visited:
                        q.append(link)
        
        total_time = time.time() - start_time
    
    # Print comprehensive metrics
    print("\n" + "="*60)
    print("CRAWLER PERFORMANCE METRICS")
    print("="*60)
    print(f"Total URLs crawled: {len(visited)}")
    print(f"Total unique links discovered: {len(set(all_links))}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per URL: {total_time/len(visited):.2f} seconds")
    print(f"Crawl rate: {len(visited)/total_time:.2f} URLs/second")
    print("\nBreakdown by operation:")
    print(f"  - Fetch time: {sum(fetch_times):.2f}s (avg: {sum(fetch_times)/len(fetch_times):.2f}s per URL)")
    print(f"  - Parse time: {sum(parse_times):.2f}s (avg: {sum(parse_times)/len(parse_times):.2f}s per URL)")
    print(f"  - DB storage: {sum(db_times):.2f}s (avg: {sum(db_times)/len(db_times):.2f}s per URL)")
    print("="*60)


asyncio.run(main("https://www.nytimes.com/", max_links=50))