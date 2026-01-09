"""
DLB (Development Lotteries Board) Scraper
Scrapes all 9 DLB lotteries from www.dlb.lk
"""

from typing import List, Dict
from .base_scraper import BaseLotteryScraper


class DLBScraper(BaseLotteryScraper):
    """Scraper for Development Lotteries Board (DLB) lotteries"""

    BASE_URL = "https://www.dlb.lk"

    # All 9 DLB lotteries with their configurations
    LOTTERIES = {
        "ada_kotipathi": {
            "name": "Ada Kotipathi",
            "path": "/results/ada-kotipathi",
            "numbers_count": 6,
        },
        "shanida": {
            "name": "Shanida",
            "path": "/results/shanida",
            "numbers_count": 5,
        },
        "lagna_wasana": {
            "name": "Lagna Wasana",
            "path": "/results/lagna-wasana",
            "numbers_count": 4,
        },
        "supiri_dhana_sampatha": {
            "name": "Supiri Dhana Sampatha",
            "path": "/results/supiri-dhana-sampatha",
            "numbers_count": 6,
        },
        "super_ball": {
            "name": "Super Ball",
            "path": "/results/super-ball",
            "numbers_count": 5,
        },
        "kapruka": {
            "name": "Kapruka",
            "path": "/results/kapruka",
            "numbers_count": 6,
        },
        "jayoda": {
            "name": "Jayoda",
            "path": "/results/jayoda",
            "numbers_count": 5,
        },
        "sasiri": {
            "name": "Sasiri",
            "path": "/results/sasiri",
            "numbers_count": 4,
        },
        "jaya_sampatha": {
            "name": "Jaya Sampatha",
            "path": "/results/jaya-sampatha",
            "numbers_count": 6,
        },
    }

    def __init__(self):
        super().__init__(self.BASE_URL)

    def scrape_game(self, game: str) -> List[Dict]:
        """
        Scrape a specific DLB lottery game

        Args:
            game: Lottery game key (e.g., 'ada_kotipathi')

        Returns:
            List of draw results with draw_id, date, numbers, etc.
        """
        if game not in self.LOTTERIES:
            raise ValueError(f"Unknown game: {game}. Available: {list(self.LOTTERIES.keys())}")

        config = self.LOTTERIES[game]
        print(f"Scraping {config['name']}...")

        url, soup = self._fetch(config['path'])
        results = []

        # Find all table rows with draw results
        table_rows = soup.select("table tr")

        for row in table_rows:
            cells = row.select("td")
            if len(cells) < 2:
                continue

            # Cell 1: draw ID and date
            cell1_text = self.clean_text(cells[0].get_text(" ", strip=True))
            # Cell 2: letter and numbers
            cell2_text = self.clean_text(cells[1].get_text(" ", strip=True))

            if not cell1_text or not cell2_text:
                continue

            # Extract draw ID (4-5 digit number)
            cell1_nums = self.extract_numbers(cell1_text)
            draw_id = None
            for num in cell1_nums:
                if len(num) >= 4 and not (num.startswith('20') and len(num) == 4):
                    draw_id = num
                    break

            if not draw_id:
                continue

            # Extract date (remove draw ID first)
            date_text = cell1_text.replace(draw_id, "", 1).strip()
            draw_date = self.extract_date(date_text)

            # Extract letter
            letter = self.extract_letter(cell2_text)

            # Extract lottery numbers from <li> elements
            li_elements = cells[1].select("li")
            lottery_nums = []

            if li_elements:
                for li in li_elements:
                    li_text = self.clean_text(li.get_text().strip())
                    # Skip letter elements
                    if len(li_text) == 1 and li_text.isalpha():
                        continue
                    if li_text.isdigit():
                        lottery_nums.append(li_text)
            else:
                # Fallback: extract from text
                cell2_nums = self.extract_numbers(cell2_text)
                lottery_nums = [n for n in cell2_nums if len(n) <= 2]

            # Validate number count
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
                "raw_text": f"{cell1_text} {cell2_text}"[:350],
                "url": url,
            })

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
