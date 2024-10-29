from quart import Quart, request
from db import add_document, create_tables, process_document, get_docs, get_terms, get_term_frequencies
from query import process_query
import re
import json


# Create engine (web-server)
app = Quart(__name__)

# Default route
@app.route('/')
def default():
    """
    The default route for the application.
    """
    return "Welcome to this Rag application!\n"


# Route for receiving a user query, processing it and returning the final response.
@app.route('/query')
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
@app.route('/add-document', methods=["POST"])
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
        return  f'You have added this document: {name}\n'
    return 'Document not added ...\n'    

@app.route('/docs')
async def docs():
    await get_docs()
    return "Done"

@app.route('/terms')
async def terms():
    await get_terms()
    return "Done"

@app.route('/term-frequencies')
async def term_frequencies():
    await get_term_frequencies()
    return "Done"

# Start the app
if __name__ == "__main__":
    create_tables()
    app.run()