"""
Effort Predictor Module
Predicts development effort based on ARXML complexity metrics.
"""

from typing import Dict


class EffortPredictor:
    """Predicts development effort based on ARXML complexity metrics."""
    
    # Effort weights for different metrics (in person-hours)
    WEIGHTS = {
        'components': 8.0,      # 8 hours per component
        'interfaces': 4.0,      # 4 hours per interface
        'ports': 2.0,           # 2 hours per port
        'signals': 1.5,         # 1.5 hours per signal
        'data_elements': 1.0,   # 1 hour per data element
        'packages': 0.5         # 0.5 hours per package
    }
    
    # Base effort for project setup and infrastructure
    BASE_EFFORT = 16.0  # 2 days (16 hours)
    
    def __init__(self, custom_weights: Dict[str, float] = None):
        """
        Initialize the effort predictor.
        
        Args:
            custom_weights: Optional custom weights for metrics
        """
        if custom_weights:
            self.weights = {**self.WEIGHTS, **custom_weights}
        else:
            self.weights = self.WEIGHTS.copy()
    
    def predict(self, metrics: Dict[str, int]) -> Dict[str, float]:
        """
        Predict effort based on complexity metrics.
        
        Args:
            metrics: Dictionary of complexity metrics
            
        Returns:
            Dictionary containing effort predictions in different units
        """
        total_effort = self.BASE_EFFORT
        
        breakdown = {}
        for metric, count in metrics.items():
            if metric in self.weights:
                effort = count * self.weights[metric]
                breakdown[metric] = effort
                total_effort += effort
        
        return {
            'total_hours': round(total_effort, 2),
            'total_days': round(total_effort / 8, 2),
            'total_weeks': round(total_effort / 40, 2),
            'breakdown': breakdown,
            'base_effort': self.BASE_EFFORT
        }
    
    def get_complexity_score(self, metrics: Dict[str, int]) -> float:
        """
        Calculate a complexity score based on metrics.
        
        Args:
            metrics: Dictionary of complexity metrics
            
        Returns:
            Complexity score (higher means more complex)
        """
        score = 0.0
        for metric, count in metrics.items():
            if metric in self.weights:
                score += count * self.weights[metric]
        return round(score, 2)
