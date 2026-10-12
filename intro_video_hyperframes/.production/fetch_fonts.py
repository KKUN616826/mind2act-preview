from pathlib import Path
import re,requests,concurrent.futures
p=Path('assets/fonts'); jobs=[]
for f in p.glob('*.css'):
 for block in f.read_text().split('@font-face')[1:]:
  w=re.search('font-weight: (\d+)',block).group(1);u=re.search(r'url\(([^)]+)',block).group(1)
  jobs.append((u,p/(f.stem+'-'+w+'.ttf')))
def one(j):
 u,p=j;r=requests.get(u,timeout=45);r.raise_for_status();p.write_bytes(r.content);return str(p)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for r in ex.map(one,jobs):print(r)
