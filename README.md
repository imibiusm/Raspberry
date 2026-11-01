# RoSearch API

A simple REST API for retrieving **Roblox user and experience data**. Use RoSearch from any programming language that can make HTTP requests—no Roblox cookies, API keys, or SDK required.

**Base URL**

```text
https://rosearch.onrender.com
```

All endpoints use `GET` and return JSON.

## Table of contents

- [Endpoints](#endpoints)
- [Response examples](#response-examples)
- [Usage](#usage)
  - [Node.js](#nodejs)
  - [Python](#python)
  - [Go](#go)
  - [.NET-c)
- [Errors](#errors)
- [Notes](#notes)

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/search/{username}` | Look up a Roblox account by username. Returns the matching user data from Roblox's username lookup API. |
| `GET` | `/avatar/{username}` | Get the account username, user ID, and avatar headshot image URL. |
| `GET` | `/description/{username}` | Get the account username, user ID, and profile description (About section). |
| `GET` | `/user/{username}` | Get a combined profile containing the user ID, username, display name, avatar URL, and description. |
| `GET` | `/get_game_info/{game_name}` | Search Roblox experiences by name and return information and vote counts for the first matching game result. |

Replace each path parameter with the value you want to look up.

### 1. Search for a Roblox user

```http
GET https://rosearch.onrender.com/search/{username}
```

Looks up a Roblox username. The response is the user record returned by Roblox's username lookup API.

Example:

```text
https://rosearch.onrender.com/search/builderman
```

### 2. Get a user's avatar

```http
GET https://rosearch.onrender.com/avatar/{username}
```

Returns:

| Field | Description |
|---|---|
| `username` | Roblox account username |
| `user_id` | Roblox user ID |
| `avatar_url` | URL of the user's avatar headshot image |

### 3. Get a user's description

```http
GET https://rosearch.onrender.com/description/{username}
```

Returns:

| Field | Description |
|---|---|
| `username` | Roblox account username |
| `user_id` | Roblox user ID |
| `description` | Text from the user's Roblox profile description |

### 4. Get a full user profile

```http
GET https://rosearch.onrender.com/user/{username}
```

Returns:

| Field | Description |
|---|---|
| `id` | Roblox user ID |
| `username` | Roblox account username |
| `display_name` | Roblox display name |
| `avatar_url` | URL of the user's avatar headshot |
| `description` | Profile description |

### 5. Get Roblox game information

```http
GET https://rosearch.onrender.com/get_game_info/{game_name}
```

Searches Roblox experiences using the supplied name and returns data for the first matching game result.

| Field | Description |
|---|---|
| `universe_id` | Roblox experience universe ID |
| `name` | Experience name |
| `playing` | Current number of players reported by Roblox |
| `visits` | Total visits reported by Roblox |
| `favorites` | Favorite count |
| `upvotes` | Upvote count |
| `downvotes` | Downvote count |

**Important:** URL-encode game names when they contain spaces or reserved URL characters. For example, `Adopt Me!` becomes `Adopt%20Me%21`. The client examples below encode path parameters for you.

## Response examples

These examples show the response shape. IDs, names, URLs, descriptions, and statistics depend on the Roblox data returned at request time.

**Avatar response**

```json
{
  "username": "builderman",
  "user_id": 156,
  "avatar_url": "https://tr.rbxcdn.com/..."
}
```

**Full profile response**

```json
{
  "id": 156,
  "username": "builderman",
  "display_name": "Builderman",
  "avatar_url": "https://tr.rbxcdn.com/...",
  "description": "Example profile description"
}
```

**Game response**

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

## Usage

Every example below calls the same public API. No API key or authentication header is required by the current service.

### Node.js

Node.js 18+ includes the Fetch API, so no additional package is needed.

```javascript
const BASE_URL = "https://rosearch.onrender.com";

async function getRobloxUser(username) {
  const url = `${BASE_URL}/user/${encodeURIComponent(username)}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`RoSearch error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

async function getGameInfo(gameName) {
  const url = `${BASE_URL}/get_game_info/${encodeURIComponent(gameName)}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`RoSearch error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

(async () => {
  try {
    const user = await getRobloxUser("builderman");
    console.log("User:", user);

    const game = await getGameInfo("Adopt Me!");
    console.log("Game:", game);
  } catch (error) {
    console.error(error.message);
  }
})();
```

### Python

This example uses the popular `requests` package.

Install it:

```bash
python -m pip install requests
```

Example:

```python
import requests

BASE_URL = "https://rosearch.onrender.com"

def get_roblox_user(username: str):
    response = requests.get(
        f"{BASE_URL}/user/{requests.utils.quote(username, safe='')}",
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

def get_game_info(game_name: str):
    response = requests.get(
        f"{BASE_URL}/get_game_info/{requests.utils.quote(game_name, safe='')}",
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        user = get_roblox_user("builderman")
        print("User:", user)

        game = get_game_info("Adopt Me!")
        print("Game:", game)
    except requests.RequestException as error:
        print("RoSearch request failed:", error)
```

### Go

This example uses Go's standard library; no third-party dependencies are required.

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"time"
)

const baseURL = "https://rosearch.onrender.com"

func getJSON(endpoint string) (map[string]any, error) {
	client := &http.Client{Timeout: 30 * time.Second}

	resp, err := client.Get(baseURL + endpoint)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("RoSearch returned %s: %s", resp.Status, string(body))
	}

	var result map[string]any
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return result, nil
}

func main() {
	username := url.PathEscape("builderman")
	user, err := getJSON("/user/" + username)
	if err != nil {
		fmt.Println("User request failed:", err)
		return
	}
	fmt.Printf("User: %+v\n", user)

	gameName := url.PathEscape("Adopt Me!")
	game, err := getJSON("/get_game_info/" + gameName)
	if err != nil {
		fmt.Println("Game request failed:", err)
		return
	}
	fmt.Printf("Game: %+v\n", game)
}
```

### .NET (C#)

This example uses `HttpClient` and `System.Text.Json`. It works with modern .NET versions that support top-level statements.

```csharp
using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

const string baseUrl = "https://rosearch.onrender.com";

using var http = new HttpClient
{
    Timeout = TimeSpan.FromSeconds(30)
};

static async Task<JsonDocument> GetJsonAsync(HttpClient http, string url)
{
    using var response = await http.GetAsync(url);
    response.EnsureSuccessStatusCode();

    var json = await response.Content.ReadAsStringAsync();
    return JsonDocument.Parse(json);
}

try
{
    var username = Uri.EscapeDataString("builderman");
    using var user = await GetJsonAsync(
        http,
        $"{baseUrl}/user/{username}"
    );

    Console.WriteLine("User:");
    Console.WriteLine(JsonSerializer.Serialize(
        user.RootElement,
        new JsonSerializerOptions { WriteIndented = true }
    ));

    var gameName = Uri.EscapeDataString("Adopt Me!");
    using var game = await GetJsonAsync(
        http,
        $"{baseUrl}/get_game_info/{gameName}"
    );

    Console.WriteLine("Game:");
    Console.WriteLine(JsonSerializer.Serialize(
        game.RootElement,
        new JsonSerializerOptions { WriteIndented = true }
    ));
}
catch (HttpRequestException error)
{
    Console.WriteLine($"RoSearch request failed: {error.Message}");
}
catch (TaskCanceledException)
{
    Console.WriteLine("The RoSearch request timed out.");
}
```

## Errors

RoSearch returns JSON error details for records it cannot find.

| HTTP status | Meaning |
|---|---|
| `404 Not Found` | Roblox user or game could not be found |
| Other non-2xx status | The request or an upstream Roblox API call failed |

Example 404 response for a missing user:

```json
{
  "detail": "Roblox user not found"
}
```

Example 404 response for a missing game:

```json
{
  "detail": "Game not found"
}
```

In your application, check the HTTP status before trying to use the JSON response as a successful result. The code samples above demonstrate this.

## Notes

- **No API key currently required:** the deployed API can be called directly from your application.
- **Upstream dependency:** user and game data comes from Roblox web APIs. Roblox outages, rate limits, API changes, or restrictions can affect responses.
- **Game search matching:** the game endpoint uses Roblox search and returns the first matching game result; it is not an exact-match guarantee.
- **Deployment cold starts:** if the hosted service is idle or starting up, the first request may take longer than subsequent requests.
- **Timeouts:** set a reasonable client timeout. The examples use 30 seconds to allow for upstream requests and hosting startup.
- **Independent project:** RoSearch is not an official Roblox service and is not affiliated with or endorsed by Roblox.

## Links

- **Live API:** [https://rosearch.onrender.com](https://rosearch.onrender.com)
- **Interactive API docs (Swagger):** [https://rosearch.onrender.com/docs](https://rosearch.onrender.com/docs)
- **Alternative API docs (ReDoc):** [https://rosearch.onrender.com/redoc](https://rosearch.onrender.com/redoc)
- **GitHub repository:** [imibiusm/RoSearch](https://github.com/imibiusm/RoSearch)
- **Discord Support:** [Discord](https://discord.gg/DVwPNPhsm7)

---

Made for developers building with Roblox data.

