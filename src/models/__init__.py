from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from src.models.search_response import SearchModel

transport = RequestsHTTPTransport(
	'https://35.215.30.59/graphiql',
	headers={
		'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiJmMmIwNGExOC03MzNhLTRhZmMtYTYyNy0zZGQ4ZjRjY2FkY2EiLCJVc2VybmFtZSI6Imp1YW5wZXJleiIsIlJvbGUiOiJhZG1pbiIsImV4cCI6MTcxNDkzNzc4OSwiaXNzIjoiaHR0cHM6Ly9sb2NhbGhvc3Q6NzIwMiIsImF1ZCI6Imh0dHBzOi8vbG9jYWxob3N0OjcyMDIifQ.iJwxstoeHY3rDyi-wumNtG_tuc24QC7b4cL4FuhkJY0'
		},
	use_json=True
)

client = Client(transport=transport, fetch_schema_from_transport=True)

def get_posts(q: str) -> SearchModel:
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