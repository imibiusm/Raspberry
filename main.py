
import httpx
import fastapi
import uvicorn
import uuid

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


async def search_game_by_name(game_name: str):
    session_id = str(uuid.uuid4())

    search_url = "https://apis.roblox.com/search-api/omni-search"

    params = {
        "searchQuery": game_name,
        "pageType": "all",
        "sessionId": session_id
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient(
        timeout=15.0,
        trust_env=False
    ) as client:

        # 1. Search for the experience
        search_resp = await client.get(
            search_url,
            params=params,
            headers=headers
        )

        search_resp.raise_for_status()
        search_data = search_resp.json()

        search_results = search_data.get("searchResults", [])
        universe_id = None

        # 2. Find the game universe ID
        for item in search_results:
            for content in item.get("contents", []):
                if content.get("contentType") == "Game":
                    universe_id = content.get("contentId")
                    break

            if universe_id:
                break

        if not universe_id:
            return None

        # 3. Get game information
        stats_url = "https://games.roblox.com/v1/games"

        stats_resp = await client.get(
            stats_url,
            params={"universeIds": universe_id},
            headers=headers
        )

        stats_resp.raise_for_status()
        stats_data = stats_resp.json()

        if not stats_data.get("data"):
            return None

        game_info = stats_data["data"][0]

        # 4. Get game votes
        votes_url = (
            f"https://games.roblox.com/v1/games/"
            f"{universe_id}/votes"
        )

        votes_resp = await client.get(
            votes_url,
            headers=headers
        )

        votes_resp.raise_for_status()
        votes_data = votes_resp.json()

        return {
            "universe_id": universe_id,
            "name": game_info.get("name"),
            "playing": game_info.get("playing"),
            "visits": game_info.get("visits"),
            "favorites": game_info.get("favoritedCount"),
            "upvotes": votes_data.get("upVotes"),
            "downvotes": votes_data.get("downVotes")
        }


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


@app.get("/get_game_info/{game_name}")
async def get_info(game_name: str):
    game = await search_game_by_name(game_name)

    if game is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail="Game not found"
        )

    return game


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
