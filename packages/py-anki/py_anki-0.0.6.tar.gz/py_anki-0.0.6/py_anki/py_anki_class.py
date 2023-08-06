  
#        /\          /\          /\          /\          /\          /\          /\          /\          /\          /\
#     /\//\\/\    /\//\\/\    /\//\\/\    /\//\\/\    /\//\\/\    /\//\\/\    /\//\\/\    /\//\\/\    /\//\\/\    /\//\\/\
#  /\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\
# //\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\
# \\//\/                                                                                                                \/\\//
#  \/                                              "In the Name of Allah"                                                  \/
#  /\                                                                                                                      /\
# //\\                                              Py-Anki Python Package                                                //\\
# \\//                                                                                                                    \\//
#  \/                                                                                                                      \/
#  /\          Package ID: 001                                                                                             /\
# //\\       Package Name: Py-Anki                                                                                        //\\
# \\//        Description: A simple API for Anki Spaced Repetition.                                                       \\//
#  \/                      The API is an unofficial python binding for AnkiConnect RESTful API.                            \/
#  /\                                                                                                                      /\
# //\\                                                                                                                    //\\
# \\//        Author Name: Abu Bakar Siddique Arman (#arman_bhaai)                                                        \\//
#  \/               Email: arman.bhaai@gmail.com                                                                           \/
#  /\              GitHub: github.com/arman-bhaai                                                                          /\
# //\\           Facebook: fb.me/arman.bhaai                                                                              //\\
# \\//            Youtube: tiny.cc/arman-bhaai-on-youtube                                                                 \\//
#  \/                      bit.ly/arman-bhaai-on-youtube                                                                   \/
#  /\                                                                                                                      /\
# //\\      Creation Date: 2021-04-24                                                                                     //\\
# \\//            Version: v0.0.1                                                                                         \\//
#  \/     Versioning Date: 2021-04-24                                                                                      \/
#  /\                                                                                                                      /\
# //\\            License: Custom License                                                                                 //\\
# \\//                                                                                                                    \\//
#  \/        Dev Language: Python 3.9.4                                                                                    \/
#  /\              Dev OS: Windows 10 (Home)                                                                               /\
# //\\                                                                                                                    //\\
# \\//        Source Code: www.github.com/arman-bhaai/py-anki                                                             \\//
#  \/         Package Url: #                                                                                               \/
#  /\                                                                                                                      /\
# //\\/\                                                                                                                /\//\\
# \\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\///\\/\//\\\//
#  \/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/\\///\\\//\/
#     \/\\//\/    \/\\//\/    \/\\//\/    \/\\//\/    \/\\//\/    \/\\//\/    \/\\//\/    \/\\//\/    \/\\//\/    \/\\//\/
#        \/          \/          \/          \/          \/          \/          \/          \/          \/          \/

import requests
import json


class AnkiApi:
	"""
	### Class (* -> required)
	AnkiApi(host:str, port:str)

		### Attributes (Public)
		host:str
		port:str

		### Methods (Public)
		create_model(*model_name:str, *in_order_model_fields:list, card_name:str, model_css:str, template_front:str, template_back:str) -> dict
		create_deck(*deck_name:str) -> dict
		fetch_picture(*url:str, *filename:str, fields:list) -> dict
		fetch_audio(*url:str, *filename:str, fields:list) -> dict
		create_note(*field_vals:list, deck_name:str, model_name:str, allow_duplicate:bool, tags:list, audios:list, making_note_list:bool) -> dict
		create_notes(*notes:list) -> dict
		exec(req_query:dict) -> json_obj

		### Methods (Private)
		_find_model_fields_by_name(*model_name:str) -> list
		_catch_error(*json_resp:json_obj)
	"""

	### Default Values
	default_in_order_model_fields = ['Front', 'Back']
	default_model_css = """
.card {
font-family: arial;
font-size: 20px;
text-align: center;
color: black;
background-color: white;
}
"""
	default_template_front = '{{Front}}'
	default_template_back = """
{{FrontSide}}

<hr id=answer>

{{Back}}
"""
	def __init__(self, host='http://localhost', port='8765'):
		self.host = host
		self.port = port
		self.model_fields = []

	def create_model(self, model_name, 
		in_order_model_fields=default_in_order_model_fields, 
		card_name='Card 1' ,
		model_css=default_model_css, 
		template_front=default_template_front, 
		template_back=default_template_back):

		model = {
			'modelName': model_name,
			'inOrderFields': in_order_model_fields,
			'css': model_css,
			'cardTemplates': [{
				'Name': card_name,
				'Front': template_front,
				'Back': template_back
			}]
		}

		req_query = {
			'action': 'createModel',
			'version': 6,
			'params': model
		}
		return req_query

	def _catch_error(self, json_resp):
		dict_resp = json.loads(json_resp)
		if dict_resp['error'] is not None:
			raise Exception(dict_resp['error'])
		elif dict_resp['result'] is None:
			raise Exception('Empty result')

	def _find_model_fields_by_name(self, model_name):
		req_query = {
			'action': 'modelFieldNames',
			'version': 6,
			'params': {
				'modelName':  model_name
			}
		}
		resp = self.exec(req_query)

		self.model_fields = json.loads(resp)['result']

		return self.model_fields

	def create_deck(self, deck_name):
		req_query = {
			'action': 'createDeck',
			'version': 6,
			'params': {
				'deck': deck_name
			}
		}
		return req_query
	
	def fetch_picture(self, url, filename, fields = ['Front']):
		picture = {
			'url': url,
			'filename': filename,
			'fields': fields
		}
		return picture

	def fetch_audio(self, url, filename, fields = ['Back']):
		audio = {
			'url': url,
			'filename': filename,
			'fields': fields
		}
		return audio

	def create_note(self, field_vals, deck_name='Default', model_name='Basic', allow_duplicate=False, 
		duplicate_scope='deck', tags=[], audios=[], pictures=[], making_note_list=False):

		# model_fields = self._find_model_fields_by_name(model_name)
		if not self.model_fields:
			self._find_model_fields_by_name(model_name)
		if not len(self.model_fields) == len(field_vals):
			raise Exception('Field length does not match')

		populated_fields = {k:v for k,v in zip(self.model_fields, field_vals)}
		note = {
			'deckName': deck_name,
			'modelName': model_name,
			'fields': populated_fields,
			'options': {
				'allowDuplicate': allow_duplicate,
				'duplicateScope': duplicate_scope
			},
			'tags': tags,
			'audio': audios,
			'picture': pictures
		}

		if making_note_list:
			return note

		req_query = {
			'action': 'addNote',
			'version': 6,
			'params': {
				'note': note
			}
		}
		return req_query

	def create_notes(self, notes):
		req_query = {
			'action': 'addNotes',
			'version': 6,
			'params': {
				'notes': notes
			}
		}
		return req_query

		
	def exec(self, req_query):
		try:
			resp = requests.post(self.host+':'+str(self.port), json.dumps(req_query)).text
		except:
			raise Exception('AnkiConnect Local Server not running')
		self._catch_error(resp)
		return resp