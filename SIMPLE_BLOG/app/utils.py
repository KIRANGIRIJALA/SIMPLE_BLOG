from flask import jsonify

def validate_post(data):
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    return None
