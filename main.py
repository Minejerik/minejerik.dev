from flask import Flask, render_template
from random import choice

app = Flask(__name__)


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


app.run(host='0.0.0.0', port=81, debug=True, use_evalex=False)
