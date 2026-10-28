from playwright.sync_api import sync_playwright
import pathlib, sys

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1.0)
    # Open in poster mode for social preview screenshot and PDF export
    pg.goto(pathlib.Path("index.html").resolve().as_uri() + "?view=poster", wait_until="networkidle")
    pg.wait_for_timeout(500)
    
    # Hide the view-picker and fit poster edge-to-edge for social preview card
    pg.evaluate("""() => {
        document.querySelector('.view-picker')?.remove();
        const stage = document.querySelector('.poster-stage');
        if (stage) {
            stage.style.padding = '0';
            stage.style.margin = '0';
            stage.style.display = 'block';
        }
        const wrapper = document.querySelector('.poster-wrapper');
        const page = document.querySelector('.page');
        if (wrapper && page) {
            wrapper.style.width = '1280px';
            wrapper.style.height = '720px';
            wrapper.style.margin = '0';
            wrapper.style.border = 'none';
            page.style.transform = 'scale(0.8)';
            page.style.transformOrigin = '0 0';
        }
    }""")
    pg.wait_for_timeout(100)
    
    over = pg.evaluate("""() => [...document.querySelectorAll('body')].filter(e=>e.scrollHeight>e.clientHeight+1).map(e=>e.className+' '+e.scrollHeight+'>'+e.clientHeight)""")
    print("overflow:", over)
    pg.screenshot(path="preview.png")
    
    if "--pdf" in sys.argv:
        pg.pdf(path="METR_time_horizon_critique.pdf", width="1280px", height="720px", print_background=True)
    b.close()
