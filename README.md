# RoSearch

RoSearch is a lightweight REST API built with **FastAPI** that retrieves Roblox user and experience (game) information using Roblox's public web APIs.

It provides endpoints to look up Roblox users, retrieve avatar and profile descriptions, return a combined user profile, and search for game statistics.

## Features

### Roblox user lookup
- Find a Roblox account by username.
- Retrieve the user's Roblox ID and account name.

### Avatar lookup
- Retrieve a user's avatar headshot image URL.
- Returns the username and Roblox user ID alongside the image URL.

### User description
- Retrieve the description (About section) from a Roblox user profile.

### Full user profile
- Combine basic account information, display name, avatar URL, and profile description in one response.

### Game information
- Search for a Roblox experience by name.
- Retrieve its universe ID, current player count, visit count, favorite count, and upvote/downvote totals.

## Tech stack

- **Python** — application language
- **FastAPI** — HTTP API framework
- **Uvicorn** — ASGI server
- **HTTPX** — asynchronous HTTP client
- **Roblox web APIs** — source of user, avatar, and game data

## Requirements

- Python 3.9 or newer
- pip

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/imibiusm/RoSearch.git
   cd RoSearch
   ```

2. (Recommended) Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the API

Start the application:

```bash
python main.py
```

The server listens on:

```
http://localhost:8000
```

The application is configured to listen on `0.0.0.0:8000`, so it can also be reached from other devices on the host's network when firewall and network settings permit.

## API documentation

With the server running, FastAPI automatically provides interactive API documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints

All endpoints use the HTTP **GET** method and return JSON.

| Endpoint | Description |
|---|---|
| `/search/{username}` | Look up a Roblox user by username |
| `/avatar/{username}` | Get a user's avatar headshot URL |
| `/description/{username}` | Get a user's profile description |
| `/user/{username}` | Get a combined user profile |
| `/get_game_info/{game_name}` | Search for a Roblox game and retrieve its statistics |

### 1. Search for a user

**Request:**

```http
GET /search/builderman
```

Returns the user object supplied by Roblox's username lookup API, including fields such as the account ID, username, and display name.

### 2. Get a user's avatar

**Request:**

```http
GET /avatar/builderman
```

**Response shape:**

```json
{
  "username": "builderman",
  "user_id": 156,
  "avatar_url": "https://..."
}
```

The values above illustrate the response format; the avatar URL is supplied by Roblox.

### 3. Get a user's description

**Request:**

```http
GET /description/builderman
```

**Response shape:**

```json
{
  "username": "builderman",
  "user_id": 156,
  "description": "The user's profile description"
}
```

### 4. Get a full user profile

**Request:**

```http
GET /user/builderman
```

**Response shape:**

```json
{
  "id": 156,
  "username": "builderman",
  "display_name": "Builderman",
  "avatar_url": "https://...",
  "description": "The user's profile description"
}
```

### 5. Get game information

**Request:**

```http
GET /get_game_info/adopt%20me
```

URL-encode spaces and other special characters in the game name when making a request.

**Response shape:**

```json
{
  "universe_id": 123456,
  "name": "Example Experience",
  "playing": 1234,
  "visits": 987654,
  "favorites": 45678,
  "upvotes": 10000,
  "downvotes": 500
}
```

The numbers and game name above are illustrative. Actual values depend on Roblox's API response.

## Error handling

If a Roblox username or game cannot be found, the corresponding endpoint returns **HTTP 404** with a JSON error detail.

Example:

```json
{
  "detail": "Roblox user not found"
}
```

The game endpoint uses the detail message `Game not found`.

Requests to Roblox use a 15-second HTTP timeout. HTTP errors from upstream Roblox endpoints are raised by HTTPX and are not currently converted into custom RoSearch error responses.

## Project structure

```text
RoSearch/
├── main.py
├── requirements.txt
└── README.md
```

- `main.py` — FastAPI application, Roblox API requests, and route definitions.
- `requirements.txt` — Python package dependencies.
- `README.md` — project documentation.

## How it works

1. A client sends a GET request to one of the RoSearch endpoints.
2. RoSearch makes an asynchronous HTTP request to the relevant Roblox API.
3. The application extracts the requested user, avatar, description, or game data.
4. FastAPI returns the result as JSON.

## Notes and limitations

- RoSearch depends on Roblox's web APIs. Changes, outages, rate limits, or availability restrictions on those APIs may affect results.
- Search results for games depend on Roblox's search API and the first matching game result returned by that search.
- The project currently has no database or persistent storage; data is fetched when an endpoint is called.
- No authentication layer is configured in the current application. If you deploy it publicly, consider adding access controls, request throttling, and appropriate monitoring.
- Roblox is a third-party service. RoSearch is an independent project and is not an official Roblox product.

## Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the API locally.
5. Open a pull request describing your changes.

## License

No license file is currently present in the repository. Unless a license is added, the project should not be assumed to grant permissions for reuse, modification, or redistribution.

---

**Repository:** [imibiusm/RoSearch](https://github.com/imibiusm/RoSearch)
