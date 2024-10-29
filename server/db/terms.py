from db.service import con, cursor
import math 

async def add_term(name: str, doc_id: int, count: int) -> bool:
    """
    Add a term to the database.
    :param name: Name of the term.
    :param doc_id: ID of the source document.
    :param count: Number of instances of the term in the document (term frequency).
    :return: True if the term was added, False otherwise.
    """
    # Check for duplicates
    check_query = "SELECT * FROM terms WHERE name=?"
    query = cursor.execute(check_query, (name,))
    if query.fetchone() is not None:
        return await update_term(name, doc_id, count)
    
    # calculate idf
    doc_count = cursor.execute("SELECT COUNT(*) FROM docs")
    idf = math.log10(doc_count.fetchone()[0] / 1)

    # Insert term into database
    term_query = "INSERT INTO terms (name, idf) VALUES(?, ?)" 
    term = cursor.execute(term_query, (name, idf))

    # Insert term frequency into database 
    tf_query = "INSERT INTO term_frequencies (doc, term, tf) VALUES(?, ?, ?)" 
    cursor.execute(tf_query, (doc_id, term.lastrowid, count))

    con.commit()
    return True


async def update_term(name: str, doc_id: int, count: int) -> bool:
    """
    Update a term from the database. Recalculate inverse document frequency (idf) and add to term frequencies database.
    :param name: Name of the term.
    :param doc_id: ID of the source document.
    :param count: Number of instances of the term in the document (term frequency).
    :return: True if the term was updated, False otherwise.
    """
    
    total_count_query = cursor.execute("SELECT COUNT(*) FROM docs")
    total_count = total_count_query.fetchone()[0]
    
    # Get count of all documents that include the term
    doc_count_query = cursor.execute("SELECT COUNT (*) FROM (SELECT * FROM (term_frequencies INNER JOIN terms ON term_frequencies.term = terms.id) WHERE terms.name = ?)", (name,))
    doc_count = doc_count_query.fetchone()[0] + 1
    idf = math.log10(total_count / doc_count)

    # Update database
    cursor.execute("UPDATE terms SET idf = ? WHERE name = ?", (idf, name))

    term = cursor.execute("SELECT * FROM terms WHERE name=?", (name,))

    # Insert term frequency into database 
    tf_query = "INSERT INTO term_frequencies (doc, term, tf) VALUES(?, ?, ?)" 
    cursor.execute(tf_query, (doc_id, term.fetchone()[0], count))

    con.commit()
    return True


async def get_terms() -> None:
    """
    Find all terms in the database and print them to stdout.
    :return: None.
    """
    doc_query = "SELECT * FROM terms"
    query = cursor.execute(doc_query)
    for doc in query.fetchall():
        print(doc)

async def get_term_frequencies() -> None:
    """
    Find all term frequencies in the database and print them to stdout.
    :return: None.
    """
    doc_query = "SELECT terms.name, docs.name,  tf FROM ((term_frequencies INNER JOIN terms ON term_frequencies.term = terms.id) INNER JOIN docs ON term_frequencies.doc = docs.id)  ;"
    query = cursor.execute(doc_query)
    for doc in query.fetchall():
        print(doc)


class QueryTerm:
    def __init__(self, name: str, doc_name: str, tf: float, idf: float) -> None:#
        self.name = name
        self.doc_name = doc_name
        self.tf = tf
        self.idf = idf
        self.tf_idf = self.tf * self.idf

async def tf_idf(name: str) -> list[QueryTerm]:
    """
    Calculate TF_IDF score for all instances of the given term.
    :param name: Name of the term.
    :return: List of query terms.
    """
    query = cursor.execute("SELECT terms.name, docs.name, tf, terms.idf FROM ((term_frequencies INNER JOIN terms ON term_frequencies.term = terms.id) INNER JOIN docs ON term_frequencies.doc = docs.id) WHERE terms.name = ?", (name,))
    elements = list()

    for doc in query.fetchall():
        elements.append(QueryTerm(doc[0], doc[1], doc[2], doc[3]))

    return elements