import requests
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, GiftEvent
import time

RENDER_URL = "https://tiktok-roblox-relay.onrender.com"
client = TikTokLiveClient(unique_id="runeless")

# Special tiers for big gifts that trigger camera events
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
    # Everything else still shows a notification but no special camera event
    return {"tier": "gift", "emoji": "🎁"}

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

if __name__ == "__main__":
    while True:
        try:
            print("Connecting to TikTok Live...")
            client.run()
        except KeyboardInterrupt:
            # Ctrl+C pressed, exit cleanly
            print("Stopped.")
            break
        except Exception as e:
            print(f"Disconnected: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)