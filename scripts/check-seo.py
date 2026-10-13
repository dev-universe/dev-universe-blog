"""Validate generated pages before deployment; only uses Python's standard library."""
from html.parser import HTMLParser
from pathlib import Path
import json
import xml.etree.ElementTree as ET

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.meta={}; self.links=[]; self.schemas=[]; self.capture=False; self.buffer=''; self.h1=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='meta': self.meta[a.get('name',a.get('property'))]=a.get('content')
        if tag=='link': self.links.append(a)
        if tag=='h1': self.h1+=1
        if tag=='script' and a.get('type')=='application/ld+json': self.capture=True; self.buffer=''
    def handle_data(self, data):
        if self.capture: self.buffer+=data
    def handle_endtag(self, tag):
        if tag=='script' and self.capture:
            self.schemas.extend(json.loads(self.buffer)['@graph']); self.capture=False

root=Path('dist'); base='https://dev-universe.tech'
urls=[]
for path in sorted(root.rglob('*.html')):
    page=Page(path.read_text()); relative=path.relative_to(root).as_posix()
    assert page.h1==1, path
    assert page.meta['description'], path
    assert len([x for x in page.links if x.get('rel')=='canonical'])==1, path
    if relative=='404.html':
        assert 'noindex' in page.meta['robots']; continue
    url=base+'/'+relative.removesuffix('index.html'); urls.append(url)
    assert next(x['href'] for x in page.links if x.get('rel')=='canonical')==url
    assert page.meta['og:url']==url
    assert page.meta['og:image']==base+'/og.png'
    assert page.meta['twitter:card']=='summary_large_image'
    assert 'noindex' not in page.meta['robots']
    if relative.startswith('posts/'):
        article=next(x for x in page.schemas if x['@type']=='BlogPosting')
        assert article['mainEntityOfPage']==url
        assert article['author']['name']=='universe'
        assert article['dateModified']>=article['datePublished']
        assert article['abstract'] in path.read_text()
        assert any(x['@type']=='BreadcrumbList' for x in page.schemas)
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap=ET.parse(root/'sitemap-0.xml')
assert set(urls)=={x.text for x in sitemap.findall('.//s:loc',ns)}
rss=ET.parse(root/'rss.xml'); links=[x.text for x in rss.findall('.//item/link')]
assert set(links)=={u for u in urls if '/posts/' in u}
assert 'Sitemap: '+base+'/sitemap-index.xml' in (root/'robots.txt').read_text()
print(f'SEO validation passed: {len(urls)} indexable pages, {len(links)} articles, valid JSON-LD, canonical URLs, sitemap and RSS.')
