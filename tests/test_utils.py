import pytest

from src.utils import extract_data, fetch_page, get_total_pages


@pytest.mark.asyncio
async def test_get_total_pages():
    total_pages = await get_total_pages("admin")
    assert total_pages == 50


@pytest.mark.asyncio
async def test_fetch_page():
    page = await fetch_page("admin", 1)
    assert "KASKUS" in page


@pytest.mark.asyncio
async def test_extract_data():
    html = await fetch_page("admin", 1)
    data = await extract_data(html)
    assert len(data) == 20
