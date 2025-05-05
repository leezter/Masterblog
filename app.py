from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


# Define the path to the JSON file for storing blog posts
BLOG_POSTS_FILE = 'blog_posts.json'


# Initialize the JSON file with some sample data if it doesn't exist
def initialize_blog_posts():
    sample_data = [
        {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
        {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'}
    ]
    try:
        with open(BLOG_POSTS_FILE, 'x') as file:
            json.dump(sample_data, file, indent=4)
    except FileExistsError:
        pass  # File already exists, no need to initialize


# Load blog posts from the JSON file
def load_blog_posts():
    with open(BLOG_POSTS_FILE, 'r') as file:
        return json.load(file)


# Save blog posts to the JSON file
def save_blog_posts(posts):
    with open(BLOG_POSTS_FILE, 'w') as file:
        json.dump(posts, file, indent=4)

# Initialize the blog posts file
initialize_blog_posts()


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Load existing blog posts
        blog_posts = load_blog_posts()

        # Create a new blog post with a unique ID
        new_post = {
            'id': len(blog_posts) + 1,  # Generate a unique ID
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content')
        }

        # Append the new post to the list
        blog_posts.append(new_post)

        # Save the updated list back to the JSON file
        save_blog_posts(blog_posts)

        # Redirect to the home page
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load existing blog posts
    blog_posts = load_blog_posts()

    # Filter out the post with the given ID
    updated_posts = []
    for post in blog_posts:
        if post['id'] != post_id:
            updated_posts.append(post)

    # Save the updated list back to the JSON file
    save_blog_posts(updated_posts)

    # Redirect to the home page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)