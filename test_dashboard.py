"""Screenshot and interaction checks via inline browser document; navigation URL policy is not bypassed."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'assets/css/dashboard.css').read_text(encoding='utf-8')
css=re.sub(r'@import url\([^;]+;', '',css)
html=re.sub(r'<link rel="stylesheet"[^>]+>',f'<style>{css}</style>',html)
html=re.sub(r'<script src="[^"]+"></script>', '',html)
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':1600,'height':1020},device_scale_factor=1)
  failures=[]
  page.on('pageerror',lambda e:failures.append(str(e)))
  page.on('console',lambda e:failures.append('console error: '+e.text) if e.type=='error' else None)
  page.set_content(html,wait_until='domcontentloaded',timeout=120000)
  for filename in ('assets/vendor/plotly.min.js','data/dashboard-data.js','assets/js/dashboard.js'):
      page.add_script_tag(content=(root/filename).read_text(encoding='utf-8'),timeout=120000) if False else page.add_script_tag(content=(root/filename).read_text(encoding='utf-8'))
      print('loaded',filename,flush=True)
  page.wait_for_selector('#exec-growth .main-svg',timeout=75000)
  names=['executive','funnel','retention','engagement','experiments','marketing','predictive']
  for i,name in enumerate(names,1):
    page.locator(f'[data-page="{name}"]').click()
    page.wait_for_selector('#page-content .plot .main-svg',timeout=60000)
    page.wait_for_timeout(1250)
    page.screenshot(path=str(root/'screenshots'/f'{i:02}_{name}_linkedin.jpg'),type='jpeg',quality=86,full_page=True,animations='disabled')
    print('page',name,'KPIs',page.locator('.kpi-value').all_text_contents(),'charts',page.locator('.main-svg').count(),flush=True)
  page.locator('[data-page="executive"]').click()
  before=page.locator('.kpi-value').all_text_contents()[0]
  page.locator('#region-filter').select_option('East')
  page.wait_for_timeout(500)
  after=page.locator('.kpi-value').all_text_contents()[0]
  print('filter changed first KPI',before,after,flush=True)
  assert before!=after,'Filter must modify KPI'
  page.locator('#reset-btn').click();page.wait_for_timeout(500)
  print('reset',page.locator('#filter-count').inner_text(),flush=True)
  print('ERRORS',json.dumps(failures[:20]),flush=True)
  assert not failures,'Browser had JS errors'
  browser.close()
