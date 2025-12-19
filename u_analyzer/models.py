"""Data models for fitness activity data."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class DataPoint:
    """Represents a single data point in time during an activity."""
    
    timestamp: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    heart_rate: Optional[int] = None
    cadence: Optional[int] = None
    speed: Optional[float] = None
    distance: Optional[float] = None
    power: Optional[int] = None
    temperature: Optional[float] = None


@dataclass
class ActivityData:
    """Represents an entire activity with multiple data points."""
    
    name: str
    source_file: str
    data_points: List[DataPoint] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def add_data_point(self, point: DataPoint):
        """Add a data point to the activity."""
        self.data_points.append(point)
        
        # Update start and end times
        if self.start_time is None or point.timestamp < self.start_time:
            self.start_time = point.timestamp
        if self.end_time is None or point.timestamp > self.end_time:
            self.end_time = point.timestamp
    
    def get_duration(self) -> Optional[float]:
        """Get activity duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    def get_metric_values(self, metric: str) -> List[Optional[float]]:
        """Get all values for a specific metric."""
        return [getattr(point, metric) for point in self.data_points]
    
    def get_statistics(self, metric: str) -> dict:
        """Calculate statistics for a given metric."""
        values = [v for v in self.get_metric_values(metric) if v is not None]
        
        if not values:
            return {
                'min': None,
                'max': None,
                'avg': None,
                'count': 0
            }
        
        return {
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'count': len(values)
        }
