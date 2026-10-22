"""Web research: up-to-date facts and learning resources (videos, articles) for the lesson.

Two jobs, both optional (no TAVILY_API_KEY or WEB_RESEARCH=off -> curated sheet only):

  1. Fresh facts. Tavily search results are distilled by the model into a few short,
     beginner-relevant facts, each tied to a source URL. They are added to the reference
     sheet as `web_facts` (lower trust than the curated facts, and labelled as such), so
     the writer can mention recent developments and the accuracy judge can check them.
  2. Resources. Candidate links come from the curated sheet plus web search (YouTube and
     articles, including a Hindi explainer search for this learner). Every link is checked
     live before use: YouTube through oEmbed (404s for removed or fake videos), other pages
     by fetching them. Only verified links reach the writer, and rule R6 rejects any URL
     in the lesson that is not on that verified list. Models invent plausible URLs, so
     "the model said so" is never enough.

Results are cached per topic per day under knowledge/web/, which keeps reruns cheap and
reproducible, and the rejection log lists every source used.
"""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pydantic import BaseModel, Field

_UA = {"User-Agent": "Mozilla/5.0 (lesson-agent link checker)", "Accept-Language": "en"}
_YT = re.compile(r"^https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})")


class WebFact(BaseModel):
    fact: str = Field(description="One short, plain-English fact a beginner can understand.")
    source_url: str = Field(description="URL of the search result the fact came from, copied exactly.")


class WebFacts(BaseModel):
    facts: list[WebFact] = Field(description="0-6 facts. Empty if the results contain nothing reliable and relevant.")


WEB_FACTS_SYSTEM = """\
You extract up-to-date facts for a beginner lesson from web search results. Rules:
- Use ONLY what the results say. Never add facts from memory.
- Keep only facts that are relevant to a beginner, widely agreed, and not marketing claims or predictions.
- If a result contradicts the reference facts, leave it out.
- Each fact: one short sentence in simple English, with the URL of the result it came from."""


# ---- search -------------------------------------------------------------------------------

def _client(settings):
    from tavily import TavilyClient

    return TavilyClient(api_key=settings.tavily_api_key)


def search(settings, query: str, **kw) -> list[dict]:
    try:
        return _client(settings).search(query, max_results=kw.pop("max_results", 5), **kw).get("results", [])
    except Exception as e:  # network, quota, auth: research is best-effort, never fatal
        print(f"    (web search failed for {query!r}: {e})", flush=True)
        return []


# ---- link verification --------------------------------------------------------------------

def _get(url: str, timeout: float = 12) -> tuple[int, str]:
    with urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=timeout) as r:
        return r.status, r.read(400_000).decode("utf-8", "ignore")


def verify(url: str) -> dict | None:
    """Live check. Returns the confirmed title (and channel / length for videos), or None."""
    try:
        m = _YT.match(url)
        if m:
            api = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")
            info = json.loads(_get(api)[1])
            out = {"url": f"https://www.youtube.com/watch?v={m.group(1)}", "type": "video",
                   "title": info["title"], "source": info.get("author_name", "")}
            try:  # length is nice to have for a learner, not required
                secs = re.search(r'"lengthSeconds":"(\d+)"', _get(out["url"])[1])
                if secs:
                    out["minutes"] = round(int(secs.group(1)) / 60)
            except Exception:
                pass
            return out
        status, html = _get(url)
        if status >= 400:
            return None
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
        return {"url": url, "type": "article", "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else url,
                "source": urllib.parse.urlparse(url).netloc.removeprefix("www.")}
    except Exception:
        return None


def verify_all(candidates: list[dict]) -> list[dict]:
    """Verify in parallel; keep curated notes (why/language) and drop anything that fails."""
    with ThreadPoolExecutor(max_workers=8) as pool:
        checked = list(pool.map(lambda c: verify(c["url"]), candidates))
    out, seen = [], set()
    for cand, ok in zip(candidates, checked):
        if ok and ok["url"] not in seen:
            seen.add(ok["url"])
            out.append({**ok, **{k: v for k, v in cand.items() if k in ("why", "language", "curated", "minutes")},
                        "language": cand.get("language") or ("Hindi" if "hindi" in ok["title"].lower() else "English")})
    return out


# ---- the research step ----------------------------------------------------------------------

def _cache_path(settings, topic: str) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:50]
    return settings.knowledge_dir / "web" / f"{slug}-{time.strftime('%Y%m%d')}.json"


def research(topic: str, reference: dict, llm, settings, log=print) -> dict:
    """Return {'resources': [...verified...], 'web_facts': [...], 'sources': [...]} for this topic."""
    curated = [{**r, "curated": True} for r in reference.get("resources", [])]
    if not settings.verify_links:  # offline tests: trust the curated sheet as-is
        return {"resources": curated, "web_facts": [], "sources": []}
    if not settings.web_research:
        res = verify_all(curated) if curated else []
        log(f"[research] web research off; {len(res)}/{len(curated)} curated resources verified live")
        return {"resources": res, "web_facts": [], "sources": []}

    cache = _cache_path(settings, topic)
    if cache.exists():
        data = json.loads(cache.read_text(encoding="utf-8"))
        log(f"[research] using today's cached web research ({len(data['resources'])} resources, "
            f"{len(data['web_facts'])} fresh facts)")
        return data

    short = reference.get("short_name") or topic
    videos = search(settings, f"{short} explained for beginners", include_domains=["youtube.com"])
    hindi = search(settings, f"{short} explained in Hindi", include_domains=["youtube.com"], max_results=3)
    news = search(settings, f"{short} latest developments", time_range="year", max_results=5)

    candidates = curated + [{"url": r["url"]} for r in videos + hindi if _YT.match(r["url"])]
    resources = verify_all(candidates)
    log(f"[research] resources: {len(resources)} verified live out of {len(candidates)} candidates "
        f"({sum(r['type'] == 'video' for r in resources)} videos, "
        f"{sum(r.get('language') == 'Hindi' for r in resources)} in Hindi)")

    facts = []
    if news:
        results = "\n\n".join(f"[{r['url']}] {r['title']}\n{r.get('content', '')[:800]}" for r in news)
        try:
            out = llm.structured(WEB_FACTS_SYSTEM,
                                 f"Topic: {topic}\n\nReference facts (do not contradict):\n"
                                 + "\n".join(f"- {f}" for f in reference.get("facts", []))
                                 + f"\n\nSearch results:\n{results}", WebFacts, role="evaluator")
            urls = {r["url"] for r in news}
            facts = [f.model_dump() for f in out.facts if f.source_url in urls]  # drop invented sources
        except Exception as e:
            log(f"[research] could not distil web facts: {e}")
    log(f"[research] fresh facts from the web: {len(facts)}")

    data = {"resources": resources, "web_facts": facts,
            "sources": [r["url"] for r in news], "searched": time.strftime("%Y-%m-%d")}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data
