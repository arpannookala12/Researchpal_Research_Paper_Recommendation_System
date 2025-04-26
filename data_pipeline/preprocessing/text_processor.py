import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """Class for preprocessing text data for the research paper recommendation system."""
    
    def __init__(self):
        """Initialize text processor with NLTK resources."""
        # Download NLTK resources if needed
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('stopwords')
            nltk.download('wordnet')
            nltk.download('omw-1.4')
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """Clean and normalize text data."""
        if pd.isnull(text):
            return ""
            
        # Lowercasing
        text = text.lower()
        
        # Remove special characters and punctuation
        text = re.sub(r'[^a-z0-9\\s]', '', text)
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\\s+', ' ', text).strip()
        
        # Tokenize and remove stopwords, then lemmatize
        tokens = text.split()
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        
        return ' '.join(tokens)
    
    def process_dataframe(self, df):
        """Process the entire dataframe."""
        logger.info("Processing dataframe with %d rows", len(df))
        
        # Apply cleaning to relevant fields
        df['cleaned_title'] = df['title'].apply(self.clean_text)
        df['cleaned_authors'] = df['authors'].apply(self.clean_text)
        df['cleaned_categories'] = df['categories'].apply(self.clean_text)
        df['cleaned_abstract'] = df['abstract'].apply(self.clean_text)
        df['cleaned_comments'] = df['comments'].apply(self.clean_text)
        
        # Create the enhanced text field for embeddings
        df['enhanced_text'] = df.apply(lambda row: f"""
        Title: {row['cleaned_title']} [SEP]
        Authors: {row['cleaned_authors']} [SEP]
        Categories: {row['cleaned_categories']} [SEP]
        Abstract: {row['cleaned_abstract']} [SEP]
        Comments: {row['cleaned_comments']} [SEP]
        Updated on: {row['update_date']}
        """.replace('\\n', ' ').strip(), axis=1)
        
        return df
    
    def stratify_sample(self, df, min_papers_per_category=20):
        """Create a stratified sample based on categories."""
        logger.info("Creating stratified sample with min %d papers per category", 
                   min_papers_per_category)
        
        # Get category counts
        category_counts = df['categories'].value_counts()
        
        # Identify categories with minimum number of occurrences
        valid_categories = category_counts[category_counts >= min_papers_per_category].index
        
        # Filter DataFrame to keep only rows with valid categories
        df_filtered = df[df['categories'].isin(valid_categories)]
        
        logger.info("Filtered dataset size: %d with %d categories", 
                   len(df_filtered), len(valid_categories))
        
        return df_filtered