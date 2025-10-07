
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NLB-Lottery-Scraper/1.0; +edu)"}

def _clean(s: Optional[str]) -> str:
    import re
    return re.sub(r"\s+", " ", (s or "")).strip()

def _extract_numbers(text: str) -> List[str]:
    import re
    return re.findall(r"\b\d+\b", text)

def _extract_date(text: str) -> Optional[str]:
    try:
        dt = dateparser.parse(text, dayfirst=True, fuzzy=True)
        if dt:
            return dt.date().isoformat()
        return None
    except Exception:
        return None

def _extract_letter(text: str) -> Optional[str]:
    import re
    m = re.search(r"\b([A-Z])\b", text)
    return m.group(1) if m else None

def _nz(num: str) -> str:
    try:
        return f"{int(num):02d}"
    except Exception:
        return num

class NLBScraper:
    BASE = "https://www.nlb.lk"
    GAME_PATHS = {
        "mahajana_sampatha": "/results/mahajana-sampatha",
        "govisetha": "/results/govisetha",
    }
    GAME_COUNTS = {"mahajana_sampatha": 6, "govisetha": 4}

    def __init__(self, session: Optional[requests.Session] = None, fetch_prizes: bool = False):
        self.s = session or requests.Session()
        self.fetch_prizes = fetch_prizes

    def _fetch(self, path: str):
        url = urljoin(self.BASE, path)
        # First request to get cookie
        resp = self.s.get(url, headers=HEADERS, timeout=25)
        resp.raise_for_status()

        # Check if we got a cookie-setting response
        if 'setCookie' in resp.text and 'location.reload' in resp.text:
            # Extract and set the cookie manually
            import re
            cookie_match = re.search(r"setCookie\('([^']+)','([^']+)'", resp.text)
            if cookie_match:
                cookie_name = cookie_match.group(1)
                cookie_value = cookie_match.group(2)
                self.s.cookies.set(cookie_name, cookie_value, domain='www.nlb.lk')

            # Make the second request with the cookie
            resp = self.s.get(url, headers=HEADERS, timeout=25)
            resp.raise_for_status()

        from bs4 import BeautifulSoup
        return url, BeautifulSoup(resp.text, "html.parser")

    def _scrape_prize_structure(self, game: str, draw_id: str) -> Dict:
        """Scrape prize structure for a specific draw"""
        url, soup = self._fetch(f"{self.GAME_PATHS[game]}/{draw_id}")
        prize_data = {}

        # Find the prize structure table (div with class tStruct)
        prize_table = soup.select_one("div.tStruct")
        if not prize_table:
            return prize_data

        # The structure is: tStruct > [thead, content_div, tfoot]
        # Get the second child which contains all prize rows
        children = prize_table.find_all('div', recursive=False)
        if len(children) < 2:
            return prize_data

        content_div = children[1]  # Second child contains prize rows
        prize_rows = content_div.find_all('div', recursive=False)

        for row in prize_rows:
            # Each row has 5 inner divs: rank, pattern, prize, winners, total
            cells = row.find_all('div', recursive=False)
            if len(cells) < 5:
                continue

            # Extract: rank, pattern, prize, winners, total
            rank = _clean(cells[0].get_text())
            pattern = _clean(cells[1].get_text())
            prize_amount = _clean(cells[2].get_text())
            winners = _clean(cells[3].get_text())
            total_payout = _clean(cells[4].get_text())

            # Create column names from rank (e.g., "Super Prize" -> "super_prize", "1 st" -> "1")
            rank_key = rank.lower().replace(" ", "_").replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").strip("_")
            if not rank_key:
                continue

            # Store prize data
            prize_data[f"{rank_key}_pattern"] = pattern
            prize_data[f"{rank_key}_prize"] = prize_amount
            prize_data[f"{rank_key}_winners"] = winners
            prize_data[f"{rank_key}_total"] = total_payout

        return prize_data

    def scrape_game(self, game: str) -> List[Dict]:
        assert game in self.GAME_PATHS, f"Unsupported game: {game}"
        url, soup = self._fetch(self.GAME_PATHS[game])
        results: List[Dict] = []

        table_rows = soup.select("table tr")

        for row in table_rows:
            cells = row.select("td")
            if len(cells) < 2:
                continue

            # First cell contains draw ID and date
            cell1_text = _clean(cells[0].get_text(" ", strip=True))
            # Second cell contains letter and numbers
            cell2_text = _clean(cells[1].get_text(" ", strip=True))

            if not cell1_text or not cell2_text:
                continue

            # Extract draw ID from first cell (first number, 4-5 digits)
            cell1_nums = _extract_numbers(cell1_text)
            draw_id = None
            for num in cell1_nums:
                if len(num) >= 4 and not (num.startswith('20') and len(num) == 4):
                    draw_id = num
                    break

            if not draw_id:
                continue

            # Extract date from first cell (skip draw ID)
            # Remove draw ID from text before parsing date
            date_text = cell1_text
            if draw_id in date_text:
                date_text = date_text.replace(draw_id, "", 1).strip()
            draw_date = _extract_date(date_text)

            # Extract letter from second cell (single capital letter)
            letter = _extract_letter(cell2_text)

            # Extract lottery numbers from second cell
            # Try structured extraction from <li> elements first
            li_elements = cells[1].select("li")
            lottery_nums = []

            if li_elements:
                for li in li_elements:
                    li_text = _clean(li.get_text().strip())
                    # Skip the letter element
                    if len(li_text) == 1 and li_text.isalpha():
                        continue
                    # Extract numbers
                    if li_text.isdigit():
                        lottery_nums.append(li_text)
            else:
                # Fallback: extract from text
                cell2_nums = _extract_numbers(cell2_text)
                # Filter to reasonable lottery numbers (1-2 digits)
                lottery_nums = [n for n in cell2_nums if len(n) <= 2]

            k = self.GAME_COUNTS[game]
            if len(lottery_nums) < k:
                continue

            # Take first k numbers
            lottery_nums = lottery_nums[:k]
            numbers = ";".join(_nz(n) for n in lottery_nums)

            # Combine text for raw_text
            raw_text = f"{cell1_text} {cell2_text}"

            result_data = {
                "source": "nlb",
                "game": game,
                "draw_id": draw_id,
                "draw_date": draw_date,
                "letter": letter,
                "numbers": numbers,
                "raw_text": raw_text[:350],
                "url": url,
            }

            # Optionally fetch prize structure
            if self.fetch_prizes and draw_id:
                print(f"  Fetching prize data for draw {draw_id}...")
                prize_data = self._scrape_prize_structure(game, draw_id)
                result_data.update(prize_data)

            results.append(result_data)

        uniq = {}
        for r in results:
            key = (r.get("draw_id"), r.get("numbers"))
            if key not in uniq:
                uniq[key] = r
        return list(uniq.values())
