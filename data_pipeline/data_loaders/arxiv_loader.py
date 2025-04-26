import pandas as pd
import json
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

class ArxivLoader:
    """Class for loading ArXiv metadata."""
    
    def load_arxiv_data(self, filepath, nrows=None):
        """Load ArXiv data from JSON file with selected fields."""
        logger.info(f"Loading data from {filepath}")
        
        # Define the columns to extract
        cols = ['id', 'title', 'abstract', 'categories', 'authors', 'comments', 'update_date']
        
        # Load data and extract relevant fields
        data = []
        with open(filepath, encoding='latin-1') as f:
            for i, line in enumerate(tqdm(f, desc="Loading data")):
                if nrows is not None and i >= nrows:
                    break
                    
                doc = json.loads(line)
                categories = doc.get('categories', '').strip()
                
                if categories:  # Include only rows with categories
                    data.append([
                        doc.get('id'),
                        doc.get('title', ''),
                        doc.get('abstract', ''),
                        categories,
                        doc.get('authors', ''),
                        doc.get('comments', ''),
                        doc.get('update_date', '')
                    ])
        
        # Convert data to DataFrame
        df = pd.DataFrame(data, columns=cols)
        
        # Convert dates
        df['update_date'] = pd.to_datetime(df['update_date'], errors='coerce')
        
        # Drop rows with missing abstracts or titles
        df = df.dropna(subset=['abstract', 'title'])
        
        logger.info(f"Loaded {len(df)} papers")
        return df