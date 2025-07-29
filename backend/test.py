"""
Basic example of Azure OpenAI LLM call and Azure AI Search query using langchain_openai.
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Azure Cognitive Search configuration
AI_SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
AI_SEARCH_KEY = os.environ["AZURE_SEARCH_KEY"]
AI_SEARCH_INDEX = os.environ["AZURE_SEARCH_INDEX"]

# Azure OpenAI configuration
AOAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Initialize clients
search_client = SearchClient(AI_SEARCH_ENDPOINT, AI_SEARCH_INDEX, AzureKeyCredential(AI_SEARCH_KEY))

aoai_client = AzureOpenAI(
    azure_endpoint=AOAI_ENDPOINT,
    api_key=AOAI_KEY,
    api_version="2023-05-15"
)

primary_llm = AzureChatOpenAI(
    azure_deployment=AOAI_DEPLOYMENT,
    api_version="2024-05-01-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=AOAI_KEY,
    azure_endpoint=AOAI_ENDPOINT
)

def basic_llm_call(user_input):
    """
    Make a basic LLM call using langchain_openai.
    
    Args:
        user_input (str): User input text
        
    Returns:
        str: LLM response content
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that analyzes resumes and job requirements."},
        {"role": "user", "content": user_input}
    ]
    
    response = primary_llm.invoke(messages)
    return response.content

def basic_search(search_query, top_results=3):
    """
    Perform a basic search using Azure AI Search.
    
    Args:
        search_query (str): Text to search for
        top_results (int): Number of results to return
        
    Returns:
        list: Formatted search results
    """
    # Generate embeddings for vector search
    query_vector = generate_embeddings(search_query)
    
    # Create vector query
    vector_query = VectorizedQuery(
        vector=query_vector, 
        k_nearest_neighbors=top_results, 
        fields="searchVector"
    )
    
    # Perform search with both text and vector queries
    results = search_client.search(
        search_text=search_query,
        vector_queries=[vector_query],
        top=top_results
    )
    
    # Format results
    formatted_results = []
    for result in results:
        formatted_results.append({
            "score": result.get("@search.score"),
            "name": result.get('sourceFileName', 'Unknown'),
            "jobTitle": result.get('jobTitle', 'Not specified'),
            "experienceLevel": result.get('experienceLevel', 'Not specified'),
            "content": result.get('content', '')[:300] + "..."  # First 300 chars
        })
    
    return formatted_results

def generate_embeddings(text, model="text-embedding-ada-002"):
    """
    Generate embeddings using Azure OpenAI.
    
    Args:
        text (str): Text to generate embeddings for
        model (str): Embedding model name
        
    Returns:
        list: Embedding vector
    """
    return aoai_client.embeddings.create(input=[text], model=model).data[0].embedding

if __name__ == "__main__":
    # Example LLM call
    print("=== Azure OpenAI LLM Call (via langchain_openai) ===")
    user_query = "What skills should I look for in a Python developer?"
    llm_response = basic_llm_call(user_query)
    print(f"Query: {user_query}")
    print(f"LLM Response: {llm_response}\n")
    
    # Example search query
    print("=== Azure AI Search Query ===")
    search_query = "python developer machine learning"
    search_results = basic_search(search_query)
    
    print(f"Search Query: {search_query}")
    print(f"Found {len(search_results)} results:\n")
    
    for i, result in enumerate(search_results, 1):
        print(f"Result {i}:")
        print(f"  Score: {result['score']:.4f}")
        print(f"  Name: {result['name']}")
        print(f"  Job Title: {result['jobTitle']}")
        print(f"  Experience Level: {result['experienceLevel']}")
        print(f"  Content Preview: {result['content']}")
        print()