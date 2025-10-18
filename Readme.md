# Web Crawler

A fast and efficient asynchronous web crawler built with Python that discovers and stores web pages from a given domain using BFS (Breadth-First Search) algorithm.

## Features

- **Asynchronous crawling** using `aiohttp` for high performance
- **BFS-based traversal** to systematically explore websites
- **Database persistence** with PostgreSQL for storing crawled content
- **Same-domain filtering** to stay within the target website
- **Duplicate prevention** using URL uniqueness constraints
- **Configurable crawl depth** to limit the number of pages crawled

## Requirements

- Python 3.7+
- PostgreSQL database
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Saiyashwanth7/Web-Crawler.git
   cd web-crawler
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your PostgreSQL connection string:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/crawler_db
   ```

5. Initialize the database:
   ```bash
   python crawler.py
   ```

## Usage

Run the crawler with your target URL:

```python
asyncio.run(main("https://example.com/"))
```

The crawler will:
- Start from the seed URL
- Discover all links on each page
- Filter links to the same domain
- Store HTML content and metadata in the database
- Crawl up to 50 pages (configurable via `max_links`)

## Project Structure

- **`crawler.py`** - Main crawler logic with async URL fetching and BFS traversal
- **`database.py`** - PostgreSQL database configuration and session management
- **`models.py`** - SQLAlchemy ORM model for storing crawled content
- **`requirements.txt`** - Python package dependencies

## Database Schema

The `ContentStorage` table stores:
- `id` - Primary key
- `url` - Unique URL (prevents duplicates)
- `html_content` - Full HTML of the page
- `status_code` - HTTP response status
- `method_name` - Crawling method (default: 'aiohttp')
- `crawled_at` - Timestamp of when the page was crawled

## Configuration

Modify these settings in `crawler.py`:

- **`max_links`** - Maximum number of pages to crawl (default: 50)
- **Seed URL** - Change the URL passed to `main()`
- **Database** - Update `.env` with your PostgreSQL credentials

## Example

```python
asyncio.run(main("http://quotes.toscrape.com/"))
```

## Error Handling

- Duplicate URLs are skipped with a warning message
- Database errors are rolled back automatically
- All exceptions are logged for debugging

## Future Enhancements

- Configurable crawl limits and filters
- Support for robots.txt and sitemap.xml
- Rate limiting and request delays
- Cookie and session handling
- JavaScript rendering support

## License

MIT
