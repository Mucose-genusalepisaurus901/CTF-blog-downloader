import os
import html2text
import time
from playwright.sync_api import sync_playwright

def download_as_md(url, save_path, browser_exe_path):
    if not os.path.exists(browser_exe_path): return False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=browser_exe_path, headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page = context.new_page()
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(2) 

            content_html = page.evaluate("""
                () => {
                    const host = location.hostname;
                    let post = null;
                    if (host.includes('xz.aliyun.com')) {
                        post = document.querySelector('.left_container');
                        if (!post) return null;
                        
                        const clone = post.cloneNode(true);
                        const topJunk = ['#news_toolbar', '.detail_info', 'script', 'style'];
                        topJunk.forEach(sel => {
                            clone.querySelectorAll(sel).forEach(el => el.remove());
                        });

                        const breakPoints = ['.detail_share', '.detail_comment', '.reply-list'];
                        breakPoints.forEach(sel => {
                            const marker = clone.querySelector(sel);
                            if (marker) {
                                let next = marker;
                                while (next) {
                                    let toRemove = next;
                                    next = next.nextElementSibling;
                                    toRemove.remove(); 
                                }
                            }
                        });
                        
                        clone.querySelectorAll('img').forEach(img => {
                            if (img.src && img.src.startsWith('/')) img.src = location.origin + img.src;
                        });
                        return clone.innerHTML;
                    } 

                    post = document.querySelector('.news-content') || 
                           document.querySelector('.topic-content') || 
                           document.querySelector('#article_content') ||
                           document.querySelector('#cnblogs_post_body') ||
                           document.querySelector('article');
                    if (!post) return null;
                    const genClone = post.cloneNode(true);
                    genClone.querySelectorAll('script, style, .login-mark, .n-reward').forEach(el => el.remove());
                    genClone.querySelectorAll('img').forEach(img => {
                        if (img.src && img.src.startsWith('/')) img.src = location.origin + img.src;
                    });
                    return genClone.innerHTML;
                }
            """)
            
            if not content_html:
                browser.close(); return False

            h2t = html2text.HTML2Text()
            h2t.body_width = 0
            h2t.mark_code = True
            md_text = h2t.handle(content_html)
            
            if len(md_text.strip()) < 50:
                browser.close(); return False
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(md_text)
            
            browser.close()
            return True
    except Exception as e:
        print(f"下载出现异常: {e}")
        return False