import importlib.util,unittest
from pathlib import Path
path=Path(__file__).with_name('collect.py')
if not path.exists():path=Path(__file__).resolve().parents[1]/'scripts/collect_posts.py'
spec=importlib.util.spec_from_file_location('collector',path)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def item(author='Example',permalink_author=None,username=None,extra='',content='Own words'):
 return f'<div class="timeline-item" data-username="{author}"><a class="tweet-link" href="/{permalink_author or author}/status/2105860000000000000#m"></a><a class="username" href="/{username or author}">@{username or author}</a><div class="tweet-content">{content}</div>{extra}</div>'.encode()

class RepostFilter(unittest.TestCase):
 def test_own_original_retained(self):
  rows,rejected,_,_=c.parse(item(),'Example');self.assertEqual(len(rows),1);self.assertFalse(rows[0][0]['is_repost']);self.assertEqual(rows[0][0]['post_kind'],'original');self.assertIsNone(rows[0][0]['text'])
 def test_native_repost_excluded_even_when_self_repost(self):
  for author in ('Example','Other'):
   rows,rejected,_,_=c.parse(item(author=author,extra='<div class="retweet-header">Example retweeted</div>'),'Example');self.assertFalse(rows);self.assertEqual(rejected['repost'],1)
 def test_foreign_author_and_mismatches_excluded(self):
  for body in (item(author='Other'),item(permalink_author='Other'),item(username='Other'),item().replace(b'data-username="Example"',b'')):
   self.assertFalse(c.parse(body,'Example')[0])
 def test_reply_retained(self):
  rows=c.parse(item(extra='<div class="replying-to">Replying to @Other</div>'),'Example')[0];self.assertEqual(rows[0][0]['post_kind'],'reply')
 def test_quote_requires_own_authored_content(self):
  quote='<div class="quote quote-big"><a class="username" href="/Other">@Other</a><div class="quote-text">Not ours</div></div>'
  self.assertEqual(c.parse(item(extra=quote),'Example')[0][0][0]['post_kind'],'quote')
  self.assertFalse(c.parse(item(extra=quote,content=''),'Example')[0])
 def test_missing_permalink_and_invalid_time_excluded(self):
  self.assertFalse(c.parse(item().replace(b'class="tweet-link"',b'class="unrelated"'),'Example')[0])
  self.assertFalse(c.parse(item().replace(b'2105860000000000000',b'9999999999999999999'),'Example')[0])
 def test_only_top_level_permalink_counts(self):
  extra='<div class="quote"><a class="quote-link" href="/Other/status/2105860000000000001"></a></div>'
  rows=c.parse(item(extra=extra),'Example')[0];self.assertEqual(rows[0][0]['post_id'],'2105860000000000000')
 def test_displayed_repost_stats_do_not_exclude_original(self):
  rows=c.parse(item(extra='<div class="tweet-stats"><span class="icon-retweet">100</span></div>'),'Example')[0];self.assertEqual(len(rows),1)
 def test_exact_ids_remain_strings_and_author_case_is_insensitive(self):
  rows=c.parse(item(author='eXample'),'Example')[0];self.assertIsInstance(rows[0][0]['post_id'],str);self.assertEqual(rows[0][0]['author'],'Example')

if __name__=='__main__':unittest.main()
