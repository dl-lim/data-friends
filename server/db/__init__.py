# Initialisation file for all database elements
from db.service import create_tables
from db.docs import add_document, process_document, Doc, get_docs, get_doc_by_name
from db.terms import get_terms, get_term_frequencies, tf_idf