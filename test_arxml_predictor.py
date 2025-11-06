"""
Unit tests for ARXML Parser and Effort Predictor
"""

import unittest
import os
from pathlib import Path
from arxml_parser import ARXMLParser
from effort_predictor import EffortPredictor


class TestARXMLParser(unittest.TestCase):
    """Test cases for ARXMLParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_file = Path(__file__).parent / 'sample.arxml'
        self.parser = ARXMLParser(str(self.sample_file))
    
    def test_parse_valid_file(self):
        """Test parsing a valid ARXML file."""
        self.assertTrue(self.parser.parse())
        self.assertIsNotNone(self.parser.root)
        self.assertIsNotNone(self.parser.tree)
    
    def test_parse_nonexistent_file(self):
        """Test parsing a non-existent file."""
        parser = ARXMLParser('nonexistent.arxml')
        self.assertFalse(parser.parse())
    
    def test_extract_metrics(self):
        """Test extracting metrics from ARXML file."""
        self.parser.parse()
        metrics = self.parser.extract_metrics()
        
        # Verify metrics dictionary structure
        self.assertIsInstance(metrics, dict)
        self.assertIn('components', metrics)
        self.assertIn('interfaces', metrics)
        self.assertIn('ports', metrics)
        self.assertIn('signals', metrics)
        self.assertIn('data_elements', metrics)
        self.assertIn('packages', metrics)
        
        # Verify sample.arxml content counts
        # 3 AR-PACKAGES
        self.assertEqual(metrics['packages'], 3)
        
        # 2 SW-COMPONENT-PROTOTYPE + 2 APPLICATION-SW-COMPONENT-TYPE + 1 COMPOSITION-SW-COMPONENT-TYPE
        self.assertGreater(metrics['components'], 0)
        
        # 3 interfaces (2 SENDER-RECEIVER + 1 CLIENT-SERVER)
        self.assertEqual(metrics['interfaces'], 3)
        
        # 3 ports (1 P-PORT + 2 mixed)
        self.assertGreater(metrics['ports'], 0)
        
        # 3 signals (2 SYSTEM-SIGNAL + 1 I-SIGNAL)
        self.assertEqual(metrics['signals'], 3)
        
        # 3 VARIABLE-DATA-PROTOTYPE elements
        self.assertEqual(metrics['data_elements'], 3)


class TestEffortPredictor(unittest.TestCase):
    """Test cases for EffortPredictor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.predictor = EffortPredictor()
    
    def test_predict_with_empty_metrics(self):
        """Test prediction with empty metrics."""
        metrics = {}
        effort = self.predictor.predict(metrics)
        
        self.assertIsInstance(effort, dict)
        self.assertIn('total_hours', effort)
        self.assertIn('total_days', effort)
        self.assertIn('total_weeks', effort)
        self.assertIn('breakdown', effort)
        self.assertIn('base_effort', effort)
        
        # Should return base effort only
        self.assertEqual(effort['total_hours'], self.predictor.BASE_EFFORT)
    
    def test_predict_with_metrics(self):
        """Test prediction with sample metrics."""
        metrics = {
            'components': 5,
            'interfaces': 3,
            'ports': 10,
            'signals': 8,
            'data_elements': 15,
            'packages': 3
        }
        
        effort = self.predictor.predict(metrics)
        
        # Verify calculation
        expected = self.predictor.BASE_EFFORT
        expected += 5 * self.predictor.weights['components']
        expected += 3 * self.predictor.weights['interfaces']
        expected += 10 * self.predictor.weights['ports']
        expected += 8 * self.predictor.weights['signals']
        expected += 15 * self.predictor.weights['data_elements']
        expected += 3 * self.predictor.weights['packages']
        
        self.assertEqual(effort['total_hours'], round(expected, 2))
        self.assertEqual(effort['total_days'], round(expected / 8, 2))
        self.assertEqual(effort['total_weeks'], round(expected / 40, 2))
    
    def test_custom_weights(self):
        """Test predictor with custom weights."""
        custom_weights = {'components': 10.0}
        predictor = EffortPredictor(custom_weights)
        
        self.assertEqual(predictor.weights['components'], 10.0)
        # Other weights should remain default
        self.assertEqual(predictor.weights['interfaces'], EffortPredictor.WEIGHTS['interfaces'])
    
    def test_complexity_score(self):
        """Test complexity score calculation."""
        metrics = {
            'components': 5,
            'interfaces': 3,
            'ports': 10
        }
        
        score = self.predictor.get_complexity_score(metrics)
        
        expected = (5 * self.predictor.weights['components'] +
                   3 * self.predictor.weights['interfaces'] +
                   10 * self.predictor.weights['ports'])
        
        self.assertEqual(score, round(expected, 2))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from parsing to prediction."""
        sample_file = Path(__file__).parent / 'sample.arxml'
        
        # Parse file
        parser = ARXMLParser(str(sample_file))
        self.assertTrue(parser.parse())
        
        # Extract metrics
        metrics = parser.extract_metrics()
        self.assertIsInstance(metrics, dict)
        
        # Predict effort
        predictor = EffortPredictor()
        effort = predictor.predict(metrics)
        
        # Verify results
        self.assertGreater(effort['total_hours'], predictor.BASE_EFFORT)
        self.assertGreater(effort['total_days'], 0)
        self.assertGreater(effort['total_weeks'], 0)


if __name__ == '__main__':
    unittest.main()
