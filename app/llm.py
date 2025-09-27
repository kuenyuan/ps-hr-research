from .config import settings try:  from groq
   import Groq except Exception:  Groq = None try:  from huggingface_hub import
   InferenceClient except Exception:  InferenceClient = None

   class LLMClient:  def init(self, model: str = "llama-3.1-70b-versatile"):
   self.model = model  self.groq = Groq(api_key=settings.groq_api_key) if (Groq and
   settings.groq_api_key) else None  self.hf = InferenceClient() if InferenceClient
   else None  def generate(self, prompt: str, max_tokens: int = 2048, temperature:
   float = 0.7) -> str:  if self.groq:  resp = self.groq.chat.completions.create(
   model=self.model,  messages=[{"role": "user", "content": prompt}],
   max_tokens=max_tokens,  temperature=temperature,  )  return
   resp.choices[0].message.content  if self.hf:  return
   self.hf.text_generation(prompt, max_new_tokens=max_tokens,
   temperature=temperature)  raise RuntimeError("No LLM backend configured")