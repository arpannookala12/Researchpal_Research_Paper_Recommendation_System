# backend/utils/lancedb_utils.py
import lancedb
import pandas as pd
import numpy as np
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

class LanceDBClient:
    """Utility class for LanceDB operations."""
    
    def __init__(self, db_uri=None):
        """Initialize LanceDB connection."""
        self.db_uri = db_uri or settings.LANCEDB_PATH
        self.db = None
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_uri), exist_ok=True)
    
    def connect(self):
        """Connect to LanceDB."""
        try:
            self.db = lancedb.connect(self.db_uri)
            logger.info(f"Connected to LanceDB at {self.db_uri}")
            return self.db
        except Exception as e:
            logger.error(f"Error connecting to LanceDB: {str(e)}")
            raise
    
    def create_table(self, table_name, data, schema=None, mode="create"):
        """Create a table with the given data."""
        if not self.db:
            self.connect()
        
        try:
            if mode == "create" and table_name in self.db.table_names():
                logger.info(f"Table {table_name} already exists, dropping it.")
                self.db.drop_table(table_name)
            
            if table_name in self.db.table_names():
                logger.info(f"Opening existing table {table_name}.")
                table = self.db.open_table(table_name)
                # Add data to existing table
                if data is not None:
                    table.add(data)
            else:
                logger.info(f"Creating new table {table_name}.")
                table = self.db.create_table(table_name, data=data, schema=schema)
            
            return table
        
        except Exception as e:
            logger.error(f"Error creating table {table_name}: {str(e)}")
            raise
    
    def search_similar(self, table_name, query_vector, k=10, metric="cosine"):
        """Search for similar vectors in a table."""
        if not self.db:
            self.connect()
        
        try:
            table = self.db.open_table(table_name)
            results = table.search(query_vector).limit(k).metric(metric).to_pandas()
            return results
        except Exception as e:
            logger.error(f"Error searching table {table_name}: {str(e)}")
            raise
    
    def get_table_info(self, table_name):
        """Get information about a table."""
        if not self.db:
            self.connect()
        
        try:
            table = self.db.open_table(table_name)
            return {
                "name": table_name,
                "num_rows": len(table),
                "schema": table.schema
            }
        except Exception as e:
            logger.error(f"Error getting info for table {table_name}: {str(e)}")
            raise