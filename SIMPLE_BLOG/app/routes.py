from flask import Blueprint, request, jsonify
from .models import Post
from . import db
from .utils import validate_post

main = Blueprint('main', __name__)

@main.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])

@main.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post.to_dict())

@main.route('/posts', methods=['POST'])
def create_post():
    error = validate_post(request.get_json())
    if error:
        return error
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@main.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    error = validate_post(request.get_json())
    if error:
        return error
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify(post.to_dict())

@main.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})
