from flask import Flask, render_template, abort
from random import choice
import os
import json
from datetime import datetime
import markdown
import functools

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

ALL_TAGS = []

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
    posts_data = []
    files = os.listdir("blog")
    posts = [f.replace(".md", "") for f in files]
    posts.remove("example")
    posts = [int(f) for f in posts]
    posts = sorted(posts)
    posts.reverse()
    posts = posts[0:3]
    posts = [get_blog_metadata(post) for post in posts]

    return render_template("index.html",
                           ran_title=choice(titles),
                           ran_quote=choice(quotes),
                           new_posts=posts)

# @functools.cache
def get_blog_metadata(blog_id):

    base = {
        "title":"",
        "source":"",
        "content":"content",
        "date":"",
        "read_time":"",
        "tags":[],
        "description":"",
        "id":""
    }

    try:
        with open(f"blog/{blog_id}.md", "r") as f:
            mark = f.read()
    except Exception:
        return base

    temp = mark.split("\n")

    data = json.loads(temp[0])

    base['title'] = data['title'].replace("\n","")
    base['source'] = data['source']
    base['date'] = datetime.strptime(data['date'], "%m-%d-%Y").strftime("%B %d %Y")
    base['tags'] = data['tags']
    base['description'] = data['description']
    base['id'] = blog_id

    content = temp[3:]
    content = "\n".join(content)
    base['content'] = markdown.markdown(content)

    # read_time = round(len(content.split())/238)
    base["read_time"] = len(content.split()) // 150
    return base

@app.route("/tag/<tag_name>")
def tag_search(tag_name):
    posts_data = []
    files = os.listdir("blog")
    posts = [f.replace(".md", "") for f in files]
    posts.remove("example")
    posts = [int(f) for f in posts]
    posts = sorted(posts)
    posts.reverse()
    for p in posts:
        data = get_blog_metadata(p)
        if tag_name in data['tags']:
            posts_data.append(data)

    return render_template("tag.html", tags=tag_name, posts=posts_data)

@app.route("/blog")
def blog():
    global ALL_TAGS
    posts_data = []
    files = os.listdir("blog")
    posts = [f.replace(".md", "") for f in files]
    posts.remove("example")
    posts = [int(f) for f in posts]
    posts = sorted(posts)
    posts.reverse()
    for p in posts:
        data = get_blog_metadata(p)
        ALL_TAGS += data['tags']
        posts_data.append(data)
    ALL_TAGS = sorted(list(set(ALL_TAGS)))

    return render_template("blog.html", posts=posts_data, tags=ALL_TAGS)


# @app.route('/project/<id>')
# def project(id):
#     if id not in os.listdir("templates/projects"):
#         abort(404)
#     return render_template(f"projects/{id}/index.html")


# @app.route("/projects")
# def projects():
#   return render_template('project.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/blog/<id>')
def blog_post(id):

    post_data = get_blog_metadata(id)

    if post_data["title"] == "":
        abort(404)

    return render_template("blog_post.html",post_data=post_data)


if __name__ == "__main__":
    app.run("localhost", debug=True, use_evalex=False)
