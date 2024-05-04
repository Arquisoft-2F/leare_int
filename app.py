from flask import request
from spyne.server.wsgi import WsgiApplication
from time import ctime
from spyne import ServiceBase, rpc, Application, Integer, Unicode, Array
from spyne.protocol.soap import Soap11
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from src.services import get_posts
from src.models.search_response import SearchModel

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from src.models.search_response import SearchModel

transport = RequestsHTTPTransport(
	'http://35.215.30.59:5555/graphql',
	headers={
		'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiJmMmIwNGExOC03MzNhLTRhZmMtYTYyNy0zZGQ4ZjRjY2FkY2EiLCJVc2VybmFtZSI6Imp1YW5wZXJleiIsIlJvbGUiOiJhZG1pbiIsImV4cCI6MTcxNDkzNzc4OSwiaXNzIjoiaHR0cHM6Ly9sb2NhbGhvc3Q6NzIwMiIsImF1ZCI6Imh0dHBzOi8vbG9jYWxob3N0OjcyMDIifQ.iJwxstoeHY3rDyi-wumNtG_tuc24QC7b4cL4FuhkJY0'
		},
	use_json=True

)

client = Client(transport=transport, fetch_schema_from_transport=True)

def get_posts(q: str) -> SearchModel:
	query = gql(f'''
		query Search {{
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


app = Flask(__name__)

class TestService(ServiceBase):

	@rpc(_returns=Unicode)
	def get_time(self):
		return ctime()

	@rpc(Integer, Integer, _returns=Integer)
	def add(self, a, b):
		return a + b
	
	@rpc(Unicode, _returns=Array(SearchModel))
	def search(self, q):
		return get_posts(q)

soap_app = Application([TestService], 'test_service',
					   in_protocol=Soap11(validator='lxml'),
					   out_protocol=Soap11())
wsgi_app = WsgiApplication(soap_app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
	'/soap': wsgi_app
})

if __name__ == '__main__':
	print('Running on http://localhost:5000/soap')
	app.debug = True
	app.run()