# leetcode_service.py
import httpx
from typing import Optional, Dict, Any

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

async def get_problem_details(title_slug: str) -> Optional[Dict[str, Any]]:
    """
    Fetches problem details from LeetCode's GraphQL API.
    """
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            title
            difficulty
            stats
        }
    }
    """
    variables = {"titleSlug": title_slug}
    payload = {"query": query, "variables": variables}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LEETCODE_GRAPHQL_URL, json=payload)
            response.raise_for_status() # Raises an exception for 4XX/5XX responses
            
            data = response.json()
            question_data = data.get("data", {}).get("question")

            if not question_data:
                return None

            # The acceptance rate is in the 'stats' JSON string
            import json
            stats = json.loads(question_data.get("stats", "{}"))
            acceptance_rate = (stats.get("totalAcceptedRaw", 0) / stats.get("totalSubmissionRaw", 1)) * 100

            return {
                "title_slug": title_slug,
                "title": question_data.get("title"),
                "difficulty": question_data.get("difficulty"),
                "acceptance_rate": round(acceptance_rate, 2),
            }
        except (httpx.RequestError, json.JSONDecodeError) as e:
            print(f"Error fetching LeetCode data for {title_slug}: {e}")
            return None