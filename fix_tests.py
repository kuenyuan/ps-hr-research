from pathlib import Path

   ROOT = Path(file).parent TESTS = ROOT / "tests" TESTS.mkdir(exist_ok=True)

   files = {  TESTS / "test_collection.py": """import app.data_collection as dc

   def test_collect_resources_smoke(monkeypatch):  def fake_crossref(topic,
   rows=25):  return [  {"title": "A", "authors": "X", "year": "2020", "source":
   "crossref", "url": "u",  "pdf_url": None, "doi": None, "abstract": "", "meta":
   {}}  for _ in range(10)  ]

     def fake_s2(topic, limit=15):
         return [
             {"title": "B", "authors": "Y", "year": "2019", "source": "semanticscholar", "url": "u2",
              "pdf_url": None, "doi": None, "abstract": "", "meta": {}}
             for _ in range(10)
         ]

     def fake_wb(topic, rows=10):
         return []

     def fake_gov(topic, limit=10):
         return []

     monkeypatch.setattr(dc, "search_crossref", fake_crossref)
     monkeypatch.setattr(dc, "search_semantic_scholar", fake_s2)
     monkeypatch.setattr(dc, "search_worldbank", fake_wb)
     monkeypatch.setattr(dc, "search_govuk", fake_gov)
     monkeypatch.setattr(dc, "unpaywall_pdf", lambda doi: None)

     out = dc.collect_resources("hr", target=20)
     assert isinstance(out, list)
     assert len(out) == 20

   """,  TESTS / "test_publish.py": """import requests from app.publish import
   publish_wordpress

   class FakeResp:  def init(self, json_data, status=200):  self._json = json_data
   self.status_code = status

     def raise_for_status(self):
         if self.status_code >= 400:
             raise requests.HTTPError("err")

     def json(self):
         return self._json

   def test_publish_wordpress(monkeypatch):  def fake_post(url, auth=None,
   json=None, timeout=60):  return FakeResp({"link": "https://example.com/post/1"}
   (https://example.com/post/1"}))

     monkeypatch.setattr(requests, "post", fake_post)

     import app.config as cfg
     old = (cfg.settings.wordpress_base_url, cfg.settings.wordpress_username,
   cfg.settings.wordpress_app_password)
     cfg.settings.wordpress_base_url = "https://example.com"
     cfg.settings.wordpress_username = "u"
     cfg.settings.wordpress_app_password = "p"
     try:
         link = publish_wordpress("t", "c")
         assert "example.com" in link
     finally:
         cfg.settings.wordpress_base_url, cfg.settings.wordpress_username,
   cfg.settings.wordpress_app_password = old

   """,  TESTS / "test_report.py": """from app import report as rpt from app.utils
   import word_count

   class FakeLLM:  def generate(self, prompt, max_tokens=0, temperature=0.0):
   return "內容 " * 800 # 模擬產生足夠長度的段落

   def test_report_structure_basic(monkeypatch):  monkeypatch.setattr(rpt,
   "LLMClient", lambda model=None: FakeLLM())

     text = rpt.generate_report(
         topic="公部門績效管理",
         analysis="分析摘要",
         resources=[{"title": "t", "authors": "a", "year": "2020", "source": "crossref", "url": "u",
   "pdf_url": None}],
         total_words=2000,
     )
     assert "摘要：" in text
     assert "參考文獻：" in text
     assert word_count(text) > 1000

   """,  TESTS / "test_social.py": """from app import social as soc

   class FakeLLM:  def generate(self, prompt, max_tokens=0, temperature=0.0):
   return "短文 #人資 #公部門 " * 200

   def test_generate_social_post_len(monkeypatch):  monkeypatch.setattr(soc,
   "LLMClient", lambda model=None: FakeLLM())

     text = soc.generate_social_post(
         title="公部門績效管理",
         topic="績效管理與激勵",
         highlights="多維度衡量、公平性、學習與扭曲風險",
         tone="LinkedIn 友善",
         audience="公共管理領域工作者與研究生",
         analysis_excerpt="公平與可操作性的平衡。",
         report_excerpt="比較美英德日澳等國制度...",
     )
     assert len(text.split()) <= 3000
     assert "#" in text

   """, }

   for path, content in files.items():  path.write_text(content, encoding="utf-8")
   head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:2])
   print(f"Wrote {path} preview:\n{head}\n---")

   print("All test files written.")