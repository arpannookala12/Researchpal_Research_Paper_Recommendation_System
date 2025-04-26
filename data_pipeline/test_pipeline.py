import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import lancedb
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Test if LanceDB is working correctly
def test_lancedb_recommendation():
    # Connect to LanceDB
    db_path = "processed_data/lancedb_directory"
    if not os.path.exists(db_path):
        print("LanceDB directory not found. Please run the data processing script first.")
        return False
    
    db = lancedb.connect(db_path)
    
    # Check if the table exists
    if "research_papers" not in db.table_names():
        print("Research papers table not found in LanceDB.")
        return False
    
    # Load the table
    table = db.open_table("research_papers")
    
    # Load a sample test data
    test_df = pd.read_csv("processed_data/test_df.csv")
    if len(test_df) == 0:
        print("Test data is empty.")
        return False
    
    # Load the SBERT model
    model = SentenceTransformer("allenai-specter")
    
    # Generate embedding for a test abstract
    sample_abstract = test_df["abstract"].iloc[0]
    sample_embedding = model.encode(sample_abstract)
    
    # Search for similar papers
    results = table.search(sample_embedding).metric("cosine").limit(5).to_pandas()
    
    # Print results
    print("Test Query Abstract:")
    print(sample_abstract[:200] + "...")
    print("\nTop 5 Recommendations:")
    
    for i, (_, row) in enumerate(results.iterrows()):
        print(f"{i+1}. {row['title']}")
        print(f"   Similarity: {1 - row['_distance']:.4f}")
        print(f"   Category: {row['categories']}")
        print()
    
    print("LanceDB recommendation test completed successfully!")
    return True

if __name__ == "__main__":
    test_lancedb_recommendation()