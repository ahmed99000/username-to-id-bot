
import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pyrogram import Client
import uvicorn

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = FastAPI()
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Telegram Username to ID</title></head>
<body>
<h2>Telegram Username থেকে User ID বের করুন</h2>
<form method="post">
  <input name="username" placeholder="@username" required>
  <button type="submit">Get ID</button>
</form>
<p>{result}</p>
</body>
</html>
"""

@app.on_event("startup")
async def startup():
    await bot.start()

@app.on_event("shutdown")
async def shutdown():
    await bot.stop()

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML.format(result="")

@app.post("/", response_class=HTMLResponse)
async def get_id(username: str = Form(...)):
    try:
        user = await bot.get_users(username)
        return HTML.format(result=f"User: @{user.username}, ID: {user.id}")
    except Exception as e:
        return HTML.format(result=f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
