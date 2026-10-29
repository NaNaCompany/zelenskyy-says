"""Public metadata only. Reject reposts and unresolved authors; never publish bodies."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import hashlib,json,re,sys,time

BASE=Path(__file__).resolve().parents[1]
RAW=BASE/'.cache/source-pages';RAW.mkdir(parents=True,exist_ok=True)
APPS=[json.loads((BASE/'APP.json').read_text(encoding='utf-8'))]
PROVIDER='https://nitter.jaydenha.uk'
NOW=datetime.now(timezone.utc)
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Node:
 def __init__(self,tag='',attrs=None,parent=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=[];self.parent=parent;self.text=''
 def has(self,cls):return cls in self.attrs.get('class','').split()
 def walk(self):
  yield self
  for child in self.children:yield from child.walk()
 def find(self,cls):return next((n for n in self.walk() if n.has(cls)),None)

class Tree(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root]
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs,self.stack[-1]);self.stack[-1].children.append(n)
  if tag not in VOID:self.stack.append(n)
 def handle_startendtag(self,tag,attrs):
  n=Node(tag,attrs,self.stack[-1]);self.stack[-1].children.append(n)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):self.stack[-1].text+=data

def classify(item,handle):
 if item.find('retweet-header') or item.find('retweet'):
  return None,'repost'
 link=item.find('tweet-link');username=item.find('username')
 if not link or not username:return None,'missing-author-or-permalink'
 m=re.fullmatch(r'/([A-Za-z0-9_]+)/status/(\d+)(?:#m)?',link.attrs.get('href',''))
 author=username.attrs.get('href','').strip('/')
 if not m or author.lower()!=handle.lower() or m[1].lower()!=handle.lower() or item.attrs.get('data-username','').lower()!=handle.lower():return None,'other-author-or-unverified'
 content=item.find('tweet-content')
 quote=item.find('quote') or item.find('quote-big')
 # Text is inspected only to classify a quote; it is never retained in output.
 if quote and (not content or not ''.join(n.text for n in content.walk()).strip()):return None,'quote-without-authored-content'
 identity=m[2];stamp=datetime.fromtimestamp(((int(identity)>>22)+1288834974657)/1000,timezone.utc)
 if int(identity)<100000000000 or stamp>NOW or stamp.year<2010:return None,'invalid-or-future-time'
 kind='quote' if quote else 'reply' if item.find('replying-to') else 'original'
 row=dict(id='x-'+identity,post_id=identity,platform='x',author=handle,original_url=f'https://x.com/{handle}/status/{identity}',published_at=stamp.isoformat(timespec='milliseconds').replace('+00:00','Z'),published_date=stamp.date().isoformat(),date_precision='millisecond',source_ids=['nitter-public-timeline'],text=None,post_kind=kind,is_repost=False,author_verified=True)
 proof={'permalink_author':m[1],'username_author':author,'item_author':item.attrs['data-username'],'retweet_header':False,'quote_has_authored_content':bool(quote),'classification':kind}
 return (row,proof),None

def parse(body,handle):
 tree=Tree();tree.feed(body.decode('utf-8'))
 items=[n for n in tree.root.walk() if n.has('timeline-item')]
 accepted=[];excluded=Counter()
 for item in items:
  result,reason=classify(item,handle)
  if reason:excluded[reason]+=1
  else:accepted.append(result)
 more=next((n for n in tree.root.walk() if n.has('show-more') and any('cursor=' in c.attrs.get('href','') for c in n.walk())),None)
 href=next((c.attrs['href'] for c in more.walk() if 'cursor=' in c.attrs.get('href','')),None) if more else None
 return accepted,excluded,href,len(items)

def collect(app,max_pages=20):
 handle=app['handle'];slug=app['slug'];folder=RAW/slug;folder.mkdir(exist_ok=True)
 rows={};proofs={};pages=[];exclusions=Counter();failures=[];url=PROVIDER+'/'+handle+'/with_replies';seen=set()
 for i in range(max_pages):
  if url in seen:break
  seen.add(url);target=folder/f'page-{i:03d}.html';urlfile=folder/f'page-{i:03d}.url'
  try:
   if target.exists():
    assert urlfile.read_text()==url,'Cache URL mismatch';body=target.read_bytes()
   else:
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as response:body=response.read()
    target.write_bytes(body);urlfile.write_text(url)
   accepted,rejected,more,total=parse(body,handle)
   if not total:raise ValueError('No timeline items; not a valid archive page')
   pagehash=hashlib.sha256(body).hexdigest();exclusions.update(rejected)
   pages.append(dict(url=url,sha256=pagehash,timeline_items=total,accepted=len(accepted),excluded=dict(rejected)))
   for row,proof in accepted:
    identity=row['id'];rows[identity]=row
    proofs.setdefault(identity,dict(**proof,source_url=url,source_sha256=pagehash))
   if not more:break
   url=urljoin(url,more)
   assert urlsplit(url).hostname=='nitter.jaydenha.uk'
   time.sleep(.25)
  except Exception as e:
   failures.append(dict(url=url,error=str(e)));break
 result=sorted(rows.values(),key=lambda r:int(r['post_id']),reverse=True)
 audit=dict(slug=slug,captured_at=NOW.isoformat(),coverage='partial',records=len(result),first=result[-1]['published_date'] if result else None,last=result[0]['published_date'] if result else None,exact_time=len(result),sources=[dict(id='nitter-public-timeline',url=PROVIDER+'/'+handle+'/with_replies',creator='Nitter public timeline (original X account linked for every record)',redistributed_fields=['post_id','author','ID-derived timestamp','original_permalink','post_kind'],body_rights='Not established; all scraped bodies, media, translations and third-party summaries excluded')],failures=failures,collection_limit_pages=max_pages,pages=pages,excluded=dict(exclusions),repost_policy='Exclude every native repost; require matching top-level permalink, username and timeline-item author. Quotes require authored content; replies are eligible. Ambiguous records excluded.',translation_policy='No translations collected or created. Official X embed displays original content.',post_body_policy='Only factual metadata and original permalinks are redistributed; original content is loaded through the official X embed on demand.')
 (BASE/'data/posts.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
 (BASE/'data/source-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (BASE/'data/classification-evidence.json').write_text(json.dumps(proofs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(slug=slug,records=len(result),pages=len(pages),excluded=dict(exclusions),failures=len(failures),first=audit['first'],last=audit['last'])),flush=True)
 return audit

if __name__=='__main__':
 chosen=[a for a in APPS if len(sys.argv)<2 or a['slug'] in sys.argv[1:]]
 with ThreadPoolExecutor(3) as pool:
  jobs=[pool.submit(collect,a) for a in chosen]
  for job in as_completed(jobs):job.result()
