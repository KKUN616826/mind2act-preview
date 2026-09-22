#!/usr/bin/env python3
"""Validate the model-only website, generated figures and responsive interactions."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
checks = []
def check(label, value):
    assert value, label
    checks.append(label)

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids
            self.ids.add(attrs['id'])
        for key in ('src', 'href'):
            if attrs.get(key):
                self.links.append(attrs[key])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--static-only', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/model.json').read_text())
    check('MindAccord model identity', data['model'] == 'MindAccord')
    check('approved model subtitle', data['subtitle'] == 'Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation')
    page_text = (ROOT / 'index.html').read_text()
    check('page and data share model subtitle', data['subtitle'] in page_text)
    check('old title removed from active page', 'PhysCo-VLA' not in page_text)
    check('editable architecture carries new model name', 'MindAccord' in (ROOT / 'media/mindaccord-architecture.svg').read_text())
    parsed = Links()
    parsed.feed((ROOT / 'index.html').read_text())
    for link in parsed.links:
        p = urlsplit(link)
        if p.scheme:
            continue
        path = (ROOT / unquote(p.path)).resolve() if p.path else ROOT / 'index.html'
        assert path.exists(), link
        if p.fragment:
            target = parsed
            if p.path:
                target = Links()
                target.feed(path.read_text())
            assert unquote(p.fragment) in target.ids, link
    check('all local resources and Bench links resolve', True)
    check('no case data in public model JSON', 'cases' not in data and all('cases' not in m for m in data['modules']))
    check('two distinct model figures', len(data['figures']) == 2)
    if args.static_only:
        print(json.dumps(dict(passed=len(checks), checks=checks), ensure_ascii=False, indent=2))
        return
    from playwright.sync_api import sync_playwright
    (ROOT / 'qa').mkdir(exist_ok=True)
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width':1440,'height':1000}, device_scale_factor=1)
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto((ROOT / 'index.html').as_uri())
        page.wait_for_load_state('networkidle')
        page.emulate_media(reduced_motion='reduce')
        check('no Case cards or search', page.locator('.case-card, #caseSearch, .featured').count() == 0)
        page.screenshot(path=str(ROOT / 'qa/model-v2-desktop.png'))
        for width in (1920,1280,768,390,320):
            page.set_viewport_size({'width':width,'height':900})
            check(f'no document overflow at {width}px', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000})
        for module in data['modules']:
            page.locator(f'[data-module="{module["id"]}"]').click()
            check('module ' + module['id'], page.locator('#moduleInspector h3').inner_text() == module['name'])
        for key, state in data['states'].items():
            page.locator(f'[data-state="{key}"]').click()
            check('execution state ' + key, page.locator('#stateResult > h3').inner_text() == state['title'])
        for figure in data['figures']:
            page.locator(f'[data-figure="{figure["id"]}"]').click()
            check('figure opens ' + figure['id'], page.locator('#figureDialog').evaluate('(d)=>d.open'))
            check('correct figure asset ' + figure['id'], page.locator('#dialogImage').get_attribute('src') == figure['path'])
            page.keyboard.press('Escape')
            check('Escape closes figure ' + figure['id'], not page.locator('#figureDialog').evaluate('(d)=>d.open'))
        page.locator('#memory').scroll_into_view_if_needed()
        page.screenshot(path=str(ROOT / 'qa/model-v2-memory.png'))
        page.locator('[data-module="runtime"]').click()
        page.locator('#moduleInspector a').first.click()
        check('source links open source disclosure', page.locator('#codeDetails').evaluate('(d)=>d.open'))
        check('only generated figures in page', page.locator('main img').count() == 2)
        check('figures loaded', page.locator('main img').evaluate_all('(els)=>els.every(e=>e.complete && e.naturalWidth===1536)'))
        page.set_viewport_size({'width':390,'height':844})
        page.evaluate("location.hash='#overview'; window.scrollTo(0,0)")
        page.screenshot(path=str(ROOT / 'qa/model-v2-mobile.png'))
        page.locator('#menuToggle').click()
        check('mobile navigation opens', page.locator('#menuToggle').get_attribute('aria-expanded') == 'true')
        page.keyboard.press('Escape')
        check('mobile navigation closes', page.locator('#menuToggle').get_attribute('aria-expanded') == 'false')
        page.locator('[data-figure="architecture"]').click()
        check('mobile enlarged figure can scroll', page.locator('.dialog-image').evaluate('(e)=>e.scrollWidth>e.clientWidth'))
        page.screenshot(path=str(ROOT / 'qa/model-v2-mobile-figure.png'))
        page.locator('#closeFigure').click()
        page.wait_for_function("() => document.body.style.overflow === ''")
        check('close restores body scrolling', page.evaluate("document.body.style.overflow === ''"))
        page.locator('#architecture').scroll_into_view_if_needed()
        page.screenshot(path=str(ROOT / 'qa/model-v2-architecture-mobile.png'))
        check('no script errors', errors == [])
        browser.close()
    report = dict(revision='model-focused-v2', passed=len(checks), checks=checks, errors=errors,
                  scope='Website verification only; generated conceptual figures, no robotics results')
    (ROOT / 'qa/validation-v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
