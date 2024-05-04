from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from src.models.search_response import SearchResponse

transport = RequestsHTTPTransport('https://35.215.30.59/graphql', headers={'Authorization': 'Bearer YOUR_GITHUB_TOKEN'}, use_json=True)

client = Client(transport=transport, fetch_schema_from_transport=True)

def get_posts(q: str) -> SearchResponse:
	query = gql(f'''
		query Search($q: String!) {{
			getPosts(q: {q}) {{
				highlight {{
					name
					lastname
					nickname
					description
				}}
				post {{
					name
					lastname
					nickname
					picture
					id
					description
					type
				}}
			}}
		}}
	''')
	return client.execute(query)['getPosts']