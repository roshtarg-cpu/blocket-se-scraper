import asyncio
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urljoin, urlparse, parse_qs

from apify import Actor
from camoufox.async_api import AsyncCamoufox
from bs4 import BeautifulSoup

async def main():
    async with Actor:
        # NO await on Actor.get_env() - SDK 4.x synchronous
        env = Actor.get_env()
        actor_input = await Actor.get_input() or {}
        
        # NO await on Actor.log - synchronous
        Actor.log.info(f"Actor started with input: {actor_input}")
        
        # Input parameters
        search_query = actor_input.get('searchQuery', '')
        category = actor_input.get('category', '')
        location = actor_input.get('location', 'hela_sverige')
        min_price = actor_input.get('minPrice')
        max_price = actor_input.get('maxPrice')
        max_results = actor_input.get('maxResults', 50)
        
        # Build search URL
        base_url = f"https://www.blocket.se/annonser/{location}"
        params = []
        if search_query:
            params.append(f"q={search_query}")
        if category:
            params.append(f"category={category}")
        if min_price:
            params.append(f"price_from={min_price}")
        if max_price:
            params.append(f"price_to={max_price}")
        
        start_url = base_url + ("?" + "&".join(params) if params else "")
        Actor.log.info(f"Starting URL: {start_url}")
        
        items_scraped = 0
        
        async with AsyncCamoufox(headless=True, geoip=True) as browser:
            page = await browser.new_page()
            
            try:
                await page.goto(start_url, wait_until='domcontentloaded', timeout=60000)
                await asyncio.sleep(3)  # Let JS render
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extract listings - multiple strategies
                containers = set()
                
                # Strategy 1: Links to item pages
                for link in soup.find_all('a', href=re.compile(r'/recommerce/forsale/item/\d+')):
                    containers.add(link)
                
                # Strategy 2: Article tags
                for article in soup.find_all('article'):
                    if article.find('a', href=re.compile(r'/item/\d+')):
                        containers.add(article)
                
                # Strategy 3: Data attributes
                for elem in soup.find_all(attrs={'data-testid': re.compile(r'listing|card|item')}):
                    containers.add(elem)
                
                Actor.log.info(f"Found {len(containers)} listing containers")
                
                for container in list(containers)[:max_results]:
                    try:
                        # Extract item URL
                        link_elem = container if container.name == 'a' else container.find('a', href=re.compile(r'/item/\d+'))
                        if not link_elem:
                            continue
                        
                        item_url = urljoin("https://www.blocket.se", link_elem.get('href'))
                        item_id = re.search(r'/item/(\d+)', item_url)
                        item_id = item_id.group(1) if item_id else None
                        
                        # Extract title
                        title_elem = container.find(['h1', 'h2', 'h3', 'span'])
                        title = title_elem.get_text(strip=True) if title_elem else None
                        
                        # Extract price
                        price_text = None
                        for price_elem in container.find_all(string=re.compile(r'\d+\s*kr')):
                            price_text = price_elem.strip()
                            break
                        
                        price = None
                        if price_text:
                            price_match = re.search(r'([\d\s\xa0]+)\s*kr', price_text)
                            if price_match:
                                # Remove spaces and non-breaking spaces (Swedish number format)
                                price = int(price_match.group(1).replace(' ', '').replace('\xa0', ''))
                        
                        # Extract location (city name)
                        location_text = None
                        for text_node in container.stripped_strings:
                            # Look for Swedish city names or location patterns
                            if len(text_node) < 30 and not any(char.isdigit() for char in text_node):
                                if text_node not in ['kr', 'Lägg till i favoriter', 'Gå till annonsen']:
                                    location_text = text_node
                                    break
                        
                        # Extract image URL
                        image_url = None
                        img = container.find('img')
                        if img:
                            image_url = img.get('src') or img.get('data-src')
                        
                        # Build result
                        result = {
                            'url': item_url,
                            'itemId': item_id,
                            'title': title,
                            'price': price,
                            'priceText': price_text,
                            'location': location_text,
                            'imageUrl': image_url,
                            'scrapedAt': datetime.now(timezone.utc).isoformat()
                        }
                        
                        await Actor.push_data(result)
                        items_scraped += 1
                        
                        if items_scraped >= max_results:
                            break
                    
                    except Exception as e:
                        Actor.log.warning(f"Failed to extract listing: {e}")
                        continue
            
            except Exception as e:
                Actor.log.error(f"Failed to load page: {e}")
            
            finally:
                await page.close()
        
        Actor.log.info(f"Scraping completed. Total items: {items_scraped}")
        
        # Save task metadata
        await Actor.set_value('SAVED-TASK', {
            'actorId': env.actor_id,
            'actorRunId': env.actor_run_id,
            'defaultDatasetId': env.default_dataset_id,
            'startedAt': env.started_at.isoformat() if env.started_at else None,
            'input': actor_input,
            'stats': {
                'itemsScraped': items_scraped
            }
        })
