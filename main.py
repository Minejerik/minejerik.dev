from flask import Flask, render_template, abort
from random import choice
import os
import markdown

#USE mjflask

app = Flask(__name__)

cache = {}
nocache = True


@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    if number == 1:
        return singular
    else:
        return plural


# md = Markdown(app)

# defines all possible titles
titles = [
    "Did you know these titles change? Reload the page for another!",
    "hello from flask", "0% javascript", "now w/ less color!", "tf is django",
    "this is a title", "we do a little", "huh",
]

quotes = [
    "We do a little programming",
    "Javascript is a plague on earth",
    "Did you ever think about the fact that earth is the only planet people have died on, and it has javascript?",
    "Covid will last 2 weeks (2020)",
    "these change btw",
    "python is the javascript of programming languages",  # <-- quote
    "me when i deploy this website but forget a major feature",
    "are you still here?",
    "it's not a bug, it's an undocumented feature",
    "i concur",
    "how did they compile the first compiler?",
    "",
    "<a href='https://github.com/Minejerik/minejerik.dev'>SOURCE</a>",
]


@app.route('/')
def index():
    # renders main html file w/ a random title extension
    return render_template("index.html",
                           ran_title=choice(titles),
                           ran_quote=choice(quotes))


def get_blog_metadata(blog_id):
    try:
        with open(f"blog/{blog_id}.md", "r") as f:
            mark = f.read()
    except Exception:
        return None, None, None, None, None

    temp = mark.split("\n")
    title = temp[0]
    title = title.replace("TITLE:", "")
    source = temp[1]
    source = source.replace("SOURCE:", "")
    date = temp[2]
    date = date.replace("DATE:", "")
    content = temp[3:]
    content = "\n".join(content)
    content = content.replace(" .", ".").replace(".\n", ".    \n")

    # read_time = round(len(content.split())/238)
    read_time = len(content.split()) // 150

    return title, source, content, date, read_time


@app.route("/blog")
def blog():
    titles = []
    sources = []
    contents = []
    ids = []
    dates = []
    files = os.listdir("blog")
    posts = [f.replace(".md", "") for f in files]
    posts = sorted(posts)
    posts.reverse()
    for p in posts:
        if p not in cache.keys() or nocache is True:
            title, source, content, date, read = get_blog_metadata(p)
            cache[p] = (title, source, content, date, read)
        else:
            title, source, content, date, read = cache[p]
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


@app.route('/project/<id>')
def project(id):
    if id not in os.listdir("templates/projects"):
        abort(404)
    return render_template(f"projects/{id}/index.html")


# @app.route("/projects")
# def projects():
#   return render_template('project.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/blog/<id>')
def blog_post(id):

    if id not in cache.keys() or nocache is True:
        title, source, content, date, read = get_blog_metadata(id)
        cache[id] = (title, source, content, date, read)
    else:
        title, source, content, date, read = cache[id]
    if title is None:
        abort(404)

    return render_template("blog_post.html",
                           title=title,
                           content=markdown.markdown(str(content)),
                           source=source,
                           date=date,
                           read_time=read)


if __name__ == "__main__":
    app.run(debug=True, use_evalex=False)
