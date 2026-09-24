# Blocket.se Scraper - Swedish Classifieds & Marketplace

Extract listings from **Blocket.se**, Sweden's largest classifieds marketplace. Scrape products, vehicles, real estate, services, and more with prices, locations, and images across all Swedish regions.

## Features

- ✅ Search by keyword, category, location, and price range
- ✅ Extract titles, prices, locations, images, and listing URLs
- ✅ Support for all Swedish regions (hela_sverige, Stockholm, Göteborg, Malmö, etc.)
- ✅ Filter by minimum/maximum price
- ✅ Residential proxy support for reliable access
- ✅ Compatible with **Claude**, **ChatGPT** & **AI agents via Apify MCP**

## Use Cases

1. **Price Monitoring** - Track prices for bikes, electronics, cars across Sweden
2. **Market Research** - Analyze supply/demand for specific products or regions
3. **Lead Generation** - Find sellers of equipment, vehicles, real estate
4. **Competitive Analysis** - Monitor competitor pricing and inventory
5. **AI Agent Integration** - Feed structured Swedish marketplace data to Claude/ChatGPT workflows

## Input Parameters

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `searchQuery` | string | Search term (Swedish keywords) | `"cykel"`, `"bil"`, `"laptop"` |
| `location` | string | Region in Sweden | `"hela_sverige"`, `"stockholm"`, `"goteborg"` |
| `category` | string | Blocket category ID (optional) | `"0.69"` (Sport), `"0.78"` (Furniture) |
| `minPrice` | integer | Minimum price in SEK | `1000` |
| `maxPrice` | integer | Maximum price in SEK | `50000` |
| `maxResults` | integer | Max listings to scrape (1-500) | `50` |

## Output Fields

Each result contains:
- `url` - Full listing URL
- `itemId` - Blocket item ID
- `title` - Listing title
- `price` - Price in Swedish Kronor (SEK)
- `priceText` - Original price text
- `location` - City/region
- `imageUrl` - Main image URL
- `scrapedAt` - ISO 8601 timestamp

## Example

**Input:**
```json
{
  "searchQuery": "cykel",
  "location": "stockholm",
  "maxPrice": 5000,
  "maxResults": 20
}
```

**Output:**
```json
{
  "url": "https://www.blocket.se/recommerce/forsale/item/26800531",
  "itemId": "26800531",
  "title": "Helt ny oanvänd cykel 28\" Medium",
  "price": 2500,
  "priceText": "2 500 kr",
  "location": "Västerås",
  "imageUrl": "https://images.blocketcdn.se/...",
  "scrapedAt": "2026-09-24T11:30:00.000Z"
}
```

## Pricing

- **$0.005 per result** scraped
- **$0.05 per actor start** (one-time fee per run)

Example: 100 results = $0.50 (results) + $0.05 (start) = **$0.55 total**

## AI Agent Integration (MCP)

This actor is **Claude Code** and **ChatGPT** compatible via the Apify MCP server:

```bash
# Install Apify MCP
npm install -g @apify/mcp-server

# Use in Claude Desktop / ChatGPT
"Tell me the average price for bikes in Stockholm on Blocket.se"
```

The AI agent will automatically run this scraper and analyze the results.

## FAQ

**Q: Does this work for all of Sweden?**  
A: Yes - use `location: "hela_sverige"` or specify regions like `stockholm`, `goteborg`, `malmo`, `uppsala`, etc.

**Q: Can I filter by category?**  
A: Yes - categories like `0.69` (Sport), `0.78` (Furniture), `0.93` (Electronics). Leave empty to search all categories.

**Q: How often is data updated?**  
A: Real-time - the scraper fetches live listings from Blocket.se at the time of each run.

**Q: What if a listing has no price?**  
A: The `price` field will be `null`, but `priceText` may contain contact-based pricing info.

## Notes

- Blocket.se uses Swedish number formatting (spaces as thousand separators: `1 000 kr`)
- Some listings require registration to view full details
- Residential proxies recommended for high-volume scraping

## Support

For issues or feature requests, visit:  
https://github.com/roshtarg-cpu/blocket-se-scraper

---

**Compatible with Claude, ChatGPT & AI agents via Apify MCP.**
