"""Main analyzer class for comparing and analyzing fitness data."""

from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime, timedelta
import logging

from .models import ActivityData, DataPoint
from .parsers import FITParser, GPXParser, TCXParser, BaseParser

logger = logging.getLogger(__name__)


class Analyzer:
    """Main analyzer class for loading and comparing fitness activity data."""
    
    def __init__(self):
        """Initialize the analyzer with available parsers."""
        self.activities: List[ActivityData] = []
        self.parsers: List[BaseParser] = [
            FITParser(),
            GPXParser(),
            TCXParser()
        ]
    
    def load_file(self, file_path: str) -> bool:
        """
        Load a fitness data file.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            True if file was successfully loaded, False otherwise
        """
        if not Path(file_path).exists():
            logger.error(f"File not found: {file_path}")
            return False
        
        # Find appropriate parser
        for parser in self.parsers:
            if parser.supports_file(file_path):
                activity = parser.parse(file_path)
                if activity:
                    self.activities.append(activity)
                    logger.info(f"Successfully loaded {file_path} with {len(activity.data_points)} data points")
                    return True
                else:
                    logger.error(f"Failed to parse {file_path}")
                    return False
        
        logger.error(f"No parser found for file: {file_path}")
        return False
    
    def load_files(self, file_paths: List[str]) -> int:
        """
        Load multiple fitness data files.
        
        Args:
            file_paths: List of file paths to load
            
        Returns:
            Number of successfully loaded files
        """
        count = 0
        for file_path in file_paths:
            if self.load_file(file_path):
                count += 1
        return count
    
    def get_activities(self) -> List[ActivityData]:
        """Get all loaded activities."""
        return self.activities
    
    def get_synchronized_data(self) -> Dict[str, List[Dict]]:
        """
        Get synchronized data from all activities.
        
        Aligns all activities by their relative timestamps, starting from 0.
        
        Returns:
            Dictionary mapping activity names to lists of synchronized data points
        """
        if not self.activities:
            return {}
        
        result = {}
        
        for activity in self.activities:
            if not activity.data_points or not activity.start_time:
                continue
            
            synced_points = []
            for point in activity.data_points:
                relative_time = (point.timestamp - activity.start_time).total_seconds()
                synced_points.append({
                    'time': relative_time,
                    'timestamp': point.timestamp,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'altitude': point.altitude,
                    'heart_rate': point.heart_rate,
                    'cadence': point.cadence,
                    'speed': point.speed,
                    'distance': point.distance,
                    'power': point.power,
                    'temperature': point.temperature
                })
            
            result[activity.name] = synced_points
        
        return result
    
    def get_statistics(self) -> Dict[str, Dict]:
        """
        Get statistics for all loaded activities.
        
        Returns:
            Dictionary mapping activity names to their statistics
        """
        result = {}
        
        metrics = ['heart_rate', 'cadence', 'speed', 'distance', 'power', 'altitude', 'temperature']
        
        for activity in self.activities:
            activity_stats = {
                'duration': activity.get_duration(),
                'data_points': len(activity.data_points),
                'start_time': activity.start_time,
                'end_time': activity.end_time,
                'metrics': {}
            }
            
            for metric in metrics:
                stats = activity.get_statistics(metric)
                if stats['count'] > 0:
                    activity_stats['metrics'][metric] = stats
            
            result[activity.name] = activity_stats
        
        return result
    
    def compare_activities(self, metric: str) -> Dict[str, Dict]:
        """
        Compare a specific metric across all activities.
        
        Args:
            metric: The metric to compare (e.g., 'heart_rate', 'speed', 'power')
            
        Returns:
            Dictionary with comparison data
        """
        comparison = {}
        
        for activity in self.activities:
            stats = activity.get_statistics(metric)
            if stats['count'] > 0:
                comparison[activity.name] = stats
        
        return comparison
    
    def clear(self):
        """Clear all loaded activities."""
        self.activities.clear()
    
    def export_to_dict(self) -> Dict:
        """
        Export all data to a dictionary format suitable for JSON serialization.
        
        Returns:
            Dictionary containing all analyzer data
        """
        return {
            'activities': [
                {
                    'name': activity.name,
                    'source_file': activity.source_file,
                    'start_time': activity.start_time.isoformat() if activity.start_time else None,
                    'end_time': activity.end_time.isoformat() if activity.end_time else None,
                    'duration': activity.get_duration(),
                    'data_points_count': len(activity.data_points)
                }
                for activity in self.activities
            ],
            'statistics': self.get_statistics(),
            'synchronized_data': self.get_synchronized_data()
        }
