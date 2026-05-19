import requests

RENDER_URL = "https://tiktok-roblox-relay.onrender.com"

print("Test Queue - Type a Roblox username and press Enter to add to queue")
print("Type 'clear' to reset, 'quit' to exit")
print("---")

while True:
    username = input("Username: ").strip()
    if username.lower() == "quit":
        break
    elif username.lower() == "clear":
        print("Queue cleared (restart server.py on Render to fully reset)")
    elif username:
        try:
            r = requests.post(f"{RENDER_URL}/add", json={"username": username})
            print(f"✓ Added '{username}' to queue")
        except:
            print("✗ Failed - is Render running?")