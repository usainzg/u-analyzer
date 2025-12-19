# U-Analyzer

A fitness data analyzer inspired by DC Rainmaker's analyzer tool. This tool allows you to upload, parse, and analyze fitness data files from various formats.

## Features

- Parse multiple fitness file formats (FIT, GPX, TCX)
- Compare data from different devices/activities
- Synchronize and analyze metrics (heart rate, speed, distance, cadence, power, etc.)
- Generate statistics and comparisons
- Export data for visualization

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```python
from u_analyzer import Analyzer

# Create analyzer instance
analyzer = Analyzer()

# Load files
analyzer.load_file('activity1.fit')
analyzer.load_file('activity2.gpx')

# Get synchronized data
data = analyzer.get_synchronized_data()

# Get statistics
stats = analyzer.get_statistics()
```

## Supported File Formats

- **FIT**: Native Garmin/Wahoo format
- **GPX**: GPS Exchange Format
- **TCX**: Training Center XML

## Development

### Running Tests

```bash
pytest tests/
```

## License

MIT
