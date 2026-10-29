# Zelenskyy Says

English interface for the public X account of Volodymyr Zelenskyy (@ZelenskyyUa). Original post language only; no translations.

Launch: https://nanalab.kr/zelenskyy-says/

## Coverage and repost filter

Partial snapshot: 140 verified account permalinks, 2026-10-15 through 2026-10-28. Not a full history, live feed, or personal-authorship claim. Native reposts (including self-reposts), other authors and ambiguous records are excluded. Replies are included. Quotes require the account's own added content. Three independent author markers and the native repost header are checked for every record. Evidence is in data/classification-evidence.json; source hashes and exclusions are in data/source-audit.json.

Only factual IDs, dates, account identifiers, classification evidence and original links are stored. Scraped post bodies, translations, media and editorial summaries are not redistributed. The official X embed displays original content; deletion, privacy, regional limits and platform sign-in requirements may prevent display. The original link remains available. Account operation may include staff.

## Navigation

Year → month → random sample of up to 50 collected posts → day → all collected posts for that date → individual static post. The home page does not fetch the corpus. Month data is loaded only for that month's shuffle. Dates use UTC; exact X Snowflake IDs remain strings.

## Build and checks

Python 3.10+ and Node.js 20+, standard libraries only.

```text
python scripts/build_site.py
python scripts/check_site.py
python -m unittest discover -s tests -p test_collect.py
node --test tests/publisher.test.mjs tests/runtime.test.mjs
```

Manual collection: python scripts/collect_posts.py. Cached raw sources stay in ignored .cache/. No authentication, access-control bypass or scheduled collection is used. An unavailable source yields a partial collection with the failure preserved.

GitHub Pages: main:/docs. Every HTML includes the verified GA4, GTM with noscript, AdSense and Cloudflare snippets, canonical URL and More Apps footer. Local publisher requests and embeds are disabled. No search/share text is transmitted as a custom analytics event.

The sitemap.xml index points to sitemap-main.xml and sitemap-posts-01.xml. A parent index must reference these leaf files directly; do not nest sitemap indexes.

## Rights and independence

Original initials SVGs by NaNaCompany; no third-party portraits. Official X embed documentation: https://help.x.com/en/using-x/how-to-embed-a-post. Provider metadata is attributed on Sources & coverage. A dataset or software license does not grant rights to underlying social-post text. No affiliation or endorsement by the account holder, X, Nitter, a government or a political party is implied.

## Ranked home feed

The main page begins with up to 100 collected posts sorted by known source like count. Null counts are excluded from that ordering. It then continues newest first, without popular-post duplicates, using sequential static HTML pages fetched on scroll. Load more remains a normal pagination link without JavaScript. Like totals are snapshots with provenance, not live totals or a complete-account ranking.

The right floating Archive menu offers the existing year/month routes. The full menu is shared and fetched only when needed outside the home. Original platform content automatically loads near the viewport in all lists; retry/original links remain available. Local previews do not send publisher or platform requests. The separate original TXT archive is local only and is not shipped in this repository. No translations or uncleared full post bodies are added to public pages.

Verified portraits keep source, creator, license, modification and hash records on Sources & coverage. Tibo uses the photograph within official X embeds until a standalone reusable portrait is available.

Additional runtime regression suite: node --test tests/feed-runtime.test.mjs. Build and exhaustive page validation remain python scripts/build_site.py and python scripts/check_site.py.
