from flask import Flask, render_template, abort
from random import choice
import os
import markdown

app = Flask(__name__)

cache = {}

# md = Markdown(app)

#defines all possible titles
titles = [
    "Did you know these titles change? Reload the page for another!",
    "hello from flask",
    "0% javascript",
    "now w/ less color!",
    "tf is django",
]


@app.route('/')
def index():
  #renders main html file w/ a random title extension
  return render_template("index.html", ran_title=choice(titles))

def get_blog_metadata(blog_id):
  try:
    with open(f"blog/{blog_id}.md","r") as f:
      mark = f.read()
  except Exception:
    return None,None,None,None
  
  temp = mark.split("\n")
  title = temp[0]
  title = title.replace("TITLE:", "")
  source = temp[1]
  source = source.replace("SOURCE:", "")
  date = temp[2]
  date = date.replace("DATE:","")
  content = temp[3:]
  content = "\n".join(content)
  content = content.replace(" .", ".")

  return title, source, content,date
  


@app.route("/blog")
def blog():
  titles = []
  sources = []
  contents = []
  ids = []
  dates = []
  files = os.listdir("blog")
  posts = [f.replace(".md","") for f in files]
  posts.reverse()
  for p in posts:
    if p not in cache.keys():
      title,source,content,date = get_blog_metadata(p)
      cache[p] = (title,source,content,date)
    else:
      title,source,content,date = cache[p]
    titles.append(title)
    sources.append(source)
    contents.append(content)
    dates.append(date)
    ids.append(int(p))
  return render_template("blog.html", 
                         posts=posts,
                         titles=titles, 
                         sources=sources, 
                         contents=contents,
                         dates=dates,
                         ids=ids)


@app.route('/blog/<id>')
def blog_post(id):

  if id not in cache.keys():
    title,source,content,date = get_blog_metadata(id)
    cache[id] = (title,source,content,date)
  else:
    title,source,content,date = cache[id]
  if title is None:
    abort(404)

  return render_template("blog_post.html",
                         title=title,
                         content=markdown.markdown(str(content)),
                         source=source,
                         date=date
                        )


app.run(host='0.0.0.0', port=81, debug=True, use_evalex=False)
