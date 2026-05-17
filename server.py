from flask import Flask, jsonify, request
from collections import deque

app = Flask(__name__)

queue = deque()
seen = set()  # prevents same username being added twice

# TikTok listener runs separately, posts to this endpoint
@app.route('/add', methods=['POST'])
def add_username():
    data = request.json
    username = data.get('username', '').strip()
    if username and username.lower() not in seen:
        seen.add(username.lower())
        queue.append(username)
    return jsonify({'ok': True})

# Roblox polls this every second
@app.route('/next', methods=['GET'])
def next_username():
    if queue:
        username = queue.popleft()
        seen.discard(username.lower())
        return jsonify({'username': username})
    return jsonify({'username': None})

# Roblox fetches this for the waitlist UI
@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify({'queue': list(queue)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)