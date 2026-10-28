from playwright.sync_api import sync_playwright
import pathlib, sys
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width":1280,"height":720}, device_scale_factor=1.5)
    pg.goto(pathlib.Path("index.html").resolve().as_uri(), wait_until="networkidle")
    pg.wait_for_timeout(500)
    over = pg.evaluate("""() => [...document.querySelectorAll('body')].filter(e=>e.scrollHeight>e.clientHeight+1).map(e=>e.className+' '+e.scrollHeight+'>'+e.clientHeight)""")
    print("overflow:", over)
    pg.screenshot(path="preview.png")
    if "--pdf" in sys.argv:
        pg.pdf(path="METR_time_horizon_critique.pdf", width="1280px", height="720px", print_background=True)
    b.close()
