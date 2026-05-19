from flask import Flask, jsonify, request
from collections import deque

app = Flask(__name__)

queue = deque()
seen = set()
gift_queue = deque()

tiktok_to_roblox = {}  # tiktok nickname → roblox username

@app.route('/add', methods=['POST'])
def add_username():
    data = request.json
    username = data.get('username', '').strip()
    tiktok = data.get('tiktok', '').strip()
    if username and username.lower() not in seen:
        seen.add(username.lower())
        queue.append(username)
        if tiktok:
            tiktok_to_roblox[tiktok.lower()] = username
    return jsonify({'ok': True})

@app.route('/next', methods=['GET'])
def next_username():
    if queue:
        username = queue.popleft()
        seen.discard(username.lower())
        return jsonify({'username': username})
    return jsonify({'username': None})

@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify({'queue': list(queue)})

@app.route('/gift', methods=['POST'])
def add_gift():
    data = request.json
    tiktok_name = data.get('username', '')
    roblox_name = tiktok_to_roblox.get(tiktok_name.lower(), None)
    gift_queue.append({
        'username': tiktok_name,
        'roblox_username': roblox_name or '',
        'gift': data.get('gift', ''),
        'emoji': data.get('emoji', '🎁'),
        'tier': data.get('tier', 'rose')
    })
    return jsonify({'ok': True})

@app.route('/nextgift', methods=['GET'])
def next_gift():
    if gift_queue:
        return jsonify({'gift': gift_queue.popleft()})
    return jsonify({'gift': None})

@app.route('/skipqueue', methods=['POST'])
def skip_queue():
    data = request.json
    username = data.get('username', '').strip()
    if username and username.lower() not in seen:
        seen.add(username.lower())
        queue.appendleft(username)  # appendleft puts them at the FRONT
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)