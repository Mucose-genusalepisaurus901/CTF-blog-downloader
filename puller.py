import requests
from playwright.sync_api import sync_playwright
from urllib.parse import quote
import time

ANTIBOT_JS = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
window.chrome = { runtime: {} };
"""

def fetch_csdn_results(keyword, page):
    results = []
    api_url = "https://so.csdn.net/api/v3/search"
    params = {"q": keyword, "t": "blog", "p": str(page)}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = requests.get(api_url, params=params, headers=headers, timeout=5)
        articles = resp.json().get('result_vos', []) or []
        for a in articles:
            title = a.get('title', '').replace('<em>','').replace('</em>','')
            results.append({"site": "CSDN", "title": title, "url": a.get('url')})
    except: pass
    return results

def fetch_cnblogs_results_all(keyword, max_pages, browser_path):
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=browser_path, headless=False, args=["--disable-blink-features=AutomationControlled"])
            pg = browser.new_page()
            pg.add_init_script(ANTIBOT_JS)
            
            for p_num in range(1, max_pages + 1):
                url = f"https://zzkx.cnblogs.com/s?w={quote(keyword)}&p={p_num}"
                pg.goto(url)
                if p_num == 1:
                    pg.wait_for_selector(".searchItem", timeout=30000) 
                else:
                    time.sleep(1)
                
                items = pg.query_selector_all(".searchItem")
                for item in items:
                    title_el = item.query_selector("h3 a")
                    if title_el:
                        results.append({"site": "博客园", "title": title_el.inner_text(), "url": title_el.get_attribute("href")})
            browser.close()
    except: pass
    return results

def fetch_xz_results_all(keyword, max_pages, browser_path):
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=browser_path, headless=False, args=["--disable-blink-features=AutomationControlled"])
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            pg = context.new_page()
            pg.add_init_script(ANTIBOT_JS)
            
            for p_num in range(1, max_pages + 1):
                url = f"https://xz.aliyun.com/search/3?keywords={quote(keyword)}&page={p_num}"
                pg.goto(url, wait_until="domcontentloaded")
                time.sleep(2)
                
                extracted = pg.evaluate("""
                    () => {
                        return Array.from(document.querySelectorAll('a'))
                            .filter(a => /xz\\.aliyun\\.com\\/news\\/\\d+/.test(a.href))
                            .map(a => ({ title: a.innerText.trim(), url: a.href.split('#')[0] }))
                            .filter(i => i.title.length > 5);
                    }
                """)
                for item in extracted:
                    results.append({"site": "先知社区", "title": item["title"], "url": item["url"]})
            browser.close()
    except: pass
    return results

def concurrent_search(keyword, max_pages, browser_path):
    all_results = []
    for p in range(1, max_pages + 1):
        all_results.extend(fetch_csdn_results(keyword, p))
    
    all_results.extend(fetch_cnblogs_results_all(keyword, max_pages, browser_path))
    all_results.extend(fetch_xz_results_all(keyword, max_pages, browser_path))
    
    seen = set()
    unique = []
    for r in all_results:
        if r['url'] not in seen:
            unique.append(r); seen.add(r['url'])
    return unique