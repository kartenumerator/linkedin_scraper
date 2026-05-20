"""
LinkedIn Login with Playwright — saves browser context (cookies + storage)
so you can reuse the session without logging in again.

Usage:
    pip install playwright
    playwright install chromium

    # First run — logs in and saves session:
    python linkedin_login.py

    # Edit credentials below or pass via environment variables:
    LINKEDIN_EMAIL=you@example.com LINKEDIN_PASSWORD=secret python linkedin_login.py
"""

import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from urllib.parse import urlparse, urlencode
# import sys 
import people
import csv

JOBSFILE = "jobs.csv"
PEOPLEFILE = "people.csv"

load_dotenv()

START = 0
with open('texts.txt', 'r') as f :
    START = int(f.read().strip())

query = {"keywords":"software posted in the past week", "start":START, "geoId":106187582, "distance":0.0}
URL = f"https://www.linkedin.com/jobs/search-results/?"
# URL = f"https://www.linkedin.com/jobs/search-results/?{urlencode(query)}&origin=JOBS_HOME_KEYWORD_HISTORY&geoId=102713980&distance=0.0"
SEARCH_URL = "https://www.linkedin.com/search/results/people/?"


path = urlparse(URL).path

# ── Credentials ──────────────────────────────────────────────────────────────
EMAIL    = os.getenv("LINKEDIN_EMAIL",    "")
PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")

# ── Paths ─────────────────────────────────────────────────────────────────────
SESSION_PATH = "linkedin_session.json"   # saved context (cookies + localStorage)

async def check_h1_contains(page, target_text: str) -> bool:
    h1 = await page.query_selector('h1')
    if h1:
        text = await h1.inner_text()
        return target_text.lower() in text.lower()  # case-insensitive
    return False

async def login_and_save(p):
    # Launch a visible browser (set headless=True to run in background)
    global query, URL
    browser = await p.chromium.launch(headless=False, slow_mo=50)
    # Load existing session if available, otherwise start fresh
    if os.path.exists(SESSION_PATH):
        print(f"[*] Loading saved session from '{SESSION_PATH}' …")
        context = await browser.new_context(storage_state=SESSION_PATH)
    else:
        print("[*] No saved session found — starting fresh login …")
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
    page = await context.new_page()
    # ── Navigate to LinkedIn ──────────────────────────────────────────────
    print("[*] Opening LinkedIn …")
    await page.goto(f'{URL}{urlencode(query)}', wait_until="domcontentloaded")
    # Check if already logged in (session restored successfully)
    # h1 = await page.query_selector('h1')
    # if h1:
    #     text = await h1.inner_text()
    #     return target_text.lower() in text.lower()  # case-insensitive
    target = "Welcome Back"
    h1 = await page.query_selector('h1')
    text = ""
    if h1:
        text = await h1.inner_text()
    
    if path == urlparse(page.url).path or "mynetwork" in page.url:
        print("[✓] Already logged in via saved session.")
    
    elif target.lower() in text.lower() :
        print("Have to click extra..")
        button = await page.query_selector("button.member-profile__details")
        await button.click()

    else:
        # ── Fill login form ───────────────────────────────────────────────
        print("[*] Filling in credentials …")
        await page.fill("#username", EMAIL)
        await page.fill("#password", PASSWORD)
        print("[*] Submitting login form …")
        await page.click('button[type="submit"]')
        # Wait for navigation after login
        # await page.wait_for_url("**/feed/**", timeout=15_000)
        print(f"[✓] Login successful! Current URL: {page.url}")
    
    # ── Save session ──────────────────────────────────────────────────────
    await context.storage_state(path=SESSION_PATH)
    print(f"[✓] Session saved to '{SESSION_PATH}'")

    return (browser, page, context)
    # ── Optional: do something on the page ───────────────────────────────
    # e.g. await page.goto("https://www.linkedin.com/mynetwork/")
    # await browser.close()
    # print("[*] Browser closed.")

def write_csv(jobs):
    people = []
    with open("texts.txt",'w') as f :
        f.write(f'{START}')
    with open(JOBSFILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not os.path.isfile(JOBSFILE) :
            writer.writerow(["title","company","location","about","url"])
        for data in jobs :
            writer.writerow([data['title'],data['company'],data['location'],data['about'],data['url']])
            people.append([data["company"],"Software Engineer", data['people']['Software Engineer']['name'], data['people']['Software Engineer']['url']])
            people.append([data["company"],"Hiring Manager", data['people']['Hiring manager']['name'], data['people']['Hiring manager']['url']])
    
    with open(PEOPLEFILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not os.path.isfile(PEOPLEFILE) :
            writer.writerow(["title","company","location","about","url"])
        writer.writerows(people)
        

async def load_saved_session(browser, page, context) -> None:
    global START
    """
    Demonstrate reusing a saved session (no login needed).
    Call this instead of login_and_save() on subsequent runs.
    """
    # if not os.path.exists(SESSION_PATH):
    #     print("[!] No saved session found. Run login_and_save() first.")
    #     return

    # browser = await p.chromium.launch(headless=False)
    # context = await browser.new_context(storage_state=SESSION_PATH)
    # page    = await context.new_page()
    while True :
        print("[*] Opening LinkedIn with saved session …")
        # await page.goto(URL, wait_until="domcontentloaded")
        
        print(f"[✓] Page loaded: {page.url}")
        # Re-save to refresh cookie expiry timestamps
        await context.storage_state(path=SESSION_PATH)
        
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)

        page.set_default_timeout(5000)

        job_results = page.locator(
            'div[componentKey="SearchResultsMainContent"]'
        )
        # jobss = await job_results.locator("> *")
        # print(jobss)
        seen = set()
        jobs = []

        children = job_results.locator("> div")

        count = await children.count()
        print(f'{count} children')
        
        for i in range(count):
            print(i)
            card = children.nth(i)

            # print(await card.text_content())
            checker = await card.locator(
                "xpath=//div/div/h2"
            ).is_visible()

            # if "Are these results helpful?".lower() in checker.lower() :
            #     print("Breaking out of loop")
            #     break
            if checker :
                break

            title = "NA"

            button = card.locator(
                "xpath=//div/div/div"
            ).first
            try :
                await button.click(timeout=10000)
            except Exception as e:
                break

            url = ''
            try :
                url = await page.locator(
                    'xpath=//*[@id="workspace"]/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div[2]/div/div[3]/div/div/div/div/div[1]/a'
                ).first.get_attribute("href")
            except Exception as e :
                continue

            try :
                title = await card.locator(
                    "xpath=//div/div/div/div/div/div/div/div/div/div/p/span[@aria-hidden='true']"
                ).text_content()
            except Exception as e :
                print("Breaking out of loop.")
                break
            location = await card.locator(
                    #    //div/div/div/div/div/div[1]/div[1]/div/p
                "xpath=//div/div/div/div/div/div/div[1]/div[1]/div/p"
            ).nth(2).text_content()
            
            company = await card.locator(
                "xpath=//div/div/div/div/div/div/div[1]/div[1]/div/div[2]/p"
                # "xpath=//div/div/div/div/div/div/div/div/div/div[2]/p"
            ).first.text_content()

            details = page.locator(
                'div[componentKey*="JobDetails_AboutTheJob"]'
            ).first
            about = await details.locator(
                'xpath=//div/div/div/div/p'
            ).first.text_content()
            

            print(url)
            # print(about)
            ppl = {
                "Software Engineer" : {
                    "name":"NA",
                    "url":"NA"
                },
                "Hiring manager" : {
                    "name":"NA",
                    "url":"NA"
                }
            }
            try :
                ppl = await people.get_people(browser,context,page,company)
                print(ppl)
            except Exception as e :
                pass
            
            START += 1
            jobs.append({
                "title":title,
                "location":location,
                "company":company,
                "about":about,
                "url":url,
                "people":ppl
            })

            write_csv(jobs)
            jobs = []
            
        print(f"\nFound {len(jobs)} jobs\n")

        try :
            query['start'] = START
            await page.goto(f'{URL}{urlencode(query)}')
        except Exception as e :
            print(e)
            break

        # write_csv(jobs)

        # for idx, job in enumerate(jobs, 1):
        #     print("=" * 80)
        #     print(f"Job #{idx}")
        #     print("Title:", job["title"])
        #     print("Location:", job["location"])
        #     print("Company:", job["company"])
        #     # print("About:", job["about"])
        #     print("URL:", job["url"])
            # print("Text:", job["raw_text"][:500])

    await browser.close()


async def main():
    async with async_playwright() as p:
        browser, page, context = await login_and_save(p)
        await load_saved_session(browser, page, context)

# if __name__ == "__main__":
#     asyncio.run(main())