# Bibliography verification

Date of every check: **2026-10-24**. Scope: every key in the "Citations needed, by section" table of `notes/OUTLINE.md` (19 keys). All 19 were verified and are in `references.bib`; none was dropped.

What was checked for each entry: title, full author list and order, year, venue, pages and DOI where they exist. Method: for arXiv papers, the abs page (its `citation_*` meta tags) plus the arXiv export API record for authors, version, primary class, journal comment and DOI; for ACM papers, the DOI resolved through doi.org (CSL JSON) and the Crossref record (conference location); for venue claims without a DOI, the OpenReview record (API search, then the forum page, HTTP 200); for software, the GitHub repository and organisation API records; for web pages, the page itself.

Test build: `references.bib` with `\nocite{*}`, `acmart` `sigconf,screen,review` and `ACM-Reference-Format`, compiled with tectonic: 19 entries render, no errors.

## Per key

| Key | URL opened | What it confirmed | Notes |
|---|---|---|---|
| aggarwal2024geo | https://arxiv.org/abs/2311.09735 ; https://doi.org/10.1145/3637528.3671900 | Title; 6 authors (Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande); arXiv comment "Accepted to KDD 2024"; DOI gives KDD '24 proceedings, pp. 5-16, Barcelona | |
| puerto2025cseo | https://arxiv.org/abs/2506.11097 ; https://openreview.net/forum?id=oTeixD3oZO | Title; 5 authors; arXiv comment "Accepted at NeurIPS Datasets & Benchmarks 2025"; OpenReview venue "NeurIPS 2025 Datasets and Benchmarks Track poster" | No DOI or page numbers found; bibtex warns about missing pages |
| vishwakarma2026cited | https://arxiv.org/abs/2605.25517 ; https://doi.org/10.1145/3805712.3808445 | Title; 3 authors (Vishwakarma, Kumar, Jamidar); DOI gives SIGIR '26 proceedings, pp. 4950-4954, Melbourne | Short-paper length (5 pp.) |
| kim2026sageo | https://arxiv.org/abs/2602.12187 ; https://doi.org/10.1145/3770855.3818146 | Title; 5 authors; arXiv comment "Accepted at KDD 2026"; DOI gives KDD '26 proceedings V.2, pp. 2342-2353, Jeju Island | DOI not in the outline; found through Crossref search, then resolved |
| martinez2026survey | https://arxiv.org/abs/2607.14035 | Title "Optimizing Visibility in Generative Engines: A Critical Survey of Generative Engine Optimization (2023-2026)"; single author Olivier Martinez; v1, 15 Jul 2026 | Preprint. Section and table numbers cited in the outline (Table 5; Sections 11.1, 11.2) were not re-checked here |
| wan2024conflictingqa | https://aclanthology.org/2024.acl-long.403/ (and its .bib) | Title "What Evidence Do Language Models Find Convincing?"; Wan, Wallace, Klein; ACL 2024 Vol. 1, pp. 7468-7484, DOI 10.18653/v1/2024.acl-long.403 | The outline's label "ConflictingQA" is the dataset the paper introduces, not its title; the prose should cite it by the paper's title or as "Wan et al." |
| wu2026autogeo | https://arxiv.org/abs/2510.11438 ; https://openreview.net/forum?id=K8EinVWtUB | Title "What Generative Search Engines Like and How to Optimize Web Content Cooperatively"; 4 authors (Wu, Zhong, Kim, Xiong); OpenReview venue "ICLR 2026 Poster" | "AutoGEO" is the method name, not in the title. No page numbers (bibtex warning) |
| zhang2026absorption | https://arxiv.org/abs/2604.25707 | Title; 3 authors; v2, 29 Apr 2026; preprint | Name order: arXiv's meta tags parse them as "Kai, Zhang" etc., but the authors entered surname first ("Zhang Kai", "Yao Jingang"; dataset repo github.com/yaojingang/geo-citation-lab). The bib uses surnames Zhang, He, Yao, matching the outline. Worth a glance at the PDF byline before submission |
| yu2026geosfe | https://arxiv.org/abs/2603.29979 | Title "Structural Feature Engineering for Generative Engine Optimization: How Content Structure Shapes Citation Behavior"; 4 authors (Yu, Yang, Ding, Sato); preprint | "GEO-SFE" is the framework name from the arXiv comment |
| bajemon2026scoring | https://arxiv.org/abs/2609.07559 | Title; 2 authors, Elisha Bajemon and Andre-Louis Rochet (matches the corpus correction); preprint | arXiv comment links a vendor site (Citead.com) and a TW3-Partners reproducibility repo; keep the "vendor-linked" label in the prose |
| schulte2026measure | https://arxiv.org/abs/2604.07585 | Title "Don't Measure Once: Measuring Visibility in AI Search (GEO)"; Schulte, Bleeker, Kaufmann; preprint | |
| chapekis2025pew | https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/ | Headline (h1 and og:title); authors Athena Chapekis and Anna Lieb; published 22 Jul 2025; the page contains the 8%, 15% and 1% figures the outline uses | Browser tab title differs ("Do people click on links in Google AI summaries?"); the bib uses the article headline |
| wang2026aisearch | https://arxiv.org/abs/2608.18352 | Title; 5 authors (Wang, Gleason, Bart, Wilson, Metaxa); v1, 18 Aug 2026; preprint | The 18.8-point figure was re-checked on 2026-10-24 in the arXiv HTML, Section 3 ("reduced click-through rate by -18.8 percentage points (pp)"), and the abstract says "preregistered field experiment (N=1,100)" (notes/verify-claims.md, section D) |
| draxler2024ghostwriter | https://doi.org/10.1145/3637875 | Title; 7 authors; ACM TOCHI 31(2), 1-40, 2024 | |
| dhillon2024scaffolding | https://doi.org/10.1145/3613904.3642134 | Title; 6 authors; CHI '24 proceedings, pp. 1-18, Honolulu | |
| lou2025anchoredai | https://arxiv.org/abs/2509.16128 | Title; 4 authors (Lou, Crowley, Dodson, Yoon); preprint | |
| aiseoaudit | https://github.com/agencyenterprise/aiseo-audit ; https://api.github.com/orgs/agencyenterprise | Repo exists, MIT licence, created 10 Feb 2026, pushed 22 Oct 2026; latest release v2.1.1 (13 Oct 2026); owner organisation display name "AE Studio" | Author field is the organisation name. The bib gives version 2.1.2, commit 6c888aa: the code Citation Equity adapted, per CE/NOTICE and CE/docs/research/2026-10-23-oss-sweep.json line 13 (2.1.1 is only the latest tagged release). Fixed 2026-10-24 (verify-claims A5) |
| geoscore | https://github.com/jianruntech/geo-score ; https://api.github.com/orgs/jianruntech | Repo exists, MIT licence (the outline does not state one), created 8 Sep 2026; latest release v1.8.3 (15 Oct 2026); organisation "Jianrun Tech" | Same as above |
| google-ai-features | https://developers.google.com/search/docs/appearance/ai-features | Page title "AI Features and Your Website"; "Last updated 2025-12-10 UTC" | Living page; re-check the date at submission |

## Dropped

None.

## Open issues

1. Rendering: ACM-Reference-Format prints "Does Conversational SEO Work?." (a period after the question mark) for puerto2025cseo. Cosmetic; fix in the bst call or accept.
2. puerto2025cseo and wu2026autogeo have no page numbers or DOI (OpenReview-hosted venues); bibtex warns but builds.
3. Two notes for the prose, not the bib: wan2024conflictingqa is titled "What Evidence Do Language Models Find Convincing?" (ConflictingQA is its dataset), and wu2026autogeo's title does not contain "AutoGEO".
4. Footnote URLs in the outline (answerlint, GEO Optimizer, the 2 to 3 product pages) are not bib entries and were not checked here.
5. Claims attributed to sources in the outline (for example Martinez Table 5 and Sections 11.1 to 11.2; Wang et al.'s 18.8 points) were not re-checked in this pass; only bibliographic metadata was.
