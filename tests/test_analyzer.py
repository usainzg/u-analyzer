"""Tests for the main Analyzer class."""

import pytest
import tempfile
import os

from u_analyzer.analyzer import Analyzer
from tests.fixtures import create_sample_gpx_file, create_sample_tcx_file


class TestAnalyzer:
    """Tests for the Analyzer class."""
    
    def test_analyzer_initialization(self):
        """Test creating an Analyzer instance."""
        analyzer = Analyzer()
        assert analyzer is not None
        assert len(analyzer.activities) == 0
        assert len(analyzer.parsers) == 3  # FIT, GPX, TCX
    
    def test_load_single_file(self):
        """Test loading a single file."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        
        try:
            success = analyzer.load_file(gpx_file)
            assert success is True
            assert len(analyzer.activities) == 1
            
            activity = analyzer.activities[0]
            assert len(activity.data_points) == 4
        finally:
            os.unlink(gpx_file)
    
    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist."""
        analyzer = Analyzer()
        success = analyzer.load_file('/nonexistent/file.gpx')
        assert success is False
        assert len(analyzer.activities) == 0
    
    def test_load_unsupported_file(self):
        """Test loading an unsupported file type."""
        analyzer = Analyzer()
        
        # Create a text file
        fd, temp_file = tempfile.mkstemp(suffix='.txt')
        os.write(fd, b'some text content')
        os.close(fd)
        
        try:
            success = analyzer.load_file(temp_file)
            assert success is False
            assert len(analyzer.activities) == 0
        finally:
            os.unlink(temp_file)
    
    def test_load_multiple_files(self):
        """Test loading multiple files."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        tcx_file = create_sample_tcx_file()
        
        try:
            count = analyzer.load_files([gpx_file, tcx_file])
            assert count == 2
            assert len(analyzer.activities) == 2
        finally:
            os.unlink(gpx_file)
            os.unlink(tcx_file)
    
    def test_get_activities(self):
        """Test getting all activities."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        
        try:
            analyzer.load_file(gpx_file)
            activities = analyzer.get_activities()
            assert len(activities) == 1
            assert activities[0].source_file == gpx_file
        finally:
            os.unlink(gpx_file)
    
    def test_get_synchronized_data(self):
        """Test getting synchronized data."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        
        try:
            analyzer.load_file(gpx_file)
            synced_data = analyzer.get_synchronized_data()
            
            assert len(synced_data) == 1
            
            # Get the activity name (based on file name)
            activity_name = list(synced_data.keys())[0]
            data_points = synced_data[activity_name]
            
            assert len(data_points) == 4
            
            # Check first point starts at time 0
            assert data_points[0]['time'] == 0.0
            assert data_points[0]['heart_rate'] == 120
            assert data_points[0]['cadence'] == 85
            
            # Check times are relative
            assert data_points[1]['time'] == 5.0
            assert data_points[2]['time'] == 10.0
            assert data_points[3]['time'] == 15.0
        finally:
            os.unlink(gpx_file)
    
    def test_get_synchronized_data_multiple_activities(self):
        """Test synchronizing multiple activities."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        tcx_file = create_sample_tcx_file()
        
        try:
            analyzer.load_files([gpx_file, tcx_file])
            synced_data = analyzer.get_synchronized_data()
            
            assert len(synced_data) == 2
            
            # Both activities should have data
            for activity_name, data_points in synced_data.items():
                assert len(data_points) == 4
                assert data_points[0]['time'] == 0.0  # All start at 0
        finally:
            os.unlink(gpx_file)
            os.unlink(tcx_file)
    
    def test_get_statistics(self):
        """Test getting statistics."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        
        try:
            analyzer.load_file(gpx_file)
            stats = analyzer.get_statistics()
            
            assert len(stats) == 1
            
            activity_name = list(stats.keys())[0]
            activity_stats = stats[activity_name]
            
            assert activity_stats['duration'] == 15.0
            assert activity_stats['data_points'] == 4
            assert activity_stats['start_time'] is not None
            assert activity_stats['end_time'] is not None
            
            # Check heart rate statistics
            assert 'heart_rate' in activity_stats['metrics']
            hr_stats = activity_stats['metrics']['heart_rate']
            assert hr_stats['min'] == 120
            assert hr_stats['max'] == 135
            assert hr_stats['avg'] == 127.5
            assert hr_stats['count'] == 4
            
            # Check cadence statistics
            assert 'cadence' in activity_stats['metrics']
            cad_stats = activity_stats['metrics']['cadence']
            assert cad_stats['min'] == 85
            assert cad_stats['max'] == 92
        finally:
            os.unlink(gpx_file)
    
    def test_compare_activities(self):
        """Test comparing activities by metric."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        tcx_file = create_sample_tcx_file()
        
        try:
            analyzer.load_files([gpx_file, tcx_file])
            comparison = analyzer.compare_activities('heart_rate')
            
            assert len(comparison) == 2
            
            # Both activities should have heart rate data
            for activity_name, stats in comparison.items():
                assert stats['count'] == 4
                assert stats['min'] is not None
                assert stats['max'] is not None
                assert stats['avg'] is not None
        finally:
            os.unlink(gpx_file)
            os.unlink(tcx_file)
    
    def test_clear_activities(self):
        """Test clearing all activities."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        
        try:
            analyzer.load_file(gpx_file)
            assert len(analyzer.activities) == 1
            
            analyzer.clear()
            assert len(analyzer.activities) == 0
        finally:
            os.unlink(gpx_file)
    
    def test_export_to_dict(self):
        """Test exporting data to dictionary."""
        analyzer = Analyzer()
        gpx_file = create_sample_gpx_file()
        
        try:
            analyzer.load_file(gpx_file)
            export = analyzer.export_to_dict()
            
            assert 'activities' in export
            assert 'statistics' in export
            assert 'synchronized_data' in export
            
            assert len(export['activities']) == 1
            activity_export = export['activities'][0]
            
            assert activity_export['source_file'] == gpx_file
            assert activity_export['start_time'] is not None
            assert activity_export['end_time'] is not None
            assert activity_export['duration'] == 15.0
            assert activity_export['data_points_count'] == 4
        finally:
            os.unlink(gpx_file)
    
    def test_empty_analyzer_operations(self):
        """Test operations on an empty analyzer."""
        analyzer = Analyzer()
        
        # Should not crash with no activities
        synced_data = analyzer.get_synchronized_data()
        assert synced_data == {}
        
        stats = analyzer.get_statistics()
        assert stats == {}
        
        comparison = analyzer.compare_activities('heart_rate')
        assert comparison == {}
        
        export = analyzer.export_to_dict()
        assert export['activities'] == []
        assert export['statistics'] == {}
        assert export['synchronized_data'] == {}
