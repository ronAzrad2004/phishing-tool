from playwright.async_api import async_playwright
from argparse import ArgumentParser
import subprocess
import asyncio
import random
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
from pydantic import BaseModel,HttpUrl

app = FastAPI()

class INPUT(BaseModel):
    url:HttpUrl

def get_random_user_agent():
    user_agents = [
        # Windows - Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        # Windows - Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        # Windows - Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.65",
        
        # macOS - Safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
        # macOS - Chrome
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        
        # Linux - Chrome (Fedora/Ubuntu style)
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        
        # iOS - iPhone Safari
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        
        # Android - Chrome
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.40 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        
        # iPad - Safari
        "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        
        # Misc/Less Common but Valid
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
    ]
    return random.choice(user_agents)

@app.get("/")
def inedx():
    return FileResponse('static/index.html')

@app.post("/")
async def start(payload:INPUT):
    print(f"starting process : {payload.url}")
    return {"status":404}

async def run(url):
    async with async_playwright() as p:
        # 1. Launch the browser
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(user_agent=get_random_user_agent())
        
        # 3. AWAIT the new_page
        page = await context.new_page()
        
        print(f"Navigating to {url}...")
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        screenshot_path = "./res/website_capture.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")
        
        await browser.close()

if __name__ == "__main__":
    uvicorn.run("app:app",host="127.0.0.1",port=8000,reload=True)
    parser = ArgumentParser()
    parser.add_argument("--url", type=str, help="URL to navigate to")
    args = parser.parse_args()
    domain = args.url.split("://")[-1].split("/")[0].replace("www.", "")
    print(f"Extracted domain: {domain}")
    process_whois = subprocess.run(['whois', domain], capture_output=True, text=True)
    process_dig = subprocess.run(['dig', domain], capture_output=True, text=True)
    output_1 = process_whois.stdout
    output_2 = process_dig.stdout
    with open("./res/whois_output.txt", "w") as f:
        f.write("who is output:\n")
        f.write(output_1)
        f.write("\ndig output:\n")
        f.write(output_2)
        f.close()
    asyncio.run(run(args.url))
    
    