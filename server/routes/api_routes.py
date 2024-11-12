from quart import Blueprint, request
from db import add_document, process_document
from query import process_query
import re
import json

api_routes = Blueprint('api_routes', __name__)

# Route for receiving a user query, processing it and returning the final response.
@api_routes.route('/query')
async def query():
    """
    Receive a user query, update query to add context and return modified query.
    """
    query_string = request.query_string.decode("utf-8")
    query_string = re.sub(r'%20', ' ', query_string)
    print('Query: ', query_string)
    updated_query = await process_query(query_string)
    # The updated query would then be sent to the LLM and the response returned here.
    # However, for this demo return the updated query.
    return f'This is the updated query: {updated_query}\n'


# Route for adding a document to the database
@api_routes.route('/add-document', methods=["POST"])
async def new_document():
    """
    Process for processing and adding new document to the context corpus. Correct data is provided in json format.
    """
    data = await request.get_data()
    # Validate data
    try:
        data = json.loads(data.decode('utf-8'))
        name = data.get('name')
        contents = data.get('contents')
        if name is None or contents is None:
            return 'Document format invalid\n'
    except Exception as e:
        print(f"Exception {e}")
        return 'Document format invalid\n'

    # Add document to database
    success, doc_id = await add_document(name, contents)

    # If successful process all terms within the document
    if success:
        await process_document(contents, doc_id)
        return f'You have added this document: {name}\n'
    return 'Document not added ...\n'