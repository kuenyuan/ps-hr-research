import requests from
   typing import List, Dict from .config import settings

   HEADERS = {"User-Agent": "ps-hr-research/1.0 (contact:
   {})".format(settings.unpaywall_email or "contact@example.com (
   mailto:contact@example.com)")}

   def search_crossref(topic: str, rows: int = 20) -> List[Dict]:  url = "
   https://api.crossref.org/works (https://api.crossref.org/works)"  params =
   {"query": topic, "rows": rows, "filter": "type:journal-article"}  r =
   requests.get(url, params=params, headers=HEADERS, timeout=30);
   r.raise_for_status()  out = []  for item in r.json().get("message",
   {}).get("items", []):  out.append({  "title": (item.get("title") or [""])[0],
   "authors": ", ".join(a.get("family","") for a in item.get("author", []) if
   "family" in a),  "year": str(item.get("issued", {}).get("date-parts",
   [[None]])[0][0]),  "source": "crossref",  "url": item.get("URL"),  "doi":
   item.get("DOI"),  "abstract": item.get("abstract") or "",  "pdf_url": None,
   "meta": {"publisher": item.get("publisher")}  })  return out

   def search_semantic_scholar(topic: str, limit: int = 15) -> List[Dict]:  url = "
   https://api.semanticscholar.org/graph/v1/paper/search (
   https://api.semanticscholar.org/graph/v1/paper/search)"  params = {"query":
   topic, "limit": limit, "fields":
   "title,year,openAccessPdf,authors,url,abstract"}  headers = HEADERS.copy()  if
   settings.semantic_scholar_api_key:  headers["x-api-key"] =
   settings.semantic_scholar_api_key  r = requests.get(url, params=params,
   headers=headers, timeout=30); r.raise_for_status()  out = []  for item in
   r.json().get("data", []):  out.append({  "title": item.get("title"),  "authors":
   ", ".join(a.get("name","") for a in item.get("authors", [])),  "year":
   str(item.get("year") or ""),  "source": "semanticscholar",  "url":
   item.get("url"),  "doi": None,  "abstract": item.get("abstract") or "",
   "pdf_url": (item.get("openAccessPdf") or {}).get("url"),  "meta": {}  })  return
   out

   def search_worldbank(topic: str, rows: int = 10) -> List[Dict]:  url = "
   https://search.worldbank.org/api/v2/wds (https://search.worldbank.org/api/v2/wds
   )"  params = {"qterm": topic, "format": "json", "rows": rows}  r =
   requests.get(url, params=params, headers=HEADERS, timeout=30);
   r.raise_for_status()  resp = r.json(); recs = resp.get("documents", {}); out =
   []  for _, item in recs.items():  out.append({  "title":
   item.get("display_title"),  "authors": ", ".join(item.get("authors", [])),
   "year": str(item.get("display_year", "")),  "source": "worldbank",  "url":
   item.get("url"),  "doi": item.get("doi"),  "abstract": item.get("abstract", ""),
   "pdf_url": item.get("pdfurl") or item.get("pdfURL"),  "meta": {"country":
   item.get("country")}  })  return out

   def search_govuk(topic: str, limit: int = 10) -> List[Dict]:  url = "
   https://www.gov.uk/api/search.json (https://www.gov.uk/api/search.json)"  params
   = {"q": topic, "count": limit, "filter_content_store_document_type":
   "publication"}  r = requests.get(url, params=params, headers=HEADERS,
   timeout=30); r.raise_for_status()  out = []  for item in r.json().get("results",
   []):  out.append({  "title": item.get("title"), "authors": "", "year": "",
   "source": "govuk",  "url": "https://www.gov.uk (https://www.gov.uk)" +
   item.get("link", ""), "doi": None,  "abstract": item.get("description") or "",
   "pdf_url": None, "meta": {"organisations": item.get("organisations")}  })
   return out

   def unpaywall_pdf(doi: str | None) -> str | None:  if not doi or not
   settings.unpaywall_email:  return None  url = f"
   https://api.unpaywall.org/v2/{doi} (https://api.unpaywall.org/v2/{doi})"  params
   = {"email": settings.unpaywall_email}  r = requests.get(url, params=params,
   headers=HEADERS, timeout=30)  if r.status_code != 200:  return None  data =
   r.json(); oa = data.get("best_oa_location") or {}  return oa.get("url_for_pdf")
   or oa.get("url")

   def collect_resources(topic: str, target: int = 50) -> List[Dict]:  results:
   List[Dict] = []  for block in [lambda: search_crossref(topic, rows=25),  lambda:
   search_semantic_scholar(topic, limit=15),  lambda: search_worldbank(topic,
   rows=10),  lambda: search_govuk(topic, limit=10)]:  try:  items = block();
   results.extend(items)  except Exception:  pass  if len(results) >= target: break
   seen = set(); deduped = []  for it in results:  key = (it.get("title") or "",
   it.get("url") or "")  if key in seen: continue  seen.add(key)  if not
   it.get("pdf_url"):  it["pdf_url"] = unpaywall_pdf(it.get("doi"))
   deduped.append(it)  if len(deduped) >= target: break  return deduped