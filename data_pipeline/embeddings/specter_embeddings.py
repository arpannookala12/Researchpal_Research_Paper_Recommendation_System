import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import torch
import logging

logger = logging.getLogger(__name__)

class SpecterEmbeddingGenerator:
    """Class for generating AllenAI-Specter embeddings for research papers."""
    
    def __init__(self, batch_size=32):
        """Initialize with AllenAI-Specter model."""
        self.model_name = "allenai-specter"
        self.model = SentenceTransformer(self.model_name)
        self.batch_size = batch_size
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        logger.info("Initialized SpecterEmbeddingGenerator with device: %s", self.device)
    
    def generate_embeddings(self, texts, show_progress=True):
        """Generate embeddings for a list of texts."""
        embeddings = []
        
        # Process in batches to avoid memory issues
        iterator = range(0, len(texts), self.batch_size)
        if show_progress:
            iterator = tqdm(iterator, desc=f"Generating {self.model_name} embeddings")
        
        for i in iterator:
            batch_texts = texts[i:i+self.batch_size]
            batch_embeddings = self.model.encode(batch_texts, show_progress_bar=False)
            embeddings.extend(batch_embeddings)
        
        return np.array(embeddings)
    
    def process_dataframe(self, df, text_column='enhanced_text'):
        """Process entire dataframe and add embeddings."""
        logger.info("Processing dataframe with %d rows to generate embeddings", len(df))
        texts = df[text_column].tolist()
        embeddings = self.generate_embeddings(texts)
        
        # Create a new dataframe with paper IDs and embeddings
        embeddings_df = pd.DataFrame({
            'paper_id': df['id'].tolist(),
            'embedding': list(embeddings)
        })
        
        return embeddings_df