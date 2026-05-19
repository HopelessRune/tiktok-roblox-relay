import requests
import threading
import time
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, GiftEvent

RENDER_URL = "https://tiktok-roblox-relay.onrender.com"
client = TikTokLiveClient(unique_id="runeless")

SPECIAL_TIERS = {
    "lion": {"tier": "lion", "emoji": "🦁"},
    "universe": {"tier": "universe", "emoji": "🌋"},
    "gift box": {"tier": "giftbox", "emoji": "🎁"},
    "rose": {"tier": "rose", "emoji": "🌹"},
}

def get_tier(gift_name):
    gift_lower = gift_name.lower()
    for key, value in SPECIAL_TIERS.items():
        if key in gift_lower:
            return value
    return {"tier": "gift", "emoji": "🎁"}

def keep_alive():
    while True:
        try:
            requests.get(f"{RENDER_URL}/queue")
            print("Pinged server to keep alive")
        except:
            pass
        time.sleep(600)

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    msg = event.comment.strip()
    if msg.startswith("!"):
        roblox_username = msg[1:].strip()
        tiktok_nickname = event.user.nickname
        if roblox_username:
            try:
                requests.post(f"{RENDER_URL}/add", json={
                    "username": roblox_username,
                    "tiktok": tiktok_nickname
                })
                print(f"Added: {roblox_username} (TikTok: {tiktok_nickname})")
            except:
                print("Failed to send to relay")

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    try:
        sender = event.user.nickname
        gift_name = event.gift.name
        tier_info = get_tier(gift_name)

        print(f"Gift: {tier_info['emoji']} {gift_name} from {sender}")

        requests.post(f"{RENDER_URL}/gift", json={
            "username": sender,
            "gift": gift_name,
            "emoji": tier_info["emoji"],
            "tier": tier_info["tier"]
        })

    except Exception as e:
        print(f"Gift error: {e}")

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    while True:
        try:
            print("Connecting to TikTok Live...")
            client.run()
        except KeyboardInterrupt:
            print("Stopped.")
            break
        except Exception as e:
            print(f"Disconnected: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)