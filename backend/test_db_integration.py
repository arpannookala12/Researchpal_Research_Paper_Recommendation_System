# backend/test_db_integration.py
import os
import sys
import django
import json
import pandas as pd
import numpy as np
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from utils.postgresql_utils import PostgreSQLClient
from utils.mongodb_utils import MongoDBClient
from utils.lancedb_utils import LanceDBClient
from core.models import Paper, PaperEmbedding
from sentence_transformers import SentenceTransformer

def test_postgresql():
    """Test PostgreSQL connection and operations."""
    print("\n--- Testing PostgreSQL Integration ---")
    
    try:
        # Create PostgreSQL client
        pg_client = PostgreSQLClient()
        pg_client.connect()
        
        # Test query
        result = pg_client.execute_query("SELECT version();")
        print(f"PostgreSQL Version: {result[0][0]}")
        
        # Test table existence
        tables = pg_client.execute_query(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        )
        print(f"Available tables: {[table[0] for table in tables]}")
        
        pg_client.disconnect()
        print("PostgreSQL integration test successful!")
        return True
    
    except Exception as e:
        print(f"PostgreSQL integration test failed: {str(e)}")
        return False

def test_mongodb():
    """Test MongoDB connection and operations."""
    print("\n--- Testing MongoDB Integration ---")
    
    try:
        # Create MongoDB client
        mongo_client = MongoDBClient()
        mongo_client.connect()
        
        # Test collection operations
        collection_name = "test_collection"
        
        # Insert a document
        doc_id = mongo_client.insert_one(collection_name, {"test": "document", "timestamp": datetime.now()})
        print(f"Inserted document with ID: {doc_id}")
        
        # Find the document
        docs = mongo_client.find(collection_name, {"_id": doc_id})
        print(f"Found document: {docs[0]['test']}")
        
        # Delete the document
        mongo_client.delete_one(collection_name, {"_id": doc_id})
        print(f"Deleted test document")
        
        mongo_client.disconnect()
        print("MongoDB integration test successful!")
        return True
    
    except Exception as e:
        print(f"MongoDB integration test failed: {str(e)}")
        return False

def test_lancedb():
    """Test LanceDB connection and operations."""
    print("\n--- Testing LanceDB Integration ---")
    
    try:
        # Create LanceDB client
        lance_client = LanceDBClient()
        lance_client.connect()
        
        # Create test data
        test_data = [
            {"id": "1", "text": "This is a test document", "embedding": np.random.rand(384).tolist()},
            {"id": "2", "text": "Another test document", "embedding": np.random.rand(384).tolist()},
            {"id": "3", "text": "Yet another test document", "embedding": np.random.rand(384).tolist()}
        ]
        
        # Create a test table
        table_name = "test_table"
        table = lance_client.create_table(table_name, test_data, mode="create")
        print(f"Created table: {table_name}")
        
        # Search for similar vectors
        query_vector = np.random.rand(384).tolist()
        results = lance_client.search_similar(table_name, query_vector, k=2)
        print(f"Search results: {len(results)} items found")
        
        # Get table info
        info = lance_client.get_table_info(table_name)
        print(f"Table info: {info['num_rows']} rows")
        
        print("LanceDB integration test successful!")
        return True
    
    except Exception as e:
        print(f"LanceDB integration test failed: {str(e)}")
        return False

def test_django_orm():
    """Test Django ORM with the databases."""
    print("\n--- Testing Django ORM Integration ---")
    
    try:
        # Create a test paper
        paper, created = Paper.objects.get_or_create(
            id="test_paper_id",
            defaults={
                "title": "Test Paper",
                "abstract": "This is a test paper for database integration.",
                "authors": ["Test Author 1", "Test Author 2"],
                "categories": "cs.AI",
                "update_date": datetime.now().date()
            }
        )
        
        if created:
            print(f"Created test paper: {paper.title}")
        else:
            print(f"Retrieved existing test paper: {paper.title}")
        
        # Create a paper embedding
        embedding, created = PaperEmbedding.objects.get_or_create(
            paper=paper,
            model_name="test_model",
            defaults={
                "vector_id": "test_vector_id",
                "dimensions": 384
            }
        )
        
        if created:
            print(f"Created test embedding for paper: {embedding.paper.title}")
        else:
            print(f"Retrieved existing embedding for paper: {embedding.paper.title}")
        
        # Query the paper
        retrieved_paper = Paper.objects.get(id="test_paper_id")
        print(f"Retrieved paper through ORM: {retrieved_paper.title}")
        
        print("Django ORM integration test successful!")
        return True
    
    except Exception as e:
        print(f"Django ORM integration test failed: {str(e)}")
        return False

def test_embedding_generation():
    """Test embedding generation and storage."""
    print("\n--- Testing Embedding Generation and Storage ---")
    
    try:
        # Initialize embedding model
        model_name = "all-MiniLM-L6-v2"
        model = SentenceTransformer(model_name)
        print(f"Loaded embedding model: {model_name}")
        
        # Generate embeddings for a test text
        test_text = "This is a test document for embedding generation."
        embedding = model.encode(test_text)
        print(f"Generated embedding with shape: {embedding.shape}")
        
        # Store in LanceDB
        lance_client = LanceDBClient()
        lance_client.connect()
        
        table_name = "test_embeddings"
        test_data = [
            {"id": "test_1", "text": test_text, "embedding": embedding.tolist()}
        ]
        
        table = lance_client.create_table(table_name, test_data, mode="create")
        print(f"Stored embedding in LanceDB table: {table_name}")
        
        # Search for similar
        results = lance_client.search_similar(table_name, embedding.tolist(), k=1)
        print(f"Retrieved similar document with ID: {results.iloc[0]['id']}")
        
        print("Embedding generation and storage test successful!")
        return True
    
    except Exception as e:
        print(f"Embedding generation and storage test failed: {str(e)}")
        return False

def main():
    """Run all integration tests."""
    print("=== Starting Database Integration Tests ===")
    
    results = {
        "PostgreSQL": test_postgresql(),
        "MongoDB": test_mongodb(),
        "LanceDB": test_lancedb(),
        "Django ORM": test_django_orm(),
        "Embedding Generation": test_embedding_generation()
    }
    
    print("\n=== Database Integration Test Results ===")
    for test, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test}: {status}")
    
    # Overall result
    all_passed = all(results.values())
    print(f"\nOverall result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())