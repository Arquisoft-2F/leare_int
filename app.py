from flask import request
from spyne.server.wsgi import WsgiApplication
from time import ctime
from spyne import ServiceBase, rpc, Application, Integer, Unicode, Array
from spyne.protocol.soap import Soap11
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from src.services import get_posts
from src.models.search_response import SearchResponse

app = Flask(__name__)

class TestService(ServiceBase):

	@rpc(_returns=Unicode)
	def get_time(self):
		return ctime()

	@rpc(Integer, Integer, _returns=Integer)
	def add(self, a, b):
		return a + b
	
	@rpc(Unicode, _returns=Array(SearchResponse))
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
	app.run()