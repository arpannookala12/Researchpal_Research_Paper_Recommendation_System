import pandas as pd
import argparse
import logging
import os
from sklearn.model_selection import train_test_split

from preprocessing.text_processor import TextProcessor
from embeddings.specter_embeddings import SpecterEmbeddingGenerator
from storage.lancedb_storage import LanceDBStorage
from data_loaders.arxiv_loader import ArxivLoader

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process ArXiv data for recommendation system")
    
    # Input/output options
    parser.add_argument("--input-file", type=str, required=True,
                      help="Path to ArXiv JSON data file")
    parser.add_argument("--output-dir", type=str, default="processed_data",
                      help="Directory to save processed data")
    
    # Processing options
    parser.add_argument("--sample-size", type=int, default=100000,
                      help="Number of papers to sample from the dataset")
    parser.add_argument("--min-papers-per-category", type=int, default=20,
                      help="Minimum papers per category for stratified sampling")
    parser.add_argument("--batch-size", type=int, default=32,
                      help="Batch size for embedding generation")
    
    # Split options
    parser.add_argument("--train-size", type=float, default=0.7,
                      help="Proportion of data to use for training")
    parser.add_argument("--val-size", type=float, default=0.15,
                      help="Proportion of data to use for validation")
    
    return parser.parse_args()

def main():
    """Main function to process ArXiv data."""
    args = parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load data
    arxiv_loader = ArxivLoader()
    df = arxiv_loader.load_arxiv_data(args.input_file, nrows=args.sample_size)
    
    # Initialize text processor
    text_processor = TextProcessor()
    
    # Create stratified sample
    df_filtered = text_processor.stratify_sample(df, min_papers_per_category=args.min_papers_per_category)
    
    # Split data into train, validation, and test sets
    train_df, temp_df = train_test_split(
        df_filtered,
        train_size=args.train_size,
        stratify=df_filtered['categories'],
        random_state=42
    )
    
    val_size = args.val_size / (1 - args.train_size)
    val_df, test_df = train_test_split(
        temp_df,
        train_size=val_size,
        stratify=temp_df['categories'],
        random_state=42
    )
    
    # Process data (clean text and create enhanced text)
    train_df = text_processor.process_dataframe(train_df)
    val_df = text_processor.process_dataframe(val_df)
    test_df = text_processor.process_dataframe(test_df)
    
    # Save processed data
    train_df.to_csv(os.path.join(args.output_dir, "train_df.csv"), index=False)
    val_df.to_csv(os.path.join(args.output_dir, "val_df.csv"), index=False)
    test_df.to_csv(os.path.join(args.output_dir, "test_df.csv"), index=False)
    
    # Initialize embedding generator
    embedding_generator = SpecterEmbeddingGenerator(batch_size=args.batch_size)
    
    # Initialize LanceDB storage
    lancedb_storage = LanceDBStorage(db_path=os.path.join(args.output_dir, "lancedb_directory"))
    
    # Create LanceDB table with embeddings
    lancedb_storage.create_paper_table(train_df, table_name="research_papers")
    
    logger.info("Data processing completed successfully")

if __name__ == "__main__":
    main()