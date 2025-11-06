#!/usr/bin/env python3
"""
ARXML Effort Predictor CLI
Command-line interface for analyzing ARXML files and predicting development effort.
"""

import argparse
import sys
from pathlib import Path
from arxml_parser import ARXMLParser
from effort_predictor import EffortPredictor


def format_output(metrics: dict, effort: dict) -> str:
    """
    Format the analysis output.
    
    Args:
        metrics: Complexity metrics dictionary
        effort: Effort prediction dictionary
        
    Returns:
        Formatted output string
    """
    output = []
    output.append("=" * 60)
    output.append("ARXML File Analysis Report")
    output.append("=" * 60)
    
    output.append("\nComplexity Metrics:")
    output.append("-" * 60)
    for metric, count in sorted(metrics.items()):
        output.append(f"  {metric.replace('_', ' ').title():.<40} {count:>5}")
    
    output.append("\nEffort Prediction:")
    output.append("-" * 60)
    output.append(f"  Base Effort:................................ {effort['base_effort']:>8.2f} hours")
    
    if effort['breakdown']:
        output.append("\n  Breakdown by Component:")
        for component, hours in sorted(effort['breakdown'].items()):
            output.append(f"    {component.replace('_', ' ').title():.<38} {hours:>8.2f} hours")
    
    output.append("\n  Total Effort Estimates:")
    output.append(f"    Hours:.................................. {effort['total_hours']:>8.2f}")
    output.append(f"    Days (8h/day):.......................... {effort['total_days']:>8.2f}")
    output.append(f"    Weeks (40h/week):...................... {effort['total_weeks']:>8.2f}")
    
    output.append("=" * 60)
    
    return "\n".join(output)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze ARXML files and predict development effort",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sample.arxml
  %(prog)s --output report.txt system.arxml
  %(prog)s --verbose architecture.arxml
        """
    )
    
    parser.add_argument(
        'file',
        type=str,
        help='Path to the ARXML file to analyze'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default: print to stdout)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Check if file exists
    arxml_file = Path(args.file)
    if not arxml_file.exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        return 1
    
    if args.verbose:
        print(f"Analyzing ARXML file: {args.file}")
    
    # Parse ARXML file
    arxml_parser = ARXMLParser(str(arxml_file))
    if not arxml_parser.parse():
        print("Error: Failed to parse ARXML file", file=sys.stderr)
        return 1
    
    if args.verbose:
        print("File parsed successfully")
    
    # Extract metrics
    metrics = arxml_parser.extract_metrics()
    
    if args.verbose:
        print(f"Extracted {len(metrics)} metrics")
    
    # Predict effort
    predictor = EffortPredictor()
    effort = predictor.predict(metrics)
    
    # Format and output results
    result = format_output(metrics, effort)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"Report saved to: {args.output}")
    else:
        print(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
