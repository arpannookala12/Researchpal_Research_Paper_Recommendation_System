import pandas as pd
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Paper
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import papers from processed CSV data'
    
    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to CSV file')
        parser.add_argument('--limit', type=int, default=None, help='Limit number of papers to import')
    
    def handle(self, *args, **options):
        file_path = options['file']
        limit = options['limit']
        
        if not file_path or not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} does not exist'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Importing papers from {file_path}'))
        
        # Load data
        df = pd.read_csv(file_path)
        if limit:
            df = df.head(limit)
        
        # Import papers
        papers_created = 0
        papers_updated = 0
        
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Importing papers"):
            try:
                paper, created = Paper.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'title': row['title'],
                        'abstract': row['abstract'],
                        'authors': row['authors'].split(',') if isinstance(row['authors'], str) else [],
                        'categories': row['categories'],
                        'comments': row['comments'] if 'comments' in row and not pd.isna(row['comments']) else '',
                        'update_date': pd.to_datetime(row['update_date']).date() if 'update_date' in row and not pd.isna(row['update_date']) else None,
                    }
                )
                
                if created:
                    papers_created += 1
                else:
                    papers_updated += 1
            
            except Exception as e:
                logger.error(f"Error importing paper {row['id']}: {str(e)}")
        
        self.stdout.write(self.style.SUCCESS(
            f'Import completed: {papers_created} papers created, {papers_updated} papers updated'
        ))