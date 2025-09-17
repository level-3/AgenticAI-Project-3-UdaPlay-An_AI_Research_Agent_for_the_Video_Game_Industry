from datetime import datetime
import os
from typing import Any, Dict, List
import requests
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import text

from lib.tooling import tool
from lib.vector_db import VectorStoreManager, CorpusLoaderService
from lib.rag import RAG
from lib.state_machine import Run

from tavily import TavilyClient

load_dotenv("/home/level-3/udacity/AgenticAI/.env/config.env")


@tool
def GET_request(url: str) -> str:
    """Perform a GET request to the specified URL and return the response text in JSON format."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        return f"An error occurred: {e}"


@tool
def POST_request(url: str, data: dict) -> str:
    """Perform a POST request to the specified URL with the given data and return the response text in JSON format."""
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        return f"An error occurred: {e}"


@tool
def web_search(query: str, search_depth: str = "advanced") -> Dict:
    """
    Search the web using Tavily API
    args:
        query (str): Search query
        search_depth (str): Type of search - 'basic' or 'advanced' (default: advanced)
    """
    api_key = os.getenv("TAVILY_API_KEY")
    client = TavilyClient(api_key=api_key)

    # Perform the search
    search_result = client.search(
        query=query,
        search_depth=search_depth,
        include_answer=True,
        include_raw_content=False,
        include_images=False,
    )

    # Format the results
    formatted_results = {
        "answer": search_result.get("answer", ""),
        "results": search_result.get("results", []),
        "search_metadata": {"timestamp": datetime.now().isoformat(), "query": query},
    }

    return formatted_results


@tool
def list_tables_tool(DB_ENGINE) -> List[str]:
    """
    List all tables in database
    """
    inspector = sqlalchemy.inspect(DB_ENGINE)

    return inspector.get_table_names()


@tool
def get_table_schema_tool(table_name: str, DB_ENGINE) -> List[str]:
    """
    Get schema information about a table. Returns a list of dictionaries.
    - name is the column name
    - type is the column type
    - nullable is whether the column is nullable or not
    - default is the default value of the column
    - primary_key is whether the column is a primary key or not

    Args:
        table_name (str): Table name
    """
    inspector = sqlalchemy.inspect(DB_ENGINE)

    return str(inspector.get_columns(table_name))


@tool
def execute_sql_tool(query: str, DB_ENGINE) -> Any:
    """
    Execute SQL query and return result.
    This will automatically connect to the database and execute the query.
    However, if the query is not valid, an error will be raised

    Args:
        query (str): SQL query
    """
    with DB_ENGINE.begin() as connection:
        answer = connection.execute(text(query)).fetchall()

    return str(answer)


@tool
def search_collection(RAG_collection, query):
    """
    Search the vector database for relevant information.

    args:
        RAG_collection: RAG collection object
        query (str): Search query
    """
    result: Run = RAG_collection.invoke(query)
    return result.get_final_state()["answer"]
