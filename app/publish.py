import requests from .config import
   settings

   def publish_wordpress(title: str, content: str) -> str:  if not
   (settings.wordpress_base_url and settings.wordpress_username and
   settings.wordpress_app_password):  raise RuntimeError("WordPress config
   missing")  api =
   f"{settings.wordpress_base_url.rstrip('/')}/wp-json/wp/v2/posts"  auth =
   (settings.wordpress_username, settings.wordpress_app_password)  r =
   requests.post(api, auth=auth, json={"title": title, "content": content,
   "status": "publish"}, timeout=60)  r.raise_for_status()  return
   r.json().get("link")

   def publish_blogger(blog_id: str, title: str, content: str, access_token: str)
   -> str:  url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/ (
   https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/)"  headers =
   {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
   r = requests.post(url, headers=headers,
   json={"kind":"blogger#post","title":title,"content":content}, timeout=60)
   r.raise_for_status()  return r.json().get("url")