#!/usr/bin/env python
"""
Example usage of u-analyzer.

This script demonstrates how to use the analyzer to load, parse,
and analyze fitness data files.
"""

import json
from u_analyzer import Analyzer


def main():
    """Demonstrate basic analyzer usage."""
    # Create analyzer instance
    analyzer = Analyzer()
    
    print("U-Analyzer Example")
    print("=" * 50)
    print()
    
    # Example 1: Load a single file
    print("Example 1: Loading files")
    print("-" * 50)
    
    # In real usage, you would provide actual file paths
    # analyzer.load_file('path/to/activity1.gpx')
    # analyzer.load_file('path/to/activity2.tcx')
    # analyzer.load_file('path/to/activity3.fit')
    
    # For demonstration, we'll show what the API looks like
    print("API: analyzer.load_file('activity.gpx')")
    print("API: analyzer.load_file('activity.tcx')")
    print()
    
    # Example 2: Get statistics
    print("Example 2: Getting statistics")
    print("-" * 50)
    print("API: stats = analyzer.get_statistics()")
    print()
    print("Returns statistics for each activity:")
    print("{")
    print("  'activity_name': {")
    print("    'duration': 3600.0,  # seconds")
    print("    'data_points': 1200,")
    print("    'start_time': datetime(...),")
    print("    'end_time': datetime(...),")
    print("    'metrics': {")
    print("      'heart_rate': {")
    print("        'min': 110,")
    print("        'max': 175,")
    print("        'avg': 145.5,")
    print("        'count': 1200")
    print("      },")
    print("      'speed': {...},")
    print("      'cadence': {...}")
    print("    }")
    print("  }")
    print("}")
    print()
    
    # Example 3: Get synchronized data
    print("Example 3: Getting synchronized data")
    print("-" * 50)
    print("API: synced = analyzer.get_synchronized_data()")
    print()
    print("Returns time-aligned data from all activities:")
    print("{")
    print("  'activity1': [")
    print("    {")
    print("      'time': 0.0,  # relative time in seconds")
    print("      'timestamp': datetime(...),")
    print("      'heart_rate': 120,")
    print("      'speed': 5.5,")
    print("      'latitude': 40.7128,")
    print("      'longitude': -74.0060,")
    print("      '...'")
    print("    },")
    print("    {...}")
    print("  ],")
    print("  'activity2': [...]")
    print("}")
    print()
    
    # Example 4: Compare activities
    print("Example 4: Comparing activities by metric")
    print("-" * 50)
    print("API: comparison = analyzer.compare_activities('heart_rate')")
    print()
    print("Returns comparison data for a specific metric:")
    print("{")
    print("  'activity1': {")
    print("    'min': 110,")
    print("    'max': 175,")
    print("    'avg': 145.5,")
    print("    'count': 1200")
    print("  },")
    print("  'activity2': {")
    print("    'min': 105,")
    print("    'max': 170,")
    print("    'avg': 142.3,")
    print("    'count': 1150")
    print("  }")
    print("}")
    print()
    
    # Example 5: Export data
    print("Example 5: Exporting all data")
    print("-" * 50)
    print("API: data = analyzer.export_to_dict()")
    print()
    print("Returns all analyzer data in a dictionary format")
    print("suitable for JSON serialization and visualization.")
    print()
    
    print("=" * 50)
    print("For actual usage, provide real fitness data files!")
    print()
    print("Supported formats:")
    print("  - FIT: Garmin, Wahoo, and other devices")
    print("  - GPX: GPS Exchange Format")
    print("  - TCX: Training Center XML")


if __name__ == "__main__":
    main()
