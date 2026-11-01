import httpx
import fastapi
import uvicorn

app = fastapi.FastAPI()


async def get_roblox_avatar(user_id: int):
    async with httpx.AsyncClient(
        timeout=15.0,
        trust_env=False,
        headers={"User-Agent": "roblox-user-searcher"},
    ) as client:
        response = await client.get(
            "https://thumbnails.roblox.com/v1/users/avatar-headshot",
            params={
                "userIds": user_id,
                "size": "420x420",
                "format": "Png",
                "isCircular": "false"
            }
        )

        response.raise_for_status()
        data = response.json()

        return data["data"][0]["imageUrl"]


async def get_roblox_user(username: str):
    async with httpx.AsyncClient(
        timeout=15.0,
        trust_env=False,
        headers={"User-Agent": "roblox-user-searcher"},
    ) as client:
        response = await client.post(
            "https://users.roblox.com/v1/usernames/users",
            json={
                "usernames": [username],
                "excludeBannedUsers": False,
            },
        )

        response.raise_for_status()
        return response.json()


@app.get("/search/{username}")
async def search(username: str):
    return await get_roblox_user(username)


@app.get("/avatar/{user_id}")
async def avatar(user_id: int):
    return {
        "user_id": user_id,
        "avatar_url": await get_roblox_avatar(user_id)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
