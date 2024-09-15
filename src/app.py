import pandas as pd

from src.model import Data
from src.utils import extract_data, fetch_page, get_total_pages


async def main():
    username = input("Enter username: ")
    totalPage = await get_total_pages(username)
    print(f"[+] Total pages for {username}: {totalPage}")

    data: list[Data] = []

    for i in range(1, totalPage + 1):
        print(f"[+] Fetching page {i}...")
        page = await fetch_page(username, i)
        content = await extract_data(page)
        data.extend(content)

    df = pd.DataFrame([d.dict() for d in data])

    output_file = f"{username}-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    df.to_excel(output_file, index=False)
    print("[+] Done!")
    print(f"[+] Data saved to {output_file}")
