
import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from urllib.parse import urlparse, urlencode

SEARCH_URL = "https://www.linkedin.com/search/results/people/?"

async def ensure_second_tab(context):
    # Check number of open tabs/pages
    if len(context.pages) < 2:
        new_page = await context.new_page()
        print("Opened a new tab")
        return new_page
    else:
        print("Already have 2 or more tabs open")
        return context.pages[-1]
    
async def get_people(browser, context, page, company):
    searchpage = await ensure_second_tab(context)
    
    qse = f'{company} Software Engineer'
    await searchpage.goto(f'{SEARCH_URL}{urlencode({"keywords":qse})}')
    se = await searchpage.locator(
        "xpath=/html/body/div/div[2]/div[2]/div[2]/main/div/div/div/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div/div/a"
    ).first.get_attribute('href')
    sename = await searchpage.locator(
        "xpath=/html/body/div/div[2]/div[2]/div[2]/main/div/div/div/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div/div/a/div/div/div[1]/p/a"
    ).first.text_content()

    qhm = f'{company} Hiring Manager'
    await searchpage.goto(f'{SEARCH_URL}{urlencode({"keywords":qhm})}')
    hm = await searchpage.locator(
        "xpath=/html/body/div/div[2]/div[2]/div[2]/main/div/div/div/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div/div/a"
    ).first.get_attribute('href')
    hmname = await searchpage.locator(
        "xpath=/html/body/div/div[2]/div[2]/div[2]/main/div/div/div/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div/div/a/div/div/div[1]/p/a"
    ).first.text_content()

    return {
        "Software Engineer" : {
            "name":sename,
            "url":se
        },
        "Hiring manager" : {
            "name":hmname,
            "url":hm
        }
    }
    