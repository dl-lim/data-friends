import random
import re
from db import tf_idf, get_doc_by_name

async def most_similar_document(query: str) -> (bool, str):
    """
    Find the document most similar to the given query. Using TF-IDF similarity measure.
    :param query: The query provided by the user.
    :return: The most similar document.
    """
    matches = re.findall('[a-zA-Z-]+', query)
    terms = set([match.lower() for match in matches])

    # Process all terms in the query to generate tf_idf scores
    processed_terms = list()
    for term in terms:
        print(term)
        query_terms = await tf_idf(term)
        [processed_terms.append(qt) for qt in query_terms]

    # Calculate the similarity for each document
    relevant_docs = set([qt.doc_name for qt in processed_terms])
    similarity_score = 0
    similar_docs = list()
    for doc in relevant_docs:
        score = sum([qt.tf_idf for qt in processed_terms if qt.doc_name == doc])
        if score > similarity_score:
            similarity_score = score
            similar_docs = [doc]
            continue
        if score == similarity_score:
            similar_docs.append(doc)
            continue

    # If there are multiple documents with equal similarity randomly select one, otherwise return the document with
    # the highest similarity
    if len(similar_docs) == 0:
        return False, ""

    target = similar_docs[0] if len(similar_docs) == 1 else similar_docs[random.randint(0, len(similar_docs) - 1)]
    doc = await get_doc_by_name(target)
    if doc is None:
        return False, ""

    return True, doc[2]


async def process_query(query: str) -> str:
    """
    Process user query and return modified query.
    :param query: The query provided by the user.
    :return: The modified query.
    """
    success, document = await most_similar_document(query)

    if not success:
        return query

    return f"Please respond to the statement {query} with the context of {document}"
