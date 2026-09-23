#!/usr/bin/env python3
"""Validate proposal artifacts, examples and source links without model execution."""
import argparse
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.in_json=False;self.payload=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        self.links += [a[k] for k in ('href','src') if a.get(k)]
        if tag=='script':self.in_json=a.get('id')=='modelData'
    def handle_endtag(self,tag):
        if tag=='script':self.in_json=False
    def handle_data(self,data):
        if self.in_json:self.payload+=data

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--static-only',action='store_true',help='Compatibility flag; validation is static.');ap.parse_args()
    data=json.loads((ROOT/'data/model.json').read_text());p=Page();page=(ROOT/'index.html').read_text();p.feed(page)
    assert data['model']=='Mind2Act Harness' and data['status']=='proposal' and data['results'] is None
    assert data['upstream']['name']=='GPT-6 Astra' and data['downstream']['name']=='Jev'
    assert data['upstream']['api_model_id'] is None and data['downstream']['version'] is None
    assert json.loads(p.payload)==data
    assert len(set(p.ids))==len(p.ids)
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        path=(ROOT/unquote(u.path)).resolve() if u.path else ROOT/'index.html'
        assert path.is_file(),link
        if u.fragment:
            target=p
            if u.path:target=Page();target.feed(path.read_text())
            assert unquote(u.fragment) in target.ids,link
    examples=data['examples'];contract=examples['subgoal-contract'];packet=examples['decision-packet'];request=examples['jev-request']
    assert request['state']==packet and contract['contract_version']==packet['contract_version']
    assert contract['goal_id']==packet['goal_id']
    ids=[c['id'] for c in packet['valid_candidates']]
    assert len(ids)==len(set(ids)) and set(ids)==set(request['questions']['next_candidate']['criteria'])
    assert set(ids)=={'refresh','escalate','abstain'} and packet['selected_id'] is None
    assert examples['scene-state']['facts'][1]['base_transform_status']=='unknown'
    assert examples['scene-state']['effect']['status']=='unknown'
    assert all(examples[k]['example_only'] for k in ['subgoal-contract','scene-state','decision-packet'])
    for f in data['figures']:
        ET.parse(ROOT/f['path'])
        assert (ROOT/'figures/specs'/ (Path(f['path']).stem+'.json')).is_file()
    assert len(data['figures'])==3 and len(data['modules'])==8
    assert 'experience-lifecycle-v2.png' not in page and 'experience' not in [m['id'] for m in data['modules']]
    assert (ROOT/'docs/PhysCo_Model_Architecture.md').read_bytes()==(ROOT/'docs/MindAccord_Proposal_v2.md').read_bytes()
    print('PASS: proposal status, identities, embedded data, local links, 3 SVG specs, memory examples and no fabricated result.')
if __name__=='__main__':main()
