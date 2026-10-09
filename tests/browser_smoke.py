"""Optional browser integration test (requires playwright and Chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as pw:
    import os
    kwargs={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
    if os.environ.get('CHROMIUM_BIN'):kwargs['executable_path']=os.environ['CHROMIUM_BIN']
    browser=pw.chromium.launch(**kwargs)
    page=browser.new_page(viewport={'width':1440,'height':960},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.set_content((ROOT/'docs/index.html').read_text(encoding='utf-8'),wait_until='load')
    print('title:',page.title())
    print('initial result label:',page.locator('#resultCount').inner_text())
    assert page.locator('#resultCount').inner_text() == '100 of 100 research problems'
    assert page.locator('.problem-card').count()==12
    assert page.locator('.discipline-tile').count()==5
    page.locator('#domain').select_option('Genetics')
    assert page.locator('#resultCount').inner_text()=='20 of 100 research problems'
    topic=page.locator('#topic option').all_text_contents()
    assert len(topic)==6, topic
    page.locator('#topic').select_option('Regulatory genomics')
    assert page.locator('#resultCount').inner_text()=='4 of 100 research problems'
    subtopic=page.locator('#subtopic option').all_text_contents()
    assert len(subtopic)==3,subtopic
    page.locator('#subtopic').select_option('Regulatory sequence logic')
    assert page.locator('#resultCount').inner_text()=='2 of 100 research problems'
    page.locator('#reset').click()
    page.locator('#query').fill('epistasis')
    print('epistasis search:',page.locator('#resultCount').inner_text())
    assert int(page.locator('#resultCount').inner_text().split(' ')[0])>0
    page.locator('#reset').click()
    page.locator('[data-save="P01"]').click()
    page.locator('#savedOnly').check()
    assert page.locator('#resultCount').inner_text()=='1 of 100 research problems'
    page.locator('#savedOnly').uncheck()
    page.locator('#themeToggle').click()
    assert page.locator('html').get_attribute('data-theme')=='dark'
    page.locator('#themeToggle').click()
    page.locator('#sourceSearch').fill('Clay Mathematics')
    print('source search:',page.locator('#sourceCount').inner_text())
    assert int(page.locator('#sourceCount').inner_text().split(' ')[0]) > 0
    page.locator('#sourceSearch').fill('')
    page.locator('#reset').click()
    page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
    page.wait_for_timeout(200)
    page.screenshot(path=str(ROOT/'assets/frontieratlas-preview.png'),full_page=False)
    print('Screenshot:',ROOT/'assets/frontieratlas-preview.png')
    print('JS errors:',errors)
    assert not errors,errors
    browser.close()
print('PASS: browser smoke tests (facets, full text, favorites, themes, source search, screenshot).')

