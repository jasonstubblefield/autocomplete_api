import pysolr
from opensearchpy import OpenSearch

# Initialize the Solr client for the 'recipes4' core
solr = pysolr.Solr('http://localhost:8983/solr/recipes4', always_commit=True)

# Initialize the OpenSearch client without authentication details
os_client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True  # Enables gzip compression for request bodies
)


def fetch_documents_from_solr(start=0, rows=500):
    """Fetch documents from the Solr core in batches."""
    print(f"Fetching documents from Solr starting at {start}...")
    results = solr.search('*:*', **{'fl': 'title_s', 'start': start, 'rows': rows})
    print(f"Fetched {len(results.docs)} documents.")
    return results.docs


def insert_documents_to_opensearch(documents, start_id):
    """Insert documents into the OpenSearch index 'autocomplete' with sequential IDs starting from start_id."""
    if documents:
        print("Inserting documents into OpenSearch...")
    for index, doc in enumerate(documents, start=start_id):
        if 'title_s' in doc:
            # Ensuring UTF-8 encoding of the title
            title_utf8 = doc['title_s'].encode('utf-8').decode('utf-8')
            doc_to_insert = {"id": index, "name": title_utf8}
            os_client.index(index="autocomplete", body=doc_to_insert)
        else:
            print("Document missing 'title_s':", doc)
    print(f"Inserted {len(documents)} documents into OpenSearch.")
    return index + 1  # Return the next start id


def main():
    start = 0
    batch_size = 500
    next_id = 1  # Start ID for documents in OpenSearch
    while True:
        # Fetch documents from Solr in batches
        documents = fetch_documents_from_solr(start, batch_size)
        if not documents:
            print("No more documents to fetch, stopping...")
            break

        # Insert documents into OpenSearch and update next_id
        next_id = insert_documents_to_opensearch(documents, next_id)

        start += batch_size  # Move to the next batch

    print("Documents have been successfully transferred from Solr to OpenSearch.")


if __name__ == "__main__":
    main()
