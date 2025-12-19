# U-Analyzer Features

This document describes the features implemented in U-Analyzer, a clone of the DC Rainmaker analyzer.

## Core Functionality

### 1. Multi-Format File Parsing
- **FIT Files**: Native format used by Garmin, Wahoo, and other fitness devices
- **GPX Files**: GPS Exchange Format with support for extensions (heart rate, cadence)
- **TCX Files**: Training Center XML format with full metadata support

### 2. Data Extraction
The analyzer extracts and processes the following metrics from fitness files:
- **GPS Data**: Latitude, Longitude, Altitude
- **Performance Metrics**: Heart Rate, Cadence, Power, Speed, Distance
- **Environmental Data**: Temperature
- **Temporal Data**: Timestamps for synchronization

### 3. Multi-Activity Analysis
- Load and analyze multiple activities simultaneously
- Support for comparing data from different devices recording the same activity
- Automatic file format detection

### 4. Data Synchronization
- Align multiple activities by timestamp
- Normalize timestamps to relative time (starting from 0)
- Maintain both absolute and relative time references
- Enable side-by-side comparison of synchronized data

### 5. Statistical Analysis
For each activity and metric, calculate:
- Minimum value
- Maximum value
- Average value
- Count of data points

Statistics are provided for:
- Heart Rate (bpm)
- Cadence (rpm)
- Speed (m/s)
- Distance (meters)
- Power (watts)
- Altitude (meters)
- Temperature (°C)

### 6. Activity Comparison
- Compare specific metrics across multiple activities
- Side-by-side statistics for device comparison
- Identify differences in recordings from different devices

### 7. Data Export
- Export all data to JSON-serializable format
- Suitable for web-based visualization
- Includes:
  - Activity metadata
  - Synchronized data points
  - Statistical summaries

## API Design

### Simple API
```python
from u_analyzer import Analyzer

# Create analyzer
analyzer = Analyzer()

# Load files
analyzer.load_file('activity1.gpx')
analyzer.load_file('activity2.tcx')
analyzer.load_file('activity3.fit')

# Get statistics
stats = analyzer.get_statistics()

# Get synchronized data
synced = analyzer.get_synchronized_data()

# Compare specific metric
hr_comparison = analyzer.compare_activities('heart_rate')

# Export for visualization
data = analyzer.export_to_dict()
```

## Testing

### Comprehensive Test Suite (34 tests)

#### Unit Tests
- **Models (8 tests)**: Test data structures and calculations
- **Parsers (10 tests)**: Test file parsing for each format
- **Analyzer (13 tests)**: Test core analyzer functionality

#### Integration Tests (3 tests)
- Complete workflow testing
- Multi-activity comparison scenarios
- Real-world usage patterns

### Test Coverage
- Happy path scenarios
- Error handling (missing files, invalid formats)
- Edge cases (empty data, missing metrics)
- Data validation
- JSON serialization

## Comparison with DC Rainmaker Analyzer

### Implemented Features ✓
- [x] Multi-format file support (FIT, GPX, TCX)
- [x] Multiple activity loading
- [x] Data synchronization by timestamp
- [x] Statistical analysis (min, max, avg)
- [x] Metric comparison across activities
- [x] Data export for visualization

### Backend vs Full Application
U-Analyzer provides the **data processing backend** equivalent to DC Rainmaker's analyzer:
- File parsing and validation
- Data extraction and synchronization
- Statistical calculations
- Comparison logic
- Data export

**Not included** (as this is a backend library):
- Web user interface
- Interactive charts (data is exported for this)
- File upload UI
- Real-time visualization

The exported data is **ready to be consumed** by any visualization library (D3.js, Chart.js, Plotly, etc.) to create the interactive charts similar to DC Rainmaker's interface.

## Use Cases

1. **Device Comparison**: Compare heart rate, power, or other metrics from multiple devices recording the same activity
2. **Data Validation**: Verify accuracy of fitness device recordings
3. **Activity Analysis**: Deep dive into training data with comprehensive statistics
4. **Data Export**: Extract data from proprietary formats for custom analysis
5. **Integration**: Use as a backend for fitness analysis applications

## Performance

- Fast file parsing with streaming support
- Efficient memory usage with lazy evaluation where possible
- Handles activities with thousands of data points
- Minimal dependencies (only essential parsing libraries)

## Error Handling

- Graceful handling of missing or corrupt files
- Clear error messages for unsupported formats
- Validation of data integrity
- Logging for debugging and monitoring
