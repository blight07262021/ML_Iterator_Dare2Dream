import chromadb
from chromadb.utils import embedding_functions
from sqlalchemy import text
from .database import engine
import pandas as pd
from typing import List, Dict

# Use a pre-built embedding function from sentence-transformers.
# This model is small and efficient for this task. It will be downloaded on the first run.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

# Initialize the ChromaDB client.
# This configuration will store the vector database on disk in the 'chroma_db' directory.
client = chromadb.PersistentClient(path="./chroma_db")

def sync_project_summaries(project_id: int) -> Dict:
    """
    Fetches all summaries for a specific project from your primary SQL database,
    generates embeddings for them, and stores them in a dedicated ChromaDB collection.
    """
    collection_name = f"project_{project_id}"

    # 1. Fetch summaries from the primary database (MySQL).
    query = text(f"""
        SELECT ss.id, ss.summary 
        FROM session_summary ss
        JOIN interviews i ON ss.interview_id = i.id
        WHERE i.project_id = {project_id};
    """)
    try:
        df = pd.read_sql(query, engine)
        if df.empty:
            print(f"No summaries found for project {project_id}. Nothing to sync.")
            return {"status": "success", "message": "No summaries available to sync."}
    except Exception as e:
        print(f"Error fetching summaries for project {project_id}: {e}")
        raise ConnectionError(f"Could not fetch summaries from the database: {e}")

    # 2. Get or create a unique ChromaDB collection for this project.
    # The embedding function is passed here so ChromaDB can handle embedding generation.
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=sentence_transformer_ef
    )

    # 3. Prepare the data in the format ChromaDB requires.
    documents = df['summary'].tolist()
    # We store the original summary ID in the metadata for potential reference.
    metadatas = [{"source": f"summary_{row['id']}"} for index, row in df.iterrows()]
    ids = [f"summary_{row['id']}" for index, row in df.iterrows()]

    # 4. Upsert the data. 'Upsert' is used to add new documents or update existing ones.
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully synced {len(documents)} summaries for project {project_id} into ChromaDB collection '{collection_name}'.")
    return {"status": "success", "synced_count": len(documents)}


def query_insights(project_id: int, question: str, n_results: int = 3) -> List[str]:
    """
    Queries the vector database for a specific project to find the most relevant
    interview summary snippets based on a user's question.
    """
    collection_name = f"project_{project_id}"
    try:
        collection = client.get_collection(name=collection_name, embedding_function=sentence_transformer_ef)
    except ValueError:
        # This error occurs if the collection doesn't exist, which means sync_project_summaries hasn't been run.
        print(f"ChromaDB collection '{collection_name}' not found. Summaries may need to be synced.")
        return []

    # 5. Perform the similarity search.
    # The query text is embedded, and the vectors are compared to find the closest matches.
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    # The actual text content is returned within the 'documents' key.
    return results['documents'][0] if results.get('documents') else []
