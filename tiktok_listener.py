import requests
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, GiftEvent

RENDER_URL = "https://tiktok-roblox-relay.onrender.com"
client = TikTokLiveClient(unique_id="runeless")

GIFT_TIERS = {
    "rose": {"tier": "rose", "emoji": "🌹"},
    "gift box": {"tier": "giftbox", "emoji": "🎁"},
    "lion": {"tier": "lion", "emoji": "🦁"},
    "universe": {"tier": "universe", "emoji": "🌋"},
}

def get_tier(gift_name):
    gift_lower = gift_name.lower()
    for key, value in GIFT_TIERS.items():
        if key in gift_lower:
            return value
    return {"tier": "rose", "emoji": "🎁"}

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
    if event.gift.streakable and not event.gift.streaked:
        return

    sender = event.user.nickname
    gift_name = event.gift.name
    tier_info = get_tier(gift_name)

    print(f"Gift: {tier_info['emoji']} {gift_name} from {sender}")

    try:
        requests.post(f"{RENDER_URL}/gift", json={
            "username": sender,
            "gift": gift_name,
            "emoji": tier_info["emoji"],
            "tier": tier_info["tier"]
        })

        if tier_info["tier"] == "rose":
            requests.post(f"{RENDER_URL}/skipqueue", json={"username": sender})

    except:
        print("Failed to send gift to relay")

if __name__ == "__main__":
    while True:
        try:
            print("Connecting to TikTok Live...")
            client.run()
        except Exception as e:
            print(f"Disconnected: {e}")
            print("Reconnecting in 5 seconds...")
            import time
            time.sleep(5)