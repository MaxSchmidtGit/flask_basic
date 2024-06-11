from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


# Funktion zum Laden von Blogbeiträgen aus der JSON-Datei
def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    return blog_posts


# Funktion zum Speichern von Blogbeiträgen in die JSON-Datei
def save_blog_posts(blog_posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file)


# Funktion zum Abrufen eines Blogbeitrags nach ID
def fetch_post_by_id(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        blog_posts = load_blog_posts()
        new_id = max([post['id'] for post in blog_posts]) + 1 if blog_posts else 1
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content,
            'likes': 0
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        blog_posts = load_blog_posts()
        for i, p in enumerate(blog_posts):
            if p['id'] == post_id:
                blog_posts[i] = post
                break
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
