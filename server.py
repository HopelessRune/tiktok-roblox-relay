from flask import Flask, jsonify, request
from collections import deque

app = Flask(__name__)

queue = deque()  # now stores dicts instead of strings
seen = set()
gift_queue = deque()
tiktok_to_roblox = {}

@app.route('/add', methods=['POST'])
def add_username():
    data = request.json
    username = data.get('username', '').strip()
    tiktok = data.get('tiktok', '').strip()
    if username and username.lower() not in seen:
        seen.add(username.lower())
        queue.append({'username': username, 'tiktok': tiktok})
        if tiktok:
            tiktok_to_roblox[tiktok.lower()] = username
    return jsonify({'ok': True})

@app.route('/next', methods=['GET'])
def next_username():
    if queue:
        entry = queue.popleft()
        seen.discard(entry['username'].lower())
        return jsonify({'username': entry['username'], 'tiktok': entry.get('tiktok', '')})
    return jsonify({'username': None, 'tiktok': None})

@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify({'queue': [entry['username'] for entry in queue]})

@app.route('/gift', methods=['POST'])
def add_gift():
    data = request.json
    tiktok_name = data.get('username', '')
    roblox_name = tiktok_to_roblox.get(tiktok_name.lower(), None)
    tier = data.get('tier', 'rose')
    
    gift_queue.append({
        'username': tiktok_name,
        'roblox_username': roblox_name or '',
        'gift': data.get('gift', ''),
        'emoji': data.get('emoji', '🎁'),
        'tier': tier
    })
    
    # Handle rose skip using roblox name not tiktok name
    if tier == 'rose' and roblox_name:
        if roblox_name.lower() not in seen:
            seen.add(roblox_name.lower())
        queue.appendleft(roblox_name)
    
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
    tiktok = data.get('tiktok', '').strip()
    if username and username.lower() not in seen:
        seen.add(username.lower())
        queue.appendleft({'username': username, 'tiktok': tiktok})
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)