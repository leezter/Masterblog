# Masterblog

Masterblog is a simple Flask-based blogging application that allows users to create, update, delete, and view blog posts. The application uses a JSON file to store blog posts and provides a user-friendly interface for managing them.

## Features
- View all blog posts on the home page.
- Add new blog posts using a form.
- Update existing blog posts.
- Delete blog posts.

## Project Structure
```
Masterblog/
├── app.py             # Main Flask application
├── blog_posts.json    # JSON file for storing blog posts
├── static/            # Static files (e.g., CSS)
│   └── style.css
├── templates/         # HTML templates
│   ├── add.html
│   ├── index.html
│   └── update.html
└── README.md          # Project documentation
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Masterblog
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Requirements
See `requirements.txt` for the list of dependencies.

## License
This project is licensed under the MIT License.