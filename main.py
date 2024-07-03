from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from opensearchpy import OpenSearch, OpenSearchException
from pydantic import BaseModel
from typing import List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# OpenSearch client configuration
client = OpenSearch(
    hosts = [{'host': 'localhost', 'port': 9200}],
    use_ssl = False,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

index_name = "autocomplete"

class Suggestion(BaseModel):
    name: str

@app.get("/autocomplete/", response_model=List[Suggestion])
async def autocomplete(query: str):
    try:
        logger.info(f"Received autocomplete request for query: {query}")
        response = client.search(
            index=index_name,
            body={
                "size": 5,
                "query": {
                    "match_phrase_prefix": {
                        "name": {
                            "query": query,
                            "max_expansions": 10
                        }
                    }
                },
                "_source": ["name"]
            }
        )
        hits = response['hits']['hits']
        suggestions = [Suggestion(name=hit["_source"]["name"]) for hit in hits]
        logger.info(f"Returning {len(suggestions)} suggestions")
        return suggestions
    except OpenSearchException as e:
        logger.error(f"OpenSearch error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenSearch error: {str(e)}")
    except KeyError as e:
        logger.error(f"Unexpected response structure: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected response structure from OpenSearch")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)