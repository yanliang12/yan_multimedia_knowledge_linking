#######jessica_knowledge_linking.py#######
import re 
import numpy 
import itertools

from yan_neo4j import start_neo4j
from yan_neo4j import create_neo4j_session
from yan_neo4j import ingest_knowledge_triplets_to_neo4j

start_neo4j(http_port = "4643", bolt_port = "6781")
neo4j_session = create_neo4j_session(bolt_port = "6781")

from yan_ocr import extract_text
from yan_tts import speech_to_text
from yan_sentence_segmentation import text_to_sentences

from jessica_dbpedia_query import *
from jessica_entity_linking import *

def entity_to_knowledge_triplets(entities,
	related_subject_num = 2,
	related_object_num = 2,
	common_object_number = 2,
	common_subject_number = 2,
	connected_entity_linkage_number = 1):
	triplets = []
	#####
	entity_ids = list(set([e['entity_dbpedia_id'] for e in entities]))
	for e in entity_ids:
		triplets += find_related_entities(e,
		related_subject_num = related_subject_num,
		related_object_num = related_object_num)
	####
	for r1, r2 in itertools.combinations(entity_ids,2):
		triplets += find_linking_entities(
			r1, r2, 
			common_object_number = common_object_number,
			common_subject_number = common_subject_number)
		triplets += find_entity_pair_relation(
			r1, r2, 
			relation_1_to_2_number = connected_entity_linkage_number,
			relation_2_to_1_number = connected_entity_linkage_number)
	#####
	triplets, entity_type_lookup, entity_name_lookup, relation_name_lookup = attach_triplet_type_and_name(triplets)
	for e in entities:
		if 'sentence' in e:
			try:				
				triplets.append({'subject':str(hash(e['sentence'])),
					'subject_type':'Sentence',
					'subject_name': re.sub(r'\'',  r'\'', e['sentence']),
					'relation':'mention',
					'object': e['entity_dbpedia_id'],
					'object_type': entity_type_lookup[e['entity_dbpedia_id']],
					'object_name': entity_name_lookup[e['entity_dbpedia_id']],
					})
			except:
				triplets.append({'subject':str(hash(e['sentence'])),
					'subject_type':'Sentence',
					'subject_name': re.sub(r'\'',  r'\'', e['sentence']),
					'relation':'mention',
					'object': e['entity_dbpedia_id'],
					'object_type': 'Other',
					'object_name': id_to_name(e['entity_dbpedia_id']),
					})
			if 'document' in e:
				triplets.append({'subject':str(hash(e['document'])),
					'subject_type':'Document',
					'subject_name': re.sub(r'\'',  r'\'', e['document']),
					'relation':'contain',
					'object': str(hash(e['sentence'])),
					'object_type': 'Sentence',
					'object_name': re.sub(r'\'',  r'\'', e['sentence']),
					})
	return triplets

'''
from yan_entity_linking import entity_linking
from jessica_neo4j import ingest_knowledge_triplets_to_neo4j

text = u"I am from Shanghai of China."

entities = entity_linking(text)

for e in entities:
	e['document'] = 'text.txt'

ingest_knowledge_triplets_to_neo4j(
	entity_to_knowledge_triplets(entities,
	related_subject_num = 1,
	related_object_num = 1,
	common_object_number = 1,
	common_subject_number = 1))
'''

def text_to_knowledge_graph(text):
	sentences = text_to_sentences(text)
	entities = []
	for s in sentences:
		entities += entity_linking(s)
	entities_with_id = []
	for e in entities:
		e['entity_dbpedia_id'] = wikipage_id_to_dbpedia_id(e['entity_wikipage_id'])
		if e['entity_dbpedia_id'] is not None:
			entities_with_id.append(e)
	triplets = entity_to_knowledge_triplets(entities_with_id,
		related_subject_num = 2,
		related_object_num = 2,
		common_object_number = 3,
		common_subject_number = 3,
		connected_entity_linkage_number = 2)
	ingest_knowledge_triplets_to_neo4j(triplets, neo4j_session)
	return triplets

'''
text = "i am from china. I moved from Shanghai to Abu Dhabi on 2020.  Welcome to Dubai."
text_to_knowledge_graph(text)
'''

def documents_to_knowledge_graph(document_paths):
	entities = []
	for document_path in document_paths:
		text = None
		if bool(re.search(r'\.(wav|mp3)$', document_path.lower())):
			text = speech_to_text(document_path)
		if bool(re.search(r'\.(jpg|png|jpeg)$', document_path.lower())):
			text = extract_text(document_path)
			text = [t['text'] for t in text]
			text = '\n'.join(text)
		if bool(re.search(r'\.(txt)$', document_path.lower())):
			f = open(document_path, "r") 
			text =f.read()
		if text is not None and len(text) > 1:
			sentences = text_to_sentences(text)
			current_entities = []
			for s in sentences:
				current_entities += entity_linking(s)
			current_entities_with_id = []
			for e in current_entities:
				e['entity_dbpedia_id'] = wikipage_id_to_dbpedia_id(e['entity_wikipage_id'])
				e['document'] = document_path
				if e['entity_dbpedia_id'] is not None:
					current_entities_with_id.append(e)
			entities += current_entities_with_id
	######
	triplets = entity_to_knowledge_triplets(entities,
		related_subject_num = 2,
		related_object_num = 2,
		common_object_number = 2,
		common_subject_number = 2,
		connected_entity_linkage_number = 2)
	####
	ingest_knowledge_triplets_to_neo4j(triplets, neo4j_session)
	return triplets

'''
document_paths = [
	"/entity_linking_test_photo.jpg",
	"/entity_linking_test_speech.mp3",
	"/entity_linking_test_text.txt"]
documents_to_knowledge_graph(document_paths)
'''
#######jessica_knowledge_linking.py#######
