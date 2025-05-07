from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


# Define the path to the JSON file for storing blog posts
BLOG_POSTS_FILE = 'blog_posts.json'


def initialize_blog_posts():
    """
    Initialize the JSON file with sample data if it doesn't exist.
    """
    sample_data = [
        {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
        {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'}
    ]
    try:
        with open(BLOG_POSTS_FILE, 'x') as file:
            json.dump(sample_data, file, indent=4)
    except FileExistsError:
        pass  # File already exists, no need to initialize


def load_blog_posts():
    """
    Load blog posts from the JSON file.

    Returns:
        List of blog posts.
    """
    with open(BLOG_POSTS_FILE, 'r') as file:
        return json.load(file)


def save_blog_posts(posts):
    """
    Save blog posts to the JSON file.

    Args:
        posts (list): List of blog posts to save.
    """
    with open(BLOG_POSTS_FILE, 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    """
    Handle the root route ('/').

    Fetch all blog posts from the JSON file and render the 'index.html' template,
    passing the list of blog posts to the template.

    Returns:
        Rendered HTML page displaying all blog posts.
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle the '/add' route.

    On GET, render the 'add.html' template to display the form.
    On POST, add a new blog post to the JSON file and redirect to the home page.

    Returns:
        Rendered HTML page or redirect to the home page.
    """
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
    """
    Handle the '/delete/<post_id>' route.

    Remove the blog post with the given ID from the JSON file and redirect to the home page.

    Args:
        post_id (int): ID of the blog post to delete.

    Returns:
        Redirect to the home page.
    """
    # Load existing blog posts
    blog_posts = load_blog_posts()

    # Find and remove the post with the given ID
    updated_posts = []
    for post in blog_posts:
        if post['id'] != post_id:
            updated_posts.append(post)

    # Reassign unique IDs to ensure no conflicts
    for index, post in enumerate(updated_posts, start=1):
        post['id'] = index

    # Save the updated list back to the JSON file
    save_blog_posts(updated_posts)

    # Redirect to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle the '/update/<post_id>' route.

    On GET, render the 'update.html' template with the current post details.
    On POST, update the blog post in the JSON file and redirect to the home page.

    Args:
        post_id (int): ID of the blog post to update.

    Returns:
        Rendered HTML page or redirect to the home page.
    """
    # Fetch the blog posts from the JSON file
    blog_posts = load_blog_posts()

    # Find the post with the given ID
    post = None
    for p in blog_posts:
        if p['id'] == post_id:
            post = p
            break

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post details
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save the updated list back to the JSON file
        save_blog_posts(blog_posts)

        # Redirect back to the index page
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


def main():
    """
    Main function to initialize the application and run the Flask server.
    """
    # Initialize the blog posts file
    initialize_blog_posts()

    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()