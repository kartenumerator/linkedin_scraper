import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from urllib.parse import urlparse, urlencode
import csv
import login
import people
import random

async def scroll_to_bottom(page):
    # Scroll incrementally to trigger lazy loaders
    # await page.locator(
    #     "xpath=/html/body/div/div[2]/div[2]/div[2]/div/main/div/div/div[1]/div/div/div[1]/div/section/div/div/div[2]/div[3]/div/div[1]/div/div[3]/button"
    # ).first.click()
    
    await asyncio.sleep(1)
    await page.mouse.click(400+(random.random()*10 - 5),500+(random.random()*10 - 5))
    print('scrolling...')
    
    await page.keyboard.press("PageDown")
    await page.keyboard.press("PageDown")
    await asyncio.sleep(random.random()+1)

    await page.keyboard.press("PageDown")
    await page.keyboard.press("PageDown")
    await asyncio.sleep(random.random()+2)
    # await page.mouse.wheel(0,1000)
async def main() :

    start = 0
    with open('persontext.txt','r') as f:
        start = int(f.read().strip())

    async with async_playwright() as p:
        browser, page, context = await login.login_and_save(p)
        page.set_default_timeout(5000)
        searchpage = await people.ensure_second_tab(context=context)
        with open("people.csv", mode="r", newline="", encoding="utf-8") as file, open("people_updated.csv", mode="a", newline="", encoding="utf-8") as outfile:
            reader = csv.reader(file)
            writer = csv.writer(outfile)
            
            idx = 0
            lim = int(random.random() * 15)
            for row in list(reader)[start:]:
                url = row[-1]
                name = row[-2]
                company = row[0]

                if idx > lim :
                    idx = 0
                    lim = int(random.random() * 10)

                    print("Pausing for natural interaction..")
                    x = input("Press enter to resume..")

                if url == "NA":
                    continue
                
                await searchpage.goto(f'{people.SEARCH_URL}{urlencode({"keywords":name+" "+company})}')
                
                for times in range(2) :
                    try :
                        await page.goto(url)
                        await asyncio.sleep(random.random())
                        await scroll_to_bottom(page)
                        exp = page.locator(
                            "div[componentKey*=profileCardsBelowActivityPart1]"
                        ).first
                    
                        post = await exp.locator(
                            "div[componentKey*=entity-collection-item]"
                        ).first.text_content()

                        about = await page.locator(
                            "div[componentKey*=About]"
                        ).first.text_content()

                        writer.writerow(row + [post, about])

                        print(post)
                        print(about)
                        break
                    except Exception as e:
                        print(e)
                        continue
                
                start += 1
                idx += 1
                with open('persontext.txt', 'w') as f:
                    f.write(f'{start}')

asyncio.run(main())