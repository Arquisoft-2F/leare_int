from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import rpc
from spyne.model.primitive import Unicode, Integer, Double, String, DateTime
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
import json
from spyne import Iterable, Array
from spyne import ComplexModel
from django.forms.models import model_to_dict
from django.db import IntegrityError
from spyne.error import ResourceNotFoundError
from spyne.model.fault import Fault
from django.db.models.deletion import ProtectedError

class SoapService(ServiceBase):
	@rpc(Double(), Double(), _returns=Double)
	def suma(self, a, b):
		return a + b
	
soap_application = Application(
	[SoapService], 
	tns='testing.soap', 
	in_protocol=Soap11(validator='lxml'), 
	out_protocol=Soap11())

def consulta():
	django_application = DjangoApplication(soap_application)
	my_soap_app = csrf_exempt(django_application)
	return my_soap_app