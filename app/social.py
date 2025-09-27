from .llm import LLMClient from .utils
   import clamp_words

   SOCIAL_PROMPT_TMPL = """你是一位公共管理與人資領域的內容編輯。請根據下列資訊，產出一篇適合在社群媒
   體發布的繁體中文短文，總字數不超過
   3,000 字：

   主題與標題：

     * {title}
     * 專題關鍵聚焦：{topic}

   作者指定重點（請務必融合呈現，避免清單堆疊、而是轉為自然段落與故事化描述）： {highlights}

   讀者與平台定位：

     * 預期受眾：{audience}
     * 文體風格（語氣/節奏）：{tone}

   可供參考的學術框架（請轉譯為易懂語句，而非照抄）：

     * 研究分析片段：{analysis_excerpt}
     * 報告摘錄（可選）：{report_excerpt}

   寫作要求：

     * 自然可讀、句型多變、段落節奏有高有低，允許少許冗詞。
     * 避免公式化寫法與明顯 AI 口吻。
     * 保持嚴謹但不艱澀，必要時以簡例說明。
     * 結尾附上 3–6 個精準的主題標籤（#標籤），並給出「延伸閱讀建議」1–2 點。
     * 禁止編造未在原始研究出現的具體數據或結論。
     * 全文字數不超過 3,000 字。
       """

   def generate_social_post(  title: str,  topic: str,  highlights: str,  tone: str
   = "專業中帶溫度，易讀、貼近實務",  audience: str = "政策研究者、政府人資、公共管理碩博士生",
   analysis_excerpt:
   str = "",  report_excerpt: str = "",  model: str = "llama-3.1-70b-versatile" )
   -> str:  prompt = SOCIAL_PROMPT_TMPL.format(  title=title, topic=topic,
   highlights=highlights.strip(),  tone=tone.strip(), audience=audience.strip(),
   analysis_excerpt=(analysis_excerpt or "").strip()[:2000],
   report_excerpt=(report_excerpt or "").strip()[:2000],  )  llm =
   LLMClient(model=model)  text = llm.generate(prompt, max_tokens=1800,
   temperature=0.8)  return clamp_words(text, 3000)