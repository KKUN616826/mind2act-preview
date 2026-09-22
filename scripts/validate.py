#!/usr/bin/env python3
"""Check generated data, local links and media coverage before publishing."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from leaderboard import load as load_leaderboard

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.payload, self.board_payload = [], [], '', ''
        self.in_data = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.links += [a[k] for k in ('src', 'href', 'poster') if k in a]
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'script': self.in_data = a.get('id')
    def handle_endtag(self, tag):
        if tag == 'script': self.in_data = False
    def handle_data(self, data):
        if self.in_data == 'showcaseData': self.payload += data
        if self.in_data == 'leaderboardData': self.board_payload += data

def main():
    records = json.loads((ROOT/'data/showcase-cases.json').read_text())
    content = (ROOT/'index.html').read_text()
    page = Page(); page.feed(content)
    subtitle = 'Evaluating Reasoning–Acting Coordination in Robotic Manipulation'
    assert subtitle in content and subtitle in (ROOT/'docs/PhysCo_Showcase.md').read_text()
    assert '<h1 id="project-title">MindActWorld</h1>' in content
    for stale in ['肌肉记忆', 'MUSCLE MEMORY', 'Cognitive–Motor Coupling', 'Cognitive Core', 'Motor Core', 'Coupling Suite', '>PhysCo<']:
        assert stale not in content, 'Outdated public narrative: ' + stale
    assert json.loads(page.payload) == records, 'HTML data differs from JSON'
    assert len(page.ids) == len(set(page.ids)), 'Duplicate HTML IDs'
    for section in ['overview', 'motivation', 'insight', 'insight-goal', 'insight-action', 'insight-feedback', 'design', 'mindact', 'leaderboard', 'cases', 'evaluation', 'resources']:
        assert section in page.ids, 'Missing research section: ' + section
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        if url.path: assert (ROOT/unquote(url.path)).is_file(), link
        elif url.fragment: assert unquote(url.fragment) in page.ids, link
    assert Counter(c['suite'] for c in records) == {'cognitive':5, 'motor':5, 'coupling':5}
    board = load_leaderboard(records)
    assert json.loads(page.board_payload) == board, 'HTML leaderboard differs from source JSON'
    assert Counter(r['track'] for r in board['candidates']) == {'vla':5, 'coding':9}
    assert [r['name'] for r in board['candidates'] if r['track']=='vla'] == ['hyVLA','dm0.5','g0.5','openwam','pi0.5']
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
    print('PASS: leaderboard roster, 15-task coverage, null scores/ranks/costs and pending status')
    for dimension in ['Task-Level Reasoning', 'Constraint-Aware Execution', 'Reasoning–Acting Coordination']:
        assert dimension in content, 'Missing named dimension: ' + dimension
    assert 'Adaptive Coordination' not in content
    assert 'Adaptive Reasoning–Acting Coordination' not in content
    assert '真实任务同时要求 agent' not in content
    assert 'Closed-Loop Coordination' not in content
    assert '闭环协同' not in content
    assert 'Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation' in content
    assert 'href="mindaccord/index.html"' in content
    print('PASS: approved subtitle, MindActWorld branding and three named dimensions')

if __name__ == '__main__':
    main()
