"""
Main script for processing Instagram network logs and generating Gephi files.
"""
import logging
import sys
from pathlib import Path
from network_logs_to_json import main as process_network_logs
from json_reader import InstagramJsonReader
from file_writer import GephiFileWriter

def setup_logging():
    """Configure logging for the application."""
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    log_file = output_dir / 'instagram_graph.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file)
        ]
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Step 1: Process network logs to JSON
        logger.info("Step 1: Processing network logs to JSON files")
        process_network_logs()
        
        # Step 2: Generate Gephi files
        logger.info("Step 2: Generating Gephi files")
        reader = InstagramJsonReader()
        reader.read_files()
        
        writer = GephiFileWriter()
        writer.write_files(reader.get_nodes(), reader.get_edges())
        
        logger.info("✅ All processing completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 