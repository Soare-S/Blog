from flask import Flask, request, render_template, redirect
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_posts.json') as json_file:
        blog_posts = json.load(json_file)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
