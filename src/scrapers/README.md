# Sri Lankan Lottery Data Scrapers

Web scrapers for collecting historical lottery draw data from Sri Lanka's lottery boards.

## Overview

This module scrapes data from **17 Sri Lankan lotteries**:
- **8 NLB (National Lotteries Board)** lotteries
- **9 DLB (Development Lotteries Board)** lotteries

## Features

- ✅ Handles bot protection (cookie-based challenges)
- ✅ Retry logic with exponential backoff
- ✅ Rate limiting to avoid overwhelming servers
- ✅ Duplicate detection and removal
- ✅ CSV export for each lottery
- ✅ Comprehensive error handling

## Usage

### Scrape All Lotteries

```bash
python run_scrapers.py --all
```

This will scrape all 17 lotteries and save individual CSV files to `data/raw/`.

### Scrape Single Lottery

```bash
# NLB lottery
python run_scrapers.py --source nlb --game mahajana_sampatha

# DLB lottery
python run_scrapers.py --source dlb --game ada_kotipathi
```

### List Available Lotteries

```bash
python run_scrapers.py --list
```

### Custom Output Directory

```bash
python run_scrapers.py --all --output my_data/
```

## Available Lotteries

### NLB Lotteries
1. `mahajana_sampatha` - Mahajana Sampatha (6 numbers)
2. `govisetha` - Govisetha (4 numbers)
3. `dhana_nidhanaya` - Dhana Nidhanaya (5 numbers)
4. `handahana` - Handahana (6 numbers)
5. `mega_power` - Mega Power (5 numbers)
6. `ada_sampatha` - Ada Sampatha (6 numbers)
7. `suba_dawasak` - Suba Dawasak (5 numbers)
8. `nlb_jaya` - NLB Jaya (4 numbers)

### DLB Lotteries
1. `ada_kotipathi` - Ada Kotipathi (4 numbers)
2. `shanida` - Shanida (4 numbers)
3. `lagna_wasana` - Lagna Wasana (4 numbers)
4. `supiri_dhana_sampatha` - Supiri Dhana Sampatha (6 numbers)
5. `super_ball` - Super Ball (4 numbers)
6. `kapruka` - Kapruka (5 numbers)
7. `jayoda` - Jayoda (4 numbers)
8. `sasiri` - Sasiri (3 numbers)
9. `jaya_sampatha` - Jaya Sampatha (4 numbers)

## Output Format

### Standard CSV Format

Each CSV file contains the following columns:

| Column | Description |
|--------|-------------|
| `source` | Lottery board (nlb or dlb) |
| `game` | Game key (e.g., mahajana_sampatha) |
| `game_name` | Full game name |
| `draw_id` | Draw number (4-5 digits) |
| `draw_date` | Date in YYYY-MM-DD format |
| `letter` | Bonus letter (if applicable) |
| `numbers` | Winning numbers (semicolon-separated, e.g., "03;09;15;21;27;33") |
| `raw_text` | Original text from website |
| `url` | Source URL |

Example:
```csv
source,game,game_name,draw_id,draw_date,letter,numbers,raw_text,url
nlb,mahajana_sampatha,Mahajana Sampatha,6068,2026-01-08,M,03;03;09;06;07;03,"6068 Thursday January 08, 2026 M 3 3 9 6 7 3",https://www.nlb.lk/results/mahajana-sampatha
```

**Note**: This project focuses on number prediction analysis. Prize data collection features are not included as they are not relevant for the ML prediction task.

## Implementation Details

### Base Scraper
- `base_scraper.py`: Common functionality for all scrapers
  - HTTP request handling with retries
  - Bot protection bypass (cookie handling)
  - Text cleaning and number extraction utilities
  - Date parsing

### Lottery-Specific Scrapers
- `nlb_scraper.py`: Scrapes 9 NLB lotteries
- `dlb_scraper.py`: Scrapes 9 DLB lotteries

### Scraper Manager
- `scraper_manager.py`: Orchestrates all scrapers
  - Manages scraping sequence
  - Handles errors gracefully
  - Generates summary reports
  - Saves data to CSV

## Error Handling

The scrapers implement robust error handling:

1. **Network Errors**: Retries up to 3 times with 2-second delays
2. **Bot Protection**: Automatically handles cookie-based challenges
3. **Parsing Errors**: Logs errors but continues with other lotteries
4. **Missing Data**: Skips invalid rows, reports at the end

## Rate Limiting

To be respectful to the lottery board servers:
- 1-second delay between requests
- Maximum 3 retries per request
- Exponential backoff on failures

## Dependencies

```
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dateutil>=2.8.2
lxml>=4.9.0
```

## Data Collection Timeline

As per assignment requirements, we aim to collect:
- **Time Period**: Last 7 months (June 2024 - January 2025)
- **Target**: 3,500-4,000 total draws
- **Per Lottery**: 60-210 draws (depending on draw frequency)

## Troubleshooting

### No data scraped
- Check internet connection
- Verify website is accessible (https://www.nlb.lk, https://www.dlb.lk)
- Check if website structure has changed

### Bot protection errors
- The scraper handles cookie-based protection automatically
- If issues persist, increase retry delays in `base_scraper.py`

### Slow scraping
- Normal for 18 lotteries (takes 5-10 minutes)
- Rate limiting is intentional to avoid server overload

## Usage Example

```python
from src.scrapers.nlb_scraper import NLBScraper
from src.scrapers.dlb_scraper import DLBScraper

# Scrape NLB lottery draws
nlb = NLBScraper()
results = nlb.scrape_game('govisetha')

# Scrape DLB lottery draws
dlb = DLBScraper()
results = dlb.scrape_game('shanida')
```

## Future Enhancements

- [ ] Incremental updates (only scrape new draws)
- [ ] Data validation and quality checks
- [ ] Export to other formats (JSON, Parquet)
- [ ] Automated scheduling (cron jobs)

## License

Educational use only - for MSc AI assignment.
