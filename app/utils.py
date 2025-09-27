import re def word_count(text: str) ->
   int:  return len(re.findall(r"\b\w+\b", text)) def clamp_words(text: str,
   max_words: int) -> str:  words = re.findall(r"\b\w+\b", text)  if len(words) <=
   max_words:  return text  i = 0; cnt = 0; out = []  for token in
   re.finditer(r"\b\w+\b|\W+", text):  out.append(token.group(0))  if
   re.match(r"\b\w+\b", token.group(0)):  cnt += 1  if cnt >= max_words:  break
   return "".join(out)