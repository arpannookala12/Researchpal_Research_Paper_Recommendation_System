import pandas as pd
import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
import logging
import os
import torch

logger = logging.getLogger(__name__)

class LanceDBStorage:
    """Class for storing and retrieving vectors using LanceDB."""
    
    def __init__(self, db_path="lancedb_directory"):
        """Initialize LanceDB connection."""
        os.makedirs(db_path, exist_ok=True)
        self.db = lancedb.connect(db_path)
        logger.info("Connected to LanceDB at %s", db_path)
        
        # Register embedding functions
        self.registry = get_registry()
    
    def create_paper_table(self, df, table_name="research_papers"):
        """Create a table with paper data and embeddings."""
        logger.info("Creating table %s with %d papers", table_name, len(df))
        
        # Register the embedding function for the table schema
        embedding_function = self.registry.get("sentence-transformers").create(
            name="allenai-specter",
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        
        # Define the LanceDB schema with Pydantic
        class TextData(LanceModel):
            id: str
            title: str
            authors: str
            abstract: str
            categories: str
            comments: str
            update_date: str
            enhanced_text: str = embedding_function.SourceField()  # Source text for embeddings
            embedding: Vector(embedding_function.ndims()) = embedding_function.VectorField()
        
        # Create the table (overwrite if it exists)
        table = self.db.create_table(table_name, schema=TextData, mode="overwrite")
        
        # Convert the DataFrame to a list of dictionaries
        data = df[["id", "title", "authors", "abstract", "categories", 
                   "comments", "update_date", "enhanced_text"]].astype(str).to_dict(orient="records")
        
        # Add data to the table
        table.add(data)
        
        logger.info("Successfully added %d papers to table %s", len(data), table_name)
        return table
    
    def get_similar_papers(self, query_embedding, table_name="research_papers", k=10):
        """Get similar papers based on embedding similarity."""
        table = self.db.open_table(table_name)
        
        # Search for similar papers
        results = table.search(query_embedding).metric("cosine").limit(k).to_pandas()
        
        return results