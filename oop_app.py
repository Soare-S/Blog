from flask import Flask, request, render_template, redirect, url_for
import json


class Blog:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
        self.likes = 0

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'likes': self.likes
        }


class BlogStorage:
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.posts = self.load_posts()

    def load_posts(self):
        with open(self.storage_file) as json_file:
            blog_posts = json.load(json_file)
        return blog_posts

    def save_posts(self):
        with open(self.storage_file, 'w') as json_file:
            json.dump(self.posts, json_file, indent=4)


app = Flask(__name__)
storage = BlogStorage('storage.json')


@app.route('/home')
def index():
    return render_template('index.html', posts=storage.posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        new_blog = Blog(title, content, author)
        storage.posts.append(new_blog.to_dict())
        storage.save_posts()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    storage.posts = [post for post in storage.posts if post['id'] != post_id]
    storage.save_posts()
    return redirect(url_for('index'))


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = next((post for post in storage.posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        post['author'] = request.form.get('author')
        storage.save_posts()
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    post = next((post for post in storage.posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    post['likes'] += 1
    storage.save_posts()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
