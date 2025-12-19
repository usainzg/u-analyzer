"""Tests for data models."""

import pytest
from datetime import datetime

from u_analyzer.models import DataPoint, ActivityData


def test_data_point_creation():
    """Test creating a DataPoint."""
    timestamp = datetime(2024, 1, 1, 10, 0, 0)
    point = DataPoint(
        timestamp=timestamp,
        latitude=40.7128,
        longitude=-74.0060,
        heart_rate=150,
        cadence=90,
        speed=5.5,
        distance=1000.0
    )
    
    assert point.timestamp == timestamp
    assert point.latitude == 40.7128
    assert point.longitude == -74.0060
    assert point.heart_rate == 150
    assert point.cadence == 90
    assert point.speed == 5.5
    assert point.distance == 1000.0


def test_data_point_optional_fields():
    """Test that optional fields default to None."""
    point = DataPoint()
    
    assert point.timestamp is None
    assert point.latitude is None
    assert point.longitude is None
    assert point.altitude is None
    assert point.heart_rate is None
    assert point.cadence is None
    assert point.speed is None
    assert point.distance is None
    assert point.power is None
    assert point.temperature is None


def test_activity_data_creation():
    """Test creating an ActivityData."""
    activity = ActivityData(name="Test Activity", source_file="test.gpx")
    
    assert activity.name == "Test Activity"
    assert activity.source_file == "test.gpx"
    assert len(activity.data_points) == 0
    assert activity.start_time is None
    assert activity.end_time is None


def test_activity_add_data_point():
    """Test adding data points to an activity."""
    activity = ActivityData(name="Test", source_file="test.gpx")
    
    point1 = DataPoint(timestamp=datetime(2024, 1, 1, 10, 0, 0), heart_rate=120)
    point2 = DataPoint(timestamp=datetime(2024, 1, 1, 10, 0, 5), heart_rate=125)
    
    activity.add_data_point(point1)
    activity.add_data_point(point2)
    
    assert len(activity.data_points) == 2
    assert activity.start_time == point1.timestamp
    assert activity.end_time == point2.timestamp


def test_activity_duration():
    """Test calculating activity duration."""
    activity = ActivityData(name="Test", source_file="test.gpx")
    
    # No data points
    assert activity.get_duration() is None
    
    # Add data points
    point1 = DataPoint(timestamp=datetime(2024, 1, 1, 10, 0, 0))
    point2 = DataPoint(timestamp=datetime(2024, 1, 1, 10, 5, 30))
    
    activity.add_data_point(point1)
    activity.add_data_point(point2)
    
    assert activity.get_duration() == 330.0  # 5 minutes 30 seconds


def test_activity_get_metric_values():
    """Test getting metric values from activity."""
    activity = ActivityData(name="Test", source_file="test.gpx")
    
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=120))
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=125))
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=130))
    
    heart_rates = activity.get_metric_values('heart_rate')
    assert heart_rates == [120, 125, 130]


def test_activity_statistics():
    """Test calculating statistics for a metric."""
    activity = ActivityData(name="Test", source_file="test.gpx")
    
    # No data points
    stats = activity.get_statistics('heart_rate')
    assert stats['min'] is None
    assert stats['max'] is None
    assert stats['avg'] is None
    assert stats['count'] == 0
    
    # Add data points with heart rate
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=120))
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=140))
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=130))
    
    stats = activity.get_statistics('heart_rate')
    assert stats['min'] == 120
    assert stats['max'] == 140
    assert stats['avg'] == 130.0
    assert stats['count'] == 3


def test_activity_statistics_with_none_values():
    """Test statistics calculation handles None values."""
    activity = ActivityData(name="Test", source_file="test.gpx")
    
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=120))
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=None))
    activity.add_data_point(DataPoint(timestamp=datetime.now(), heart_rate=140))
    
    stats = activity.get_statistics('heart_rate')
    assert stats['min'] == 120
    assert stats['max'] == 140
    assert stats['avg'] == 130.0
    assert stats['count'] == 2  # Only 2 non-None values
