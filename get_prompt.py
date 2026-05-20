import asyncio
from playwright.async_api import async_playwright
import login
import random
import test
import sys
import pyperclip

async def scroll_to_bottom(page):
    
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

    async with async_playwright() as p:
        url = sys.argv[1]
        browser, page, context = await login.login_and_save(p)
        page.set_default_timeout(5000)
        # searchpage = await people.ensure_second_tab(context=context)
        
        # await searchpage.goto(f'{people.SEARCH_URL}{urlencode({"keywords":name+" "+company})}')
        
        prompt = ""
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
                
                title = await page.title()
                name = title.split("|")
                if len(name) > 0 :
                    print(name[0])
                else :
                    sys.exit(0)

                prompt = test.SYSTEM_PROMPT + '\n' + test.build_prompt(name[0], post, about)
                
                pyperclip.copy(prompt)
                print(prompt)
                # print(post)
                # print(about)
                break

            except Exception as e:
                print(e)
                continue
        
        with open('prompt.txt', 'w') as f :
            f.write(prompt)
        

asyncio.run(main())

# Hi [], I am Kartik Gupta, a 3rd year student at NIT Kurukshetra with an interest in backend systems. I am reaching out to industry professionals to understand how actual products work. Would you be open to a quick chat about []
# Hi Ritika, I’m an ECE student at NITKKR focused on backend systems. I recently built a search engine with Redis/BM25 and have been following Sauce Labs' work in infra. I'd love to connect and learn about any upcoming internship cycles for your team!
