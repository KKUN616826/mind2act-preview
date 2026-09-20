#!/usr/bin/env python3
"""Check generated data, local links and media coverage before publishing."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.payload = [], [], ''
        self.in_data = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.links += [a[k] for k in ('src', 'href', 'poster') if k in a]
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'script': self.in_data = a.get('id') == 'showcaseData'
    def handle_endtag(self, tag):
        if tag == 'script': self.in_data = False
    def handle_data(self, data):
        if self.in_data: self.payload += data

def main():
    records = json.loads((ROOT/'data/showcase-cases.json').read_text())
    page = Page(); page.feed((ROOT/'index.html').read_text())
    assert json.loads(page.payload) == records, 'HTML data differs from JSON'
    assert len(page.ids) == len(set(page.ids)), 'Duplicate HTML IDs'
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        if url.path: assert (ROOT/unquote(url.path)).is_file(), link
        elif url.fragment: assert unquote(url.fragment) in page.ids, link
    assert Counter(c['suite'] for c in records) == {'cognitive':5, 'motor':5, 'coupling':5}
    media = [a for c in records for a in c['media']]
    assert len({a['path'] for a in media}) == len(media), 'Duplicate media'
    for c in records:
        assert set(c['evidence']) == {'high', 'low', 'feedback'}
        assert all(len(r) == len(c['difficulty']['columns']) for r in c['difficulty']['rows'])
        doc = (ROOT/'docs/cases'/f'{c["id"]}.md').read_text()
        assert all(a['path'] in doc for a in c['media']), c['id']
        assert all(c['evidence'][k] in doc for k in c['evidence']), c['id']
    print('PASS: embedded data, all HTML links, case documents, evidence and media coverage')
    print(dict(Counter(a['kind'] for a in media)))

if __name__ == '__main__':
    main()
