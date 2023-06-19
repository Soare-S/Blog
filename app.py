from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


@app.route('/home')
def index():
    with open('storage.json') as json_file:
        blog_posts = json.load(json_file)
    return render_template('index.html', posts=blog_posts)


def generate_unique_id():
    with open('storage.json', 'r') as file:
        data = json.load(file)
        post_id = int(len(data) + 1)
        for post in data:
            if post_id == post["id"]:
                post_id = post_id + 1
        return post_id


def append_to_storage(new_post):
    with open('storage.json', 'r+') as file:
        data = json.load(file)
        data.append(new_post)
        file.seek(0)
        json.dump(data, file, indent=4)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Add the code that handles adding a new blog
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        # Generate a unique ID for the new blog post
        new_post_id = generate_unique_id()
        # Create a new blog post dictionary
        new_post = {
            'id': new_post_id,
            'title': title,
            'content': content,
            'author': author
        }
        # Append the new blog post to the blog_posts list
        append_to_storage(new_post)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    with open("storage.json") as handle:
        data = json.load(handle)
    updated_posts = [post for post in data if post['id'] != post_id]
    data = updated_posts
    with open('storage.json', 'w') as file:
        json.dump(data, file, indent=4)
    # Redirect back to the home page
    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    with open('storage.json', 'r') as f:
        data = json.load(f)
        for post in data:
            if post['id'] == post_id:
                return post
    return None


def update_post(post):
    with open('storage.json', 'r+') as file:
        data = json.load(file)
        for existing_post in data:
            if existing_post['id'] == post['id']:
                existing_post['title'] = post['title']
                existing_post['content'] = post['content']
                existing_post['author'] = post['author']
                break
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    # Fetch the blog post from the storage
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404
    if request.method == 'POST':
        # Update the post in the storage
        updated_title = request.form.get('title')
        updated_content = request.form.get('content')
        updated_author = request.form.get('author')
        # Update the post's fields
        post['title'] = updated_title
        post['content'] = updated_content
        post['author'] = updated_author
        # Update the storage
        update_post(post)
        # Redirect back to the index page
        return redirect(url_for('index'))
    # Else, it's a GET request
    # So display the edit.html page
    return render_template('edit.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    # Fetch the blog posts from the storage
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404
    # Increment the 'likes' value of the post
    post['likes'] += 1
    # Update the post in the storage
    update_post(post)
    # Redirect back to the index page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
