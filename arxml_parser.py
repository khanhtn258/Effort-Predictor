"""
ARXML Parser Module
Parses AUTOSAR ARXML files and extracts complexity metrics.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional


class ARXMLParser:
    """Parser for AUTOSAR ARXML files."""
    
    # Common AUTOSAR namespaces
    NAMESPACES = {
        'ar': 'http://autosar.org/schema/r4.0',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }
    
    def __init__(self, filepath: str):
        """
        Initialize the parser with an ARXML file.
        
        Args:
            filepath: Path to the ARXML file
        """
        self.filepath = filepath
        self.tree = None
        self.root = None
        
    def parse(self) -> bool:
        """
        Parse the ARXML file.
        
        Returns:
            True if parsing was successful, False otherwise
        """
        try:
            self.tree = ET.parse(self.filepath)
            self.root = self.tree.getroot()
            return True
        except Exception as e:
            print(f"Error parsing ARXML file: {e}")
            return False
    
    def extract_metrics(self) -> Dict[str, int]:
        """
        Extract complexity metrics from the ARXML file.
        
        Returns:
            Dictionary containing various complexity metrics
        """
        if self.root is None:
            return {}
        
        metrics = {
            'components': 0,
            'interfaces': 0,
            'ports': 0,
            'signals': 0,
            'data_elements': 0,
            'packages': 0
        }
        
        # Count AR-PACKAGES
        metrics['packages'] = len(self._find_all_elements('AR-PACKAGE'))
        
        # Count SW-COMPONENT-PROTOTYPE (components)
        metrics['components'] = len(self._find_all_elements('SW-COMPONENT-PROTOTYPE'))
        
        # Count SW-COMPONENT-TYPE variations
        metrics['components'] += len(self._find_all_elements('APPLICATION-SW-COMPONENT-TYPE'))
        metrics['components'] += len(self._find_all_elements('COMPOSITION-SW-COMPONENT-TYPE'))
        
        # Count interfaces
        metrics['interfaces'] = len(self._find_all_elements('SENDER-RECEIVER-INTERFACE'))
        metrics['interfaces'] += len(self._find_all_elements('CLIENT-SERVER-INTERFACE'))
        
        # Count ports
        metrics['ports'] = len(self._find_all_elements('P-PORT-PROTOTYPE'))
        metrics['ports'] += len(self._find_all_elements('R-PORT-PROTOTYPE'))
        
        # Count signals
        metrics['signals'] = len(self._find_all_elements('SYSTEM-SIGNAL'))
        metrics['signals'] += len(self._find_all_elements('I-SIGNAL'))
        
        # Count data elements
        metrics['data_elements'] = len(self._find_all_elements('DATA-ELEMENT-PROTOTYPE'))
        metrics['data_elements'] += len(self._find_all_elements('VARIABLE-DATA-PROTOTYPE'))
        
        return metrics
    
    def _find_all_elements(self, tag_name: str) -> List:
        """
        Find all elements with the given tag name.
        Handles both with and without namespace.
        
        Args:
            tag_name: Element tag name (without namespace prefix)
            
        Returns:
            List of matching elements
        """
        if self.root is None:
            return []
        
        # First try with the default namespace
        ns_tag = f".//{{{self.NAMESPACES['ar']}}}{tag_name}"
        elements = self.root.findall(ns_tag)
        
        if elements:
            return elements
        
        # If not found with namespace, try without (fallback for files without namespace)
        # Iterate through all elements and match by local tag name
        matching = []
        for elem in self.root.iter():
            # Extract local name from tag (remove namespace)
            local_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if local_name == tag_name:
                matching.append(elem)
        
        return matching
