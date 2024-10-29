from db.service import con, cursor
from db.terms import add_term
import re


class Doc:
    def __init__(self, doc_id, name, contents):
        self.id = doc_id if doc_id else None
        self.name = name if name else ""
        self.contents = contents if contents else ""

    def info(self):
        return {
            "id": self.id,
            "name": self.name,
            "contents": self.contents
        }


async def add_document(name, contents) -> (bool, int):
    """
    Add a document to the database.
    :param name: The name of the document.
    :param contents: The contents of the document.
    :return: True if the document was added, False otherwise and id value of the document.
    """
    # Check for duplicates
    check_query = "SELECT * FROM docs WHERE name=?"
    query = cursor.execute(check_query, (name,))
    if query.fetchone() is not None:
        return False, 0

    # Insert document into database
    doc_query = "INSERT INTO docs (name, contents) VALUES(?,? )"
    cur = cursor.execute(doc_query, (name, contents))
    con.commit()
    return True, cur.lastrowid


async def process_document(contents: str, doc_id: int) -> None :
    """
    Process document. Find all individual terms and add them to the database.

    :param contents: The contents of the document.
    :param doc_id: The id of the document.
    :return: None.
    """
    # Find all unique terms
    matches = re.findall('[a-zA-Z-]+', contents)
    res = set([match.lower() for match in matches])
    # Add term to database if required
    for term in res:
        count = len([1 for match in matches if match.lower() == term])
        await add_term(term, doc_id, count)


async def get_docs() -> None:
    """
    Find all documents in the database and print them to stdout.
    :return: None.
    """
    doc_query = "SELECT * FROM docs"
    query = cursor.execute(doc_query)
    for doc in query.fetchall():
        print(doc)

async def get_doc_by_name(name: str):
    """
    Find a document in database by name.
    """
    query = cursor.execute("SELECT * FROM docs WHERE name=?", (name,))
    res = query.fetchone()
    return res
