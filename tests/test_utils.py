import pytest

from src.utils import extract_data, fetch_page, get_total_pages
from unittest.mock import patch, Mock
from src.model import Data


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


@pytest.mark.asyncio
async def test_extract_data_mock():
    html = """
    <div class="Bdb(borderSolidLightGrey)">
        <span class="Mstart(8px)">Activity 1</span>
        <div class="Fw(500) C(c-primary) Fz(18px) Mb(10px) nightmode_C(c-primary-night)">Title 1</div>
        <div class="C(c-secondary) Lh(1.5) nightmode_C(c-secondary-night)">Content 1</div>
        <div class="C(c-tertiary) nightmode_C(c-tertiary-night)">Status Content 1</div>
        <a href="/link1">Link 1</a>
    </div>
    <div class="Bdb(borderSolidLightGrey)">
        <span class="Mstart(8px)">Activity 2</span>
        <div class="Fw(500) C(c-primary) Fz(18px) Mb(10px) nightmode_C(c-primary-night)">Title 2</div>
        <div class="C(c-secondary) Lh(1.5) nightmode_C(c-secondary-night)">Content 2</div>
        <div class="C(c-tertiary) nightmode_C(c-tertiary-night)">Status Content 2</div>
        <a href="/link2">Link 2</a>
    </div>
    """
    data = await extract_data(html)
    assert len(data) == 2
    assert data[0].activity == "Activity 1"
    assert data[0].title == "Title 1"
    assert data[0].content == "Content 1"
    assert data[0].status_content == "Status Content 1"
    assert data[0].link == "https://m.kaskus.co.id/link1"
    assert data[1].activity == "Activity 2"
    assert data[1].title == "Title 2"
    assert data[1].content == "Content 2"
    assert data[1].status_content == "Status Content 2"
    assert data[1].link == "https://m.kaskus.co.id/link2"
