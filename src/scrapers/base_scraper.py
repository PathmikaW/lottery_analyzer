"""
Base Scraper Class for Sri Lankan Lottery Data Collection
Provides common functionality for NLB and DLB scrapers
"""

import re
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser


class BaseLotteryScraper:
    """Base class for lottery scrapers with common utilities"""

    def __init__(self, base_url: str, session: Optional[requests.Session] = None):
        self.base_url = base_url
        self.session = session or requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def _fetch(self, path: str, max_retries: int = 3, retry_delay: int = 2) -> tuple:
        """
        Fetch a page with retry logic and cookie handling
        Returns: (url, BeautifulSoup object)
        """
        url = urljoin(self.base_url, path)

        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, headers=self.headers, timeout=30)
                resp.raise_for_status()

                # Handle bot protection (cookie setting)
                if 'setCookie' in resp.text and 'location.reload' in resp.text:
                    cookie_match = re.search(r"setCookie\('([^']+)','([^']+)'", resp.text)
                    if cookie_match:
                        cookie_name, cookie_value = cookie_match.groups()
                        domain = self.base_url.replace('https://', '').replace('http://', '')
                        self.session.cookies.set(cookie_name, cookie_value, domain=domain)

                    time.sleep(1)
                    resp = self.session.get(url, headers=self.headers, timeout=30)
                    resp.raise_for_status()

                return url, BeautifulSoup(resp.text, "html.parser")

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  Retry {attempt + 1}/{max_retries}: {e}")
                    time.sleep(retry_delay)
                else:
                    raise

    @staticmethod
    def clean_text(text: Optional[str]) -> str:
        """Clean and normalize text"""
        return re.sub(r"\s+", " ", (text or "")).strip()

    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """Extract all numbers from text"""
        return re.findall(r"\b\d+\b", text)

    @staticmethod
    def extract_date(text: str) -> Optional[str]:
        """Extract and parse date"""
        try:
            # Try to extract date pattern first (e.g., "2026-Jan-11" or "11-01-2026")
            date_patterns = [
                r'\d{4}-[A-Za-z]{3}-\d{1,2}',  # 2026-Jan-11
                r'\d{1,2}-\d{1,2}-\d{4}',       # 11-01-2026
                r'[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4}',  # January 11, 2026
            ]

            for pattern in date_patterns:
                match = re.search(pattern, text)
                if match:
                    date_str = match.group()
                    dt = dateparser.parse(date_str, fuzzy=True)
                    if dt:
                        return dt.date().isoformat()

            # Fallback: try parsing the whole text
            dt = dateparser.parse(text, fuzzy=True)
            return dt.date().isoformat() if dt else None
        except:
            return None

    @staticmethod
    def extract_letter(text: str) -> Optional[str]:
        """Extract single capital letter"""
        m = re.search(r"\b([A-Z])\b", text)
        return m.group(1) if m else None

    @staticmethod
    def normalize_number(num: str) -> str:
        """Format number as 2-digit (e.g., '5' -> '05')"""
        try:
            return f"{int(num):02d}"
        except:
            return num
