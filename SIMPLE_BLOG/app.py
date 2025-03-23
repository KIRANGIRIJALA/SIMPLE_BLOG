from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "posts.json"

def load_posts():
    """Loads blog posts from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_posts(posts):
    """Saves blog posts to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

posts = load_posts()
next_post_id = len(posts) + 1

@app.route('/posts', methods=['GET'])
def get_posts():
    """Returns a list of all blog posts."""
    return jsonify(posts)

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Returns a specific blog post by ID."""
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({'message': 'Post not found'}), 404

@app.route('/posts', methods=['POST'])
def create_post():
    """Creates a new blog post."""
    global next_post_id
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Title and content are required'}), 400
    new_post = {'id': next_post_id, 'title': data['title'], 'content': data['content']}
    posts.append(new_post)
    save_posts(posts)
    next_post_id += 1
    return jsonify(new_post), 201

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Updates an existing blog post."""
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        data = request.get_json()
        if data and 'title' in data:
            post['title'] = data['title']
        if data and 'content' in data:
            post['content'] = data['content']
        save_posts(posts)
        return jsonify(post)
    return jsonify({'message': 'Post not found'}), 404

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Deletes a blog post by ID."""
    global posts
    initial_len = len(posts)
    posts = [p for p in posts if p['id'] != post_id]
    if len(posts) < initial_len:
        save_posts(posts)
        return jsonify({'message': 'Post deleted'})
    return jsonify({'message': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
