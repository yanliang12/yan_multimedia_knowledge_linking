#######server_path.py#######
import re
import time
import logging
import argsparser
from flask import *
from flask_restplus import *

from jessica_knowledge_linking import *

ns = Namespace('JessKnowLik', description='Jessica\'s Text to Knowledge Graph Engine. I am open for a DS/AI job, contact me by gaoyuanliang@outlook.com')
args = argsparser.prepare_args()

parser = ns.parser()
parser.add_argument('text', type=str, location='json')
parser.add_argument('document_path', type=list, location='json')


#######Text2DBPedia_KnowledgeGraph
req_fields = {\
	'text': fields.String(\
	example = u"Sheikh Mohammed bin Rashid Al Maktoum is the 70-year-old billionaire ruler of Dubai and vice-president of the United Arab Emirates.")\
	}
jessica_api_req = ns.model('JessKnowLik', req_fields)

rsp_fields = {\
	'status':fields.String,\
	'running_time':fields.Float\
	}
jessica_api_rsp = ns.model('JessKnowLik', rsp_fields)

@ns.route('/text')
class jessica_api(Resource):
	def __init__(self, *args, **kwargs):
		super(jessica_api, self).__init__(*args, **kwargs)
	@ns.marshal_with(jessica_api_rsp)
	@ns.expect(jessica_api_req)
	def post(self):		
		start = time.time()
		output = {}
		try:			
			args = parser.parse_args()	
			triplets = text_to_knowledge_graph(args['text'])
			output['status'] = "success"
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = 'error:'+str(e)
			output['running_time'] = float(time.time()- start)
			return output

###########Cocktail2DBPedia_KnowledgeGraph
req_fields1 = {\
	'document_path': 
	fields.List(fields.String())\
	}
jessica_api_req_cocktail = ns.model('JessCKnowG', req_fields1)

rsp_fields1 = {\
	'status':fields.String,\
	'running_time':fields.Float\
	}
jessica_api_rsp_cocktail = ns.model('JessCKnowG', rsp_fields1)

@ns.route('/multimedia')
class jessica_api_cocktail(Resource):
	def __init__(self, *args, **kwargs):
		super(jessica_api_cocktail, self).__init__(*args, **kwargs)
	@ns.marshal_with(jessica_api_rsp_cocktail)
	@ns.expect(jessica_api_req_cocktail)
	def post(self):		
		start = time.time()
		output = {}
		try:			
			args = parser.parse_args()
			triplets = documents_to_knowledge_graph(args['document_path'])
			######
			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output['status'] = 'error:'+str(e)
			output['running_time'] = float(time.time()- start)
			return output
#######server_path.py#######
