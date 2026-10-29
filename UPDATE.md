# Updates

## 2026-10-29 — Initial app

- English UI; original post language only, without translations.
- 140 account permalinks, 2026-10-15–2026-10-28, partial snapshot.
- Native reposts excluded; author-marker and authored-quote checks recorded for every retained post. Other authors and ambiguous records excluded.
- Year/month/day navigation, up to 50 random monthly records, complete collected-day lists, static detail pages, original links, official X embeds, canonical copy/share links and recovery fallback.
- Original initials graphics; no scraped bodies, images, translations or third-party summaries redistributed.
- GA4, GTM plus noscript, AdSense and Cloudflare from the verified publisher template on every HTML; local requests disabled; More Apps footer.
- Leaf sitemaps prepared for parent-index integration. Local checks and public release status are recorded in evidence/. Deployment is not established by this initial note alone.

- Local validation passed: 158 HTML pages, author/repost evidence for every post, reciprocal navigation and complete sitemap coverage, 9 collector regression tests and 13 publisher/runtime tests. Mobile home, month shuffle and day navigation passed; desktop shared-template geometry and local embed fallback/copy toast also checked. Actual OS sharing delivery is not claimed.

## 2026-10-29 — Ranked home feed and archive menu

- The home shows up to 100 collected posts with known source like counts, highest first. This snapshot contains 140 known-count and 0 unknown-count eligible records. Unknown is never rendered as zero. Source metrics are historical snapshots, not live counters; provenance and capture precision are retained.
- The newest collected posts continue through 2 static HTML pages, 20 per page. The home and continuations exclude duplicate popular records and explicitly classified reposts. Each next link works as ordinary pagination without JavaScript. Runtime HTML parsing validates IDs, authors, dates, canonical URLs, sequential next links and chronological order before reconstructing inert cards.
- Original content is loaded automatically near the viewport in the main, month and day lists through official platform embeds, with at most three active initializations. Manual retry and original links remain available. Full original text is separately recorded in a local TXT archive with ID offsets and hashes; that private archive is not included in this public repository. No translations or uncleared full bodies are newly redistributed.
- The right floating Archive control opens year/month navigation. The home renders its menu directly; other pages load the shared archive-menu.html on demand to avoid copying years of navigation into tens of thousands of pages. Escape, outside click, focus return, failed loading and retry are supported.
- A verified public-license/public-domain portrait is used with original-source attribution, license URL, download hash and modification notice on Sources & coverage.
- Existing detail URLs, original links, UTC/source calendar dates, monthly shuffle and day navigation are preserved. Verified repost-only historical dates keep their existing route with an empty eligible list rather than silently disappearing.
- Every HTML including feed and archive-menu pages retains GA4, GTM with noscript, AdSense, Cloudflare, a self canonical and More Apps. Publisher and embed requests are disabled on local hosts; the preview CSP also blocks the noscript frame. Bottom spacing and floating-menu offsets leave room for observed mobile ad anchors; third-party ad height may vary.
- Shared feed runtime regression tests cover HTML pagination, deduplication/order, concurrent loading, errors/retry, unsafe URLs/HTML, lazy embeds, source availability, menu fetching/keyboard/focus, mutation cleanup and unavailable IntersectionObserver. Full static checks validate every generated page and source-backed ranking.

## 2026-10-29 · Expanded mobile anchor navigation fix

- Move the floating Archive button to the right middle of the viewport (40% from the top). On mobile, keep the archive panel controls below top anchors and above expanded bottom anchors. An expanded production advertisement had intercepted the previous bottom button. Publisher integrations and ad settings remain unchanged.
- Verified locally at 375 × 812: visible menu open/close, month navigation, lazy archive menu and shuffled 50-card content. Only the shared stylesheet and this record changed; source data, generated HTML and the tested feed runtime remain unchanged. Production verification is recorded separately.

## 2026-10-29 · Cache-aware navigation stylesheet release

- Refresh the static asset version in every generated HTML page so existing browser caches request the corrected navigation stylesheet immediately after the new page is served. Python builds already derive this version from the asset hash; Trump build sources now use the new CSS release version. Every changed HTML byte is accounted for by the exact old-to-new version replacement. No post contents or sitemap URLs changed.


## 2026-10-29 — Text-first lists and full captured source text on details

- User-requested display policy: home, continuation, month, day and shuffled list cards render text-first previews linking to the existing individual static detail pages. Lists do not initialize platform embeds; individual details retain both available captured text and the official embed/original link.
- Previews are capped at 800 Unicode characters including the ellipsis: when longer, 799 source characters plus one … character. The captured source string remains intact; individual details display the entire captured available string rather than the preview truncation.
- Public text is supplied by the separate data/post-texts.json overlay, without rewriting data/posts.json. Source text stays in its original language. Partial source strings, original-page metadata descriptions, empty bodies and unavailable text retain accurate source/status labels. A source description is not relabeled as a complete authored post; missing text is not inferred, translated or generated.
- This supersedes the earlier feed's metadata/embed-only display policy. Historical UPDATE entries remain unchanged as records of their release. Source provenance, rights declarations and original snapshot boundaries remain applicable.
- Existing portraits and their creator/source/license/hash records, four publisher integrations with GTM noscript, local-host request guards, More Apps, original permalinks, static page paths and canonical identities are preserved by the requested change. Source like-count snapshots, repost exclusions, archive navigation and chronological pagination remain part of the feed contract.
- Release evidence directory: .tools/says-text-first-20261029/. This documentation entry records the requested source/UI policy; it does not by itself establish completed build/tests, commit/push, Pages publication, production HTTP/browser verification or search-engine indexing. The parent release workflow records those outcomes separately.


## 2026-10-29 — Homepage social preview image

- Added one set of Open Graph image URL/alt/width/height/type and Twitter/X large-image card/image/alt tags on the canonical homepage only. The existing JPEG at https://nanalab.kr/zelenskyy-says/assets/portrait.jpg is used unchanged (960 × 1300 pixels).
- Added a source build helper that reads the JPEG dimensions and verifies its bytes against the existing portrait-credit SHA256 before generating homepage metadata. Creator attribution, source, license and modification notices remain unchanged.
- Local validation: no duplicate image tags; generated homepage tags match the directly updated homepage; source helper emits no image tags for a non-home page. Removing the inserted tags exactly restores the original homepage bytes. Body content, scripts, publisher integrations, APIs and existing non-home HTML are preserved. No full build, commit, push or deployment is claimed by this note.
