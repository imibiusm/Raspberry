
import httpx
import fastapi
import uvicorn

app = fastapi.FastAPI()

HEADERS = {"User-Agent": "roblox-user-searcher"}



async def get_roblox_user(username: str):
    async with httpx.AsyncClient(
        timeout=15.0,
        trust_env=False,
        headers=HEADERS
    ) as client:
        response = await client.post(
            "https://users.roblox.com/v1/usernames/users",
            json={
                "usernames": [username],
                "excludeBannedUsers": False
            }
        )

        response.raise_for_status()
        data = response.json()

        if not data.get("data"):
            return None

        return data["data"][0]



async def get_roblox_avatar(user_id: int):
    async with httpx.AsyncClient(
        timeout=15.0,
        trust_env=False,
        headers=HEADERS
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

        if not data.get("data"):
            return None

        return data["data"][0]["imageUrl"]



async def get_roblox_user_description(user_id: int):
    async with httpx.AsyncClient(
        timeout=15.0,
        trust_env=False,
        headers=HEADERS
    ) as client:
        response = await client.get(
            f"https://users.roblox.com/v1/users/{user_id}"
        )

        response.raise_for_status()
        data = response.json()

        return data["description"]



@app.get("/search/{username}")
async def search(username: str):
    user = await get_roblox_user(username)

    if user is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail="Roblox user not found"
        )

    return user


@app.get("/avatar/{username}")
async def avatar(username: str):
    user = await get_roblox_user(username)

    if user is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail="Roblox user not found"
        )

    avatar_url = await get_roblox_avatar(user["id"])

    return {
        "username": user["name"],
        "user_id": user["id"],
        "avatar_url": avatar_url
    }


@app.get("/description/{username}")
async def description(username: str):
    user = await get_roblox_user(username)

    if user is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail="Roblox user not found"
        )

    description = await get_roblox_user_description(user["id"])

    return {
        "username": user["name"],
        "user_id": user["id"],
        "description": description
    }


@app.get("/user/{username}")
async def full_profile(username: str):
    user = await get_roblox_user(username)

    if user is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail="Roblox user not found"
        )

    user_id = user["id"]

    avatar_url = await get_roblox_avatar(user_id)
    description = await get_roblox_user_description(user_id)

    return {
        "id": user_id,
        "username": user["name"],
        "display_name": user["displayName"],
        "avatar_url": avatar_url,
        "description": description
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
