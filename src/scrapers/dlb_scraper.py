"""
DLB (Development Lotteries Board) Scraper
Scrapes all 9 DLB lotteries from www.dlb.lk
"""

from typing import List, Dict
from .base_scraper import BaseLotteryScraper


class DLBScraper(BaseLotteryScraper):
    """Scraper for Development Lotteries Board (DLB) lotteries"""

    BASE_URL = "https://www.dlb.lk"

    # All 9 DLB lotteries with their configurations (using numeric IDs)
    LOTTERIES = {
        "shanida": {
            "name": "Shanida",
            "path": "/result/1/",
            "lottery_id": 1,
            "numbers_count": 4,
        },
        "lagna_wasana": {
            "name": "Lagna Wasana",
            "path": "/result/2/",
            "lottery_id": 2,
            "numbers_count": 4,
        },
        "super_ball": {
            "name": "Super Ball",
            "path": "/result/3/",
            "lottery_id": 3,
            "numbers_count": 4,
        },
        "jayoda": {
            "name": "Jayoda",
            "path": "/result/6/",
            "lottery_id": 6,
            "numbers_count": 4,
        },
        "ada_kotipathi": {
            "name": "Ada Kotipathi",
            "path": "/result/11/",
            "lottery_id": 11,
            "numbers_count": 6,
        },
        "kapruka": {
            "name": "Kapruka",
            "path": "/result/12/",
            "lottery_id": 12,
            "numbers_count": 6,
        },
        "sasiri": {
            "name": "Sasiri",
            "path": "/result/13/",
            "lottery_id": 13,
            "numbers_count": 4,
        },
        "supiri_dhana_sampatha": {
            "name": "Supiri Dhana Sampatha",
            "path": "/result/17/",
            "lottery_id": 17,
            "numbers_count": 6,
        },
        "jaya_sampatha": {
            "name": "Jaya Sampatha",
            "path": "/result/18/",
            "lottery_id": 18,
            "numbers_count": 6,
        },
    }

    def __init__(self):
        super().__init__(self.BASE_URL)

    def _fetch_paginated(self, lottery_id: int, page: int, result_id: str) -> 'BeautifulSoup':
        """
        Fetch a specific page using DLB's AJAX pagination

        Args:
            lottery_id: DLB lottery ID (1-18)
            page: Page number (2+, page 1 is loaded via normal GET)
            result_id: The resultID from hidden input field

        Returns:
            BeautifulSoup object of the page content, or None on error
        """
        import time
        from bs4 import BeautifulSoup

        # DLB pagination endpoint
        url = f"{self.BASE_URL}/result/pagination_re"

        # POST data mimicking the AJAX call
        # Note: pagination is 0-indexed (page 2 in UI = pageId 1, page 3 = pageId 2, etc.)
        data = {
            'pageId': str(page - 1),  # Convert to 0-indexed
            'resultID': result_id,
            'lotteryID': str(lottery_id),
            'lastsegment': 'en'  # Language segment
        }

        # Add AJAX headers
        headers = self.headers.copy()
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Referer'] = f"{self.BASE_URL}/result/{lottery_id}/"

        try:
            resp = self.session.post(url, data=data, headers=headers, timeout=30)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, 'html.parser')
        except Exception as e:
            print(f"  Error fetching page {page}: {e}")
            return None

    def _parse_paginated_table(self, soup: 'BeautifulSoup', config: Dict, game: str, url: str) -> List[Dict]:
        """
        Parse paginated results (page 2+) which use table structure
        Each 7 cells = 1 draw (draw_info, empty, numbers, empty, empty, icon, button)

        Args:
            soup: BeautifulSoup object of paginated page
            config: Lottery configuration
            game: Game key
            url: Source URL

        Returns:
            List of draw results
        """
        results = []
        rows = soup.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 7:
                continue

            # Process every 7 cells as one draw
            for i in range(0, len(cells) - 6, 7):
                # Cell pattern: [draw_info, empty, numbers, empty, empty, icon, button]
                draw_cell = cells[i]
                numbers_cell = cells[i + 2]

                # Extract draw info (cell 0)
                draw_info_text = self.clean_text(draw_cell.get_text(" ", strip=True))
                if not draw_info_text or len(draw_info_text) < 10:
                    continue

                # Extract draw ID
                draw_nums = self.extract_numbers(draw_info_text)
                draw_id = None
                for num in draw_nums:
                    if 3 <= len(num) <= 5 and not (num.startswith('20') and len(num) == 4):
                        draw_id = num
                        break

                if not draw_id:
                    continue

                # Extract date
                draw_date = self.extract_date(draw_info_text)

                # Extract numbers from cell 2
                letter = None
                lottery_nums = []

                # Find ul.res_allnumber
                result_ul = numbers_cell.find('ul', class_='res_allnumber')
                if result_ul:
                    li_elements = result_ul.find_all('li')
                    for li in li_elements:
                        value = self.clean_text(li.get_text().strip())
                        if not value:
                            continue

                        # Single letter
                        if len(value) == 1 and value.isalpha():
                            letter = value.upper()
                        # Number
                        elif value.isdigit():
                            lottery_nums.append(value)

                # Validate we have enough numbers
                expected_count = config['numbers_count']
                if len(lottery_nums) < expected_count:
                    continue

                # Take first k numbers and format
                lottery_nums = lottery_nums[:expected_count]
                numbers = ";".join(self.normalize_number(n) for n in lottery_nums)

                # Store result
                results.append({
                    "source": "dlb",
                    "game": game,
                    "game_name": config['name'],
                    "draw_id": draw_id,
                    "draw_date": draw_date,
                    "letter": letter,
                    "numbers": numbers,
                    "raw_text": draw_info_text[:350],
                    "url": url,
                })

        return results

    def scrape_game(self, game: str, max_pages: int = 10) -> List[Dict]:
        """
        Scrape a specific DLB lottery game with pagination support
        DLB uses AJAX pagination - page 1 is loaded normally, pages 2+ via POST

        Args:
            game: Lottery game key (e.g., 'ada_kotipathi')
            max_pages: Maximum number of pages to scrape (default 10 for ~30 draws)

        Returns:
            List of draw results with draw_id, date, numbers, etc.
        """
        if game not in self.LOTTERIES:
            raise ValueError(f"Unknown game: {game}. Available: {list(self.LOTTERIES.keys())}")

        config = self.LOTTERIES[game]
        print(f"Scraping {config['name']}...")

        url, soup = self._fetch(config['path'])
        results = []

        # DLB structure: H3 tags for draw info, H6 tags for numbers
        # Each lottery result is grouped: 1 H3 followed by several H6 elements

        h3_tags = soup.find_all('h3')

        for h3 in h3_tags:
            # Extract draw info from H3
            draw_info_text = self.clean_text(h3.get_text(" ", strip=True))

            if not draw_info_text or len(draw_info_text) < 10:
                continue

            # Extract draw ID (3-5 digit number)
            draw_nums = self.extract_numbers(draw_info_text)
            draw_id = None
            for num in draw_nums:
                if 3 <= len(num) <= 5 and not (num.startswith('20') and len(num) == 4):
                    draw_id = num
                    break

            if not draw_id:
                continue

            # Extract date
            draw_date = self.extract_date(draw_info_text)

            # Find H6 tags within the result structure
            # DLB structure: H3 is in div.col-lg-4, numbers are in sibling div.col-lg-7
            # Both are children of div.lot_main_result
            letter = None
            lottery_nums = []

            # Go up to the grandparent (lot_main_result container)
            parent = h3.parent
            if parent:
                grandparent = parent.parent
                if grandparent:
                    # Find the ul.result_detail_result in the grandparent
                    result_ul = grandparent.find('ul', class_='result_detail_result')
                    if result_ul:
                        # Get all H6 tags from LI elements
                        li_elements = result_ul.find_all('li')
                        for li in li_elements:
                            h6 = li.find('h6')
                            if h6:
                                value = self.clean_text(h6.get_text().strip())

                                if not value:
                                    continue

                                # Single letter
                                if len(value) == 1 and value.isalpha():
                                    letter = value.upper()
                                # Number
                                elif value.isdigit():
                                    lottery_nums.append(value)

            # Validate we have enough numbers
            expected_count = config['numbers_count']
            if len(lottery_nums) < expected_count:
                continue

            # Take first k numbers and format
            lottery_nums = lottery_nums[:expected_count]
            numbers = ";".join(self.normalize_number(n) for n in lottery_nums)

            # Store result
            results.append({
                "source": "dlb",
                "game": game,
                "game_name": config['name'],
                "draw_id": draw_id,
                "draw_date": draw_date,
                "letter": letter,
                "numbers": numbers,
                "raw_text": draw_info_text[:350],
                "url": url,
            })

        # Pagination: fetch additional pages if max_pages > 1
        if max_pages > 1:
            # Extract resultID from page 1 for pagination
            lottery_id = config['lottery_id']
            result_input = soup.find('input', id=f'resultID{lottery_id}')
            result_id = result_input.get('value') if result_input else None

            if result_id:
                import time
                for page_num in range(2, max_pages + 1):
                    # Rate limiting
                    time.sleep(0.5)

                    page_soup = self._fetch_paginated(lottery_id, page_num, result_id)
                    if page_soup:
                        page_results = self._parse_paginated_table(page_soup, config, game, url)
                        results.extend(page_results)

                        # Stop if we got no results (end of data)
                        if len(page_results) == 0:
                            break
            else:
                print(f"  Warning: Could not find resultID for pagination")

        # Remove duplicates
        unique_results = {}
        for r in results:
            key = (r["draw_id"], r["numbers"])
            if key not in unique_results:
                unique_results[key] = r

        print(f"  Found {len(unique_results)} draws for {config['name']}")
        return list(unique_results.values())

    def scrape_all(self) -> Dict[str, List[Dict]]:
        """Scrape all 9 DLB lotteries"""
        all_results = {}
        for game in self.LOTTERIES:
            try:
                all_results[game] = self.scrape_game(game)
            except Exception as e:
                print(f"  Error scraping {game}: {e}")
                all_results[game] = []
        return all_results
