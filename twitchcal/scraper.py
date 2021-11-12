from requests import Session, HTTPError
from typing import Dict, Any

JSONObject = Dict[str, Any]

session = Session()
session.headers = {"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"}

class ExtractorException(Exception):
    pass

def normalize(string: str) -> str:
	return string.lower().strip()

def gql_request(query: str, variables: JSONObject = {}) -> JSONObject:
	url = "https://gql.twitch.tv/gql"
	body = {
		"query": query,
		"variables": variables
	}

	res = session.post(
		url,
		json=body,
		headers={"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"}
	)

	try:
		res.raise_for_status()
	except HTTPError as e:
		raise ExtractorException(e)

	body: Dict[str, Any] = res.json()

	if body.get("errors"):
		raise ExtractorException(f"GQL error: {body.get('errors')}")

	return res.json()["data"]

def get_schedule(channel_name: str) -> JSONObject:
	query = '''
	query Schedule($login: String!) {
		user(login: $login) {
			displayName
			profileURL
			channel {
				schedule {
					segments(includeFutureSegments: true) {
						title
						id
						startAt
						endAt
						isCancelled
						categories {
							displayName
						}
					}
				}
			}
		}
	}
	'''

	data = gql_request(query, variables={"login": channel_name})

	if not data["user"] or not data["user"]["channel"]["schedule"]:
		return None
	
	return data
