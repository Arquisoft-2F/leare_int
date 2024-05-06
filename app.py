from spyne.server.wsgi import WsgiApplication
from time import ctime
from spyne import ServiceBase, rpc, Application, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from src.models.search_response import SearchModel

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from src.models.search_response import SearchModel


def get_posts(token: str, q: str) -> SearchModel:
	transport = RequestsHTTPTransport(
		'http://35.215.30.59:5555/graphql',
		headers={
			'Authorization': f'Bearer {token}'
			},
		use_json=True

	)

	client = Client(transport=transport, fetch_schema_from_transport=True)
	query = gql(f'''
		query Search {{
			getPosts(q: "{q}") {{
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

class AuthenticationHeader(ComplexModel):
    HTTP_AUTHORIZATION = Unicode

class LeareIntService(ServiceBase):
	__in_header__ = AuthenticationHeader

	@rpc(_returns=Unicode)
	def get_time(self):
		return ctime()

	@rpc(Integer, Integer, _returns=Integer)
	def add(self, a, b):
		return a + b
	
	@rpc(Unicode, _returns=Array(SearchModel))
	def search(self, q):
		headers = self.in_header
		print(headers)
		token = headers.HTTP_AUTHORIZATION
		print(token)
		return get_posts(token, q)

soap_app = Application([LeareIntService], 'leare_int',
					   in_protocol=Soap11(validator='lxml'),
					   out_protocol=Soap11())

# app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
# 	'/soap': wsgi_app
# })

if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	wsgi_app = WsgiApplication(soap_app)
	server = make_server('0.0.0.0', 5000, wsgi_app)
	print('Running on http://localhost:5000/soap')
	server.serve_forever()