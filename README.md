# Effort-Predictor

A Python tool for analyzing AUTOSAR ARXML files and predicting development effort based on complexity metrics.

## Features

- Parse AUTOSAR ARXML files (AUTOSAR 4.x format)
- Extract complexity metrics including:
  - Number of software components
  - Number of interfaces (Sender-Receiver and Client-Server)
  - Number of ports (Provided and Required)
  - Number of signals and data elements
  - Package structure
- Predict development effort in hours, days, and weeks
- Detailed breakdown of effort by component type
- Command-line interface for easy integration

## Installation

No external dependencies required! This tool uses Python's built-in XML parser.

```bash
# Clone the repository
git clone https://github.com/khanhtn258/Effort-Predictor.git
cd Effort-Predictor

# Make the CLI executable (Unix/Linux/Mac)
chmod +x arxml_predictor.py
```

## Usage

### Basic Usage

```bash
python arxml_predictor.py sample.arxml
```

### Save Report to File

```bash
python arxml_predictor.py --output report.txt sample.arxml
```

### Verbose Output

```bash
python arxml_predictor.py --verbose sample.arxml
```

### Help

```bash
python arxml_predictor.py --help
```

## Example Output

```
============================================================
ARXML File Analysis Report
============================================================

Complexity Metrics:
------------------------------------------------------------
  Components:................................. 5
  Data Elements:.............................. 3
  Interfaces:................................. 3
  Packages:................................... 3
  Ports:...................................... 3
  Signals:.................................... 3

Effort Prediction:
------------------------------------------------------------
  Base Effort:................................    16.00 hours

  Breakdown by Component:
    Components:............................... 40.00 hours
    Data Elements:............................  3.00 hours
    Interfaces:............................... 12.00 hours
    Packages:.................................  1.50 hours
    Ports:....................................  6.00 hours
    Signals:..................................  4.50 hours

  Total Effort Estimates:
    Hours:....................................    83.00
    Days (8h/day):............................    10.38
    Weeks (40h/week):........................     2.08
============================================================
```

## Running Tests

```bash
python -m unittest test_arxml_predictor.py
```

## How It Works

The effort predictor analyzes ARXML files in three steps:

1. **Parsing**: Uses Python's built-in ElementTree XML parser to read ARXML files
2. **Metric Extraction**: Counts various AUTOSAR elements (components, interfaces, ports, etc.)
3. **Effort Calculation**: Applies predefined weights to each metric type to estimate total effort

### Default Effort Weights

- Components: 8 hours each
- Interfaces: 4 hours each
- Ports: 2 hours each
- Signals: 1.5 hours each
- Data Elements: 1 hour each
- Packages: 0.5 hours each
- Base Project Setup: 16 hours

These weights can be customized by modifying the `EffortPredictor` class.

## Project Structure

```
Effort-Predictor/
├── arxml_parser.py          # ARXML file parser
├── effort_predictor.py      # Effort prediction logic
├── arxml_predictor.py       # Command-line interface
├── test_arxml_predictor.py  # Unit tests
├── sample.arxml             # Sample ARXML file for testing
└── README.md                # This file
```

## Supported ARXML Elements

- AR-PACKAGE
- SW-COMPONENT-PROTOTYPE
- APPLICATION-SW-COMPONENT-TYPE
- COMPOSITION-SW-COMPONENT-TYPE
- SENDER-RECEIVER-INTERFACE
- CLIENT-SERVER-INTERFACE
- P-PORT-PROTOTYPE (Provided Ports)
- R-PORT-PROTOTYPE (Required Ports)
- SYSTEM-SIGNAL
- I-SIGNAL
- DATA-ELEMENT-PROTOTYPE
- VARIABLE-DATA-PROTOTYPE

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.