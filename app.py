
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_blog_posts():
    with open("data/data.json", "r") as file:
        return json.load(file)

def save_blog_post(blog_posts):
    with open("data/data.json", "w") as file:
        json.dump(blog_posts, file)
    print("Posts saved:", blog_posts)  # Debugging line to show what is being saved


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


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Load all blog posts
    blog_posts = load_blog_posts()

    # Find the post by its ID (directly in the update function)
    post = None
    for p in blog_posts:
        if p['id'] == post_id:
            post = p
            break

    # If the post is not found, return a 404 error
    if post is None:
        return "Post not found", 404

    # Handle POST request (form submission)
    if request.method == 'POST':
        # Get updated values from the form
        new_author = request.form['author']
        new_title = request.form['title']
        new_content = request.form['content']

        # Debugging: Show the updated data before saving
        print(f"Updating post {post_id}: author={new_author}, title={new_title}, content={new_content}")

        # Update the post with the new values
        post['author'] = new_author
        post['title'] = new_title
        post['content'] = new_content

        # Save the updated blog posts list back to the file
        save_blog_post(blog_posts)

        # Debugging: Confirm save action
        print("Post saved. Redirecting to home...")

        return redirect(url_for('index'))

    # Handle GET request (render the update form)
    else:
        return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)