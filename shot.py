from playwright.sync_api import sync_playwright
import pathlib, sys
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width":1280,"height":720}, device_scale_factor=1.5)
    # Open in poster mode for social preview screenshot and PDF export
    pg.goto(pathlib.Path("index.html").resolve().as_uri() + "?view=poster", wait_until="networkidle")
    pg.wait_for_timeout(500)
    # Temporarily hide the interactive view-picker for a pristine poster screenshot
    pg.evaluate("document.querySelector('.view-picker')?.remove()")
    pg.wait_for_timeout(100)
    over = pg.evaluate("""() => [...document.querySelectorAll('body')].filter(e=>e.scrollHeight>e.clientHeight+1).map(e=>e.className+' '+e.scrollHeight+'>'+e.clientHeight)""")
    print("overflow:", over)
    pg.screenshot(path="preview.png")
    if "--pdf" in sys.argv:
        pg.pdf(path="METR_time_horizon_critique.pdf", width="1280px", height="720px", print_background=True)
    b.close()
