import httpx
import fastapi
import uvicorn
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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


app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/search")
async def search(username: str = ""):
    username = username.strip()
    if not username:
        return RedirectResponse("/", status_code=303)
    return RedirectResponse(f"/user/{username}", status_code=303)


@app.get("/user/{username}", response_class=HTMLResponse)
async def get_user(request: Request, username: str):
    try:
        payload = await get_roblox_user(username)
    except httpx.HTTPError as exc:
        return templates.TemplateResponse(
            request,
            "user.html",
            {"account": None, "username": username, "error": str(exc)},
            status_code=502,
        )

    accounts = payload.get("data") or []
    return templates.TemplateResponse(
        request,
        "user.html",
        {"account": accounts[0] if accounts else None, "username": username, "error": None},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
