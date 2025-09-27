from typing import List, Dict from
   .utils import word_count, clamp_words from .llm import LLMClient

   APA_TMPL = """標題：{title}

   摘要： {abstract}

   關鍵詞：{keywords}

   一、前言 {intro}

   二、文獻回顧 {lit_review}

   三、方法論 {method}

   四、討論 {discussion}

   五、結論 {conclusion}

   參考文獻： {references} """

   SECTION_PROMPT = """請以繁體中文撰寫學術報告的「{section}」部分，主題：{topic}。 要求：

     * 風格自然、具反思與脈絡，句型多變，允許少許冗詞與非標準表述。
     * 請結合先前文獻分析的結論（如下），避免重複抄寫，做適度延伸。
     * 嚴謹但可讀。
       文獻分析重點：
       {analysis}
       請產出約 {words} 字。"""

   def build_references(resources: List[Dict]) -> str:  out = []  for r in
   resources[:50]:  authors = r.get("authors") or ""  year = r.get("year") or
   "n.d."  title = (r.get("title") or "").strip()  url = r.get("url") or
   r.get("pdf_url") or ""  out.append(f"{authors}（{year}）。{title}。{url}")  return
   "\n".join(out)

   def generate_report(topic: str, analysis: str, resources: List[Dict],
   total_words: int = 12000, model: str = "llama-3.1-70b-versatile") -> str:
   budget = {"abstract": 300, "intro": 2000, "lit_review": 4000, "method": 1500,
   "discussion": 2500, "conclusion": 1000}  llm = LLMClient(model=model)  title =
   f"{topic}：公部門人力資源制度與實務之比較研究"; keywords = "公部門, 人力資源, 招募, 績效, 訓練,
   制度"  def
   gen(section, words):  prompt = SECTION_PROMPT.format(section=section,
   topic=topic, analysis=analysis, words=words)  return llm.generate(prompt,
   max_tokens=min(3500, int(words*2)), temperature=0.8)  abstract =
   clamp_words(gen("摘要", budget["abstract"]), 400)  intro = gen("前言",
   budget["intro"])  lit_review = gen("文獻回顧", budget["lit_review"])  method =
   gen("方法論", budget["method"])  discussion = gen("討論", budget["discussion"])
   conclusion = gen("結論", budget["conclusion"])  references =
   build_references(resources)  report = APA_TMPL.format(title=title,
   abstract=abstract, keywords=keywords, intro=intro, lit_review=lit_review,
   method=method, discussion=discussion, conclusion=conclusion,
   references=references)  wc = word_count(report)  if wc > 15000:  report =
   clamp_words(report, 15000)  return report