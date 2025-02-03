
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_blog_posts():
    with open("data/data.json", "r") as file:
        return json.load(file)

def save_blog_post(blog_posts):
    with open("data/data.json", "w") as file:
        return json.dump(blog_posts, file)

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    blog_posts = load_blog_posts()
    if request.method == 'POST':

        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]

        if blog_posts:
            new_id = max(post["id"] for post in blog_posts) + 1
        else:
            new_id = 1

        new_post = {
            "id" : new_id,
            "author" : author,
            "title" : title,
            "content" : content
                }
        blog_posts.append(new_post)
        save_blog_post(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_blog_posts()
    new_list_of_blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_blog_post(new_list_of_blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)