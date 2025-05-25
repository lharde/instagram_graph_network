"""
Module for writing processed Instagram data to CSV files.
"""
import csv
import logging
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class GephiFileWriter:
    def __init__(self, output_dir: str = 'output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.nodes_file = self.output_dir / 'nodes.csv'
        self.edges_file = self.output_dir / 'edges.csv'

    def write_files(self, nodes: Dict[str, Tuple[str, str]], edges: List[Tuple[str, str]]) -> None:
        """Write nodes and edges to their respective CSV files."""
        if not nodes:
            raise ValueError("No nodes to write")
        if not edges:
            raise ValueError("No edges to write")
            
        logger.info(f"Writing {len(nodes)} nodes and {len(edges)} edges to CSV files")
        
        try:
            self._write_nodes(nodes)
            self._write_edges(edges)
        except Exception as e:
            logger.error(f"Error writing CSV files: {str(e)}")
            raise

    def _write_nodes(self, nodes: Dict[str, Tuple[str, str]]) -> None:
        """Write nodes to CSV file."""
        logger.debug(f"Writing nodes to {self.nodes_file}")
        
        try:
            with open(self.nodes_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Id', 'Label', 'FullName', 'Username'])
                for node_id, (fullname, username) in sorted(nodes.items()):
                    writer.writerow([node_id, username, fullname, username])
        except Exception as e:
            logger.error(f"Error writing nodes file: {str(e)}")
            raise

    def _write_edges(self, edges: List[Tuple[str, str]]) -> None:
        """Write edges to CSV file."""
        logger.debug(f"Writing edges to {self.edges_file}")
        
        try:
            with open(self.edges_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Source', 'Target', 'Type'])
                for source, target in edges:
                    writer.writerow([source, target, 'Directed'])
        except Exception as e:
            logger.error(f"Error writing edges file: {str(e)}")
            raise 