"""
Module for reading Instagram following data from JSON files.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class InstagramJsonReader:
    def __init__(self, json_dir: str = 'json_followings'):
        self.json_dir = Path(json_dir)
        self.nodes: Dict[str, Tuple[str, str]] = {}  # {id: (full_name, username)}
        self.edges: List[Tuple[str, str]] = []       # [(source_id, target_id)]
        
        if not self.json_dir.exists():
            raise FileNotFoundError(f"Directory {json_dir} does not exist")

    def read_files(self) -> None:
        """Read all JSON files in the directory and populate nodes and edges."""
        json_files = list(self.json_dir.glob('*.json'))
        if not json_files:
            raise FileNotFoundError(f"No JSON files found in {self.json_dir}")
            
        logger.info(f"Found {len(json_files)} JSON files to process")
        
        for json_file in json_files:
            try:
                self._read_single_file(json_file)
            except Exception as e:
                logger.error(f"Error processing {json_file}: {str(e)}")
                raise

    def _read_single_file(self, json_file: Path) -> None:
        """Read a single JSON file and update nodes and edges."""
        logger.debug(f"Reading file: {json_file}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {json_file}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reading {json_file}: {str(e)}")
            raise
            
        # Process main user
        try:
            source_id = data['id']
            source_username = data['username']
            source_fullname = data.get('full_name', '')
            
            if source_id not in self.nodes:
                self.nodes[source_id] = (source_fullname, source_username)
                logger.debug(f"Added new node: {source_username}")
            
            # Process followings
            for following in data.get('followings', []):
                target_id = following['id']
                target_username = following['username']
                target_fullname = following.get('full_name', '')
                
                if target_id not in self.nodes:
                    self.nodes[target_id] = (target_fullname, target_username)
                    logger.debug(f"Added new node: {target_username}")
                
                self.edges.append((source_id, target_id))
                
        except KeyError as e:
            logger.error(f"Missing required field in {json_file}: {str(e)}")
            raise

    def get_nodes(self) -> Dict[str, Tuple[str, str]]:
        """Get the processed nodes."""
        return self.nodes

    def get_edges(self) -> List[Tuple[str, str]]:
        """Get the processed edges."""
        return self.edges 