# Lottery Data Collection Summary

## Overview
Successfully scraped lottery data from NLB and DLB websites for all 17 Sri Lankan lotteries.

## Data Files Available

### Basic Lottery Data (17 files)
Located in `data/raw/`

**NLB Lotteries (8):**
- nlb_mahajana_sampatha.csv (215 draws)
- nlb_govisetha.csv (215 draws)
- nlb_dhana_nidhanaya.csv (81 draws)
- nlb_handahana.csv (81 draws)
- nlb_mega_power.csv (215 draws)
- nlb_ada_sampatha.csv (207 draws)
- nlb_suba_dawasak.csv (90 draws)
- nlb_nlb_jaya.csv (206 draws)

**DLB Lotteries (9):**
- dlb_shanida.csv (1,627 draws)
- dlb_lagna_wasana.csv (1,627 draws)
- dlb_super_ball.csv (946 draws)
- dlb_jayoda.csv (74 draws)
- dlb_ada_kotipathi.csv (772 draws)
- dlb_kapruka.csv (122 draws)
- dlb_sasiri.csv (773 draws)
- dlb_supiri_dhana_sampatha.csv (680 draws)
- dlb_jaya_sampatha.csv (154 draws)

**Total: 8,085 lottery draws**

### Prize Data (8 NLB files)
Located in `data/raw/` with `_with_prizes` suffix

**NLB Lotteries with Full Prize Data:**
- nlb_mahajana_sampatha_with_prizes.csv
- nlb_govisetha_with_prizes.csv
- nlb_dhana_nidhanaya_with_prizes.csv
- nlb_handahana_with_prizes.csv
- nlb_mega_power_with_prizes.csv
- nlb_ada_sampatha_with_prizes.csv
- nlb_suba_dawasak_with_prizes.csv
- nlb_nlb_jaya_with_prizes.csv

Each prize file includes:
- All basic draw data (date, numbers, etc.)
- Prize tier data: pattern, prize amount, winners, total payout
- 9-13 prize tiers per draw depending on lottery type

**DLB Prize Data:**
DLB displays prize information as PNG images which cannot be scraped programmatically.
Prize images are available at: `https://www.dlb.lk/front_img/{filename}.png`

## Data Fields

### Basic Data Columns
- source: nlb or dlb
- game: lottery game key
- game_name: full lottery name
- draw_id: unique draw identifier
- draw_date: draw date (YYYY-MM-DD format)
- letter: bonus letter (if applicable)
- numbers: winning numbers (semicolon-separated)
- raw_text: original text from website
- url: source URL

### Prize Data Columns (NLB only)
For each prize tier:
- {tier}_pattern: winning pattern (e.g., "6 Numbers Correct")
- {tier}_prize: prize amount
- {tier}_winners: number of winners
- {tier}_total: total payout

## Data Coverage

- **NLB**: Data from June 2025 to January 2026
- **DLB**: Data ranges from 2021 to January 2026 (varies by lottery)
- **Latest data**: Up to January 11-12, 2026

## Scripts

- `main.py`: Scrape all basic lottery data (17 lotteries)
- `scrape_with_prizes.py`: Scrape NLB lotteries with prize data (8 lotteries)

## Notes

1. DLB pagination may lag by 1 day for the most recent draws
2. Prize data is only available for NLB lotteries due to DLB's image-based display
3. All dates are in ISO format (YYYY-MM-DD)
4. Numbers are zero-padded and semicolon-separated
