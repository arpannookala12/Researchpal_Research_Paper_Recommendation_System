# backend/utils/postgresql_utils.py
import psycopg2
import psycopg2.extras
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class PostgreSQLClient:
    """Utility class for direct PostgreSQL operations."""
    
    def __init__(self, connection_params=None):
        """Initialize PostgreSQL connection parameters."""
        if connection_params:
            self.connection_params = connection_params
        else:
            # Parse from Django's DATABASE_URL
            db_settings = settings.DATABASES['default']
            self.connection_params = {
                'host': db_settings.get('HOST', 'localhost'),
                'port': db_settings.get('PORT', '5432'),
                'database': db_settings.get('NAME', 'paper_recommendation'),
                'user': db_settings.get('USER', 'postgres'),
                'password': db_settings.get('PASSWORD', 'postgres')
            }
        self.connection = None
    
    def connect(self):
        """Connect to PostgreSQL."""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            logger.info("Connected to PostgreSQL database")
            return self.connection
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {str(e)}")
            raise
    
    def disconnect(self):
        """Disconnect from PostgreSQL."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Disconnected from PostgreSQL database")
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute a query and return results."""
        if not self.connection:
            self.connect()
        
        try:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, params)
                
                if fetch and cursor.description:
                    results = cursor.fetchall()
                    return results
                
                self.connection.commit()
                return None
                
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def bulk_insert(self, table_name, columns, values_list, batch_size=1000):
        """Perform bulk insert operation."""
        if not self.connection:
            self.connect()
        
        try:
            total_rows = len(values_list)
            inserted = 0
            
            with self.connection.cursor() as cursor:
                for i in range(0, total_rows, batch_size):
                    batch = values_list[i:i+batch_size]
                    placeholders = ','.join(['%s'] * len(batch))
                    columns_str = ', '.join(columns)
                    
                    query = f"INSERT INTO {table_name} ({columns_str}) VALUES {placeholders}"
                    cursor.execute(query, batch)
                    
                    inserted += len(batch)
                    logger.info(f"Inserted {inserted}/{total_rows} rows into {table_name}")
                
                self.connection.commit()
            
            return inserted
        
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error performing bulk insert: {str(e)}")
            raise