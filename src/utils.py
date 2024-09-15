from typing import List

import requests
from bs4 import BeautifulSoup

from src.model import Data


async def get_total_pages(username: str) -> int:
    headers = {
        "referer": f"https://m.kaskus.co.id/@{username}",
        "origin": "https://m.kaskus.co.id",
    }
    resp = requests.get(
        f"https://m.kaskus.co.id/@{username}/viewallposts/", headers=headers
    )
    soup = BeautifulSoup(resp.text, "html.parser")
    pagination = soup.select_one(".c-pagination")
    if pagination:
        return int(pagination.contents[0].text.split()[3])
    return 1


async def fetch_page(username: str, page: int) -> str:
    resp = requests.get(
        f"https://m.kaskus.co.id/@{username}/viewallposts/{page}/?sort=desc"
    )
    return resp.text


async def extract_data(html: str) -> List[Data]:
    soup = BeautifulSoup(html, "html.parser")

    cards_class = "Bdb(borderSolidLightGrey)"
    cards = soup.select(f'div[class*="{cards_class}"]')

    content = []
    for card in cards:
        activity_class = "Mstart(8px)"
        activity = card.select_one(f'span[class*="{activity_class}"]').text

        title_class = (
            "Fw(500) C(c-primary) Fz(18px) Mb(10px) nightmode_C(c-primary-night)"
        )
        title = card.select_one(f'div[class*="{title_class}"]').text

        content_class = "C(c-secondary) Lh(1.5) nightmode_C(c-secondary-night)"
        content_text = card.select_one(f'div[class*="{content_class}"]')
        content_text = content_text.text if content_text else None

        status_content_class = "C(c-tertiary) nightmode_C(c-tertiary-night)"
        status_content_elem = card.select_one(f'div[class*="{status_content_class}"]')
        status_content = status_content_elem.text if status_content_elem else None

        link_elem = card.select_one("a")
        link = f'https://m.kaskus.co.id{link_elem["href"]}' if link_elem else None

        result = {
            "activity": activity,
            "title": title,
            "content": content_text,
            "status_content": status_content,
            "link": link,
        }

        try:
            parsed = Data(**result)
            content.append(parsed)
        except ValueError as e:
            print(result)
            print(f"Validation error: {e}")

    return content
