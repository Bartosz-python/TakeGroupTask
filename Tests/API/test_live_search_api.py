from playwright.sync_api import Playwright, APIRequestContext, APIResponse
import json

BASE_URL = "https://vod.film"
SEARCH_API_ENDPOINT = "/pl/search-route"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"

payload = {
    "host":"vod.film",
    "locale":"pl",
    "searchTerm":"the pickup"
    }

def test_live_search_api(playwright: Playwright):
    title: str = "the pickup"

    api_context: APIRequestContext = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers = {
            "User-Agent": USER_AGENT,
        })
    response: APIResponse = api_context.post(url = SEARCH_API_ENDPOINT, data = json.dumps(payload))
    assert response.status == 200

    responseBody = response.json()
    assert any(title.lower() in item.get("title", "").lower() for item in responseBody.get("data", []))

    api_context.dispose()