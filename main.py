from flask import Flask, render_template, abort
from random import choice
import markdown

app = Flask(__name__)

# md = Markdown(app)

#defines all possible titles
titles = [
  "Did you know these titles change? Reload the page for another!",
  "HELLO FROM FLASK",
  "I AM AN EPIC WEBSITE",
  "I HATE JAVASCRIPT",
  "NOW WITH LESS COLOR!",
  "WHAT IS A DJANGO?",
  "IS THE BEST WEBSITE EVER!"
]

@app.route('/')
def index():
  #renders main html file w/ a random title extension
  return render_template("index.html", ran_title = choice(titles))

@app.route('/blog/<id>')
def blog_post(id):

  try:
    with open(f"blog/{id}.md", "r") as f:
      mark = f.read()
  except:
    abort(404)

  temp = mark.split("\n")
  title = temp[0]
  title = title.replace("TITLE:","")
  source = temp[1]
  source = source.replace("SOURCE:","")
  content = temp[2:]
  content = "\n".join(content)
  content = content.replace(" .",".")
  
  return render_template("blog_post.html", 
                         title = title, 
                         content = markdown.markdown(content), 
                         source=source)


app.run(host='0.0.0.0', port=81, debug=True, use_evalex=False)
