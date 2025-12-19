"""Integration tests for the analyzer workflow."""

import pytest
import os
import json

from u_analyzer import Analyzer
from tests.fixtures import create_sample_gpx_file, create_sample_tcx_file


@pytest.mark.integration
def test_complete_analyzer_workflow():
    """Test a complete workflow of loading, analyzing, and comparing activities."""
    # Create sample files
    gpx_file = create_sample_gpx_file()
    tcx_file = create_sample_tcx_file()
    
    try:
        # Initialize analyzer
        analyzer = Analyzer()
        
        # Load files
        loaded_count = analyzer.load_files([gpx_file, tcx_file])
        assert loaded_count == 2, "Should load both files successfully"
        
        # Get activities
        activities = analyzer.get_activities()
        assert len(activities) == 2, "Should have 2 activities"
        
        # Each activity should have data points
        for activity in activities:
            assert len(activity.data_points) > 0, "Activity should have data points"
            assert activity.start_time is not None, "Activity should have start time"
            assert activity.end_time is not None, "Activity should have end time"
            duration = activity.get_duration()
            assert duration is not None and duration > 0, "Activity should have positive duration"
        
        # Get synchronized data
        synced_data = analyzer.get_synchronized_data()
        assert len(synced_data) == 2, "Should have synced data for both activities"
        
        for activity_name, data_points in synced_data.items():
            assert len(data_points) > 0, f"{activity_name} should have synced data points"
            # First point should start at time 0
            assert data_points[0]['time'] == 0.0, "First point should be at time 0"
            # Should have timestamp
            assert data_points[0]['timestamp'] is not None, "Should have timestamp"
        
        # Get statistics
        stats = analyzer.get_statistics()
        assert len(stats) == 2, "Should have stats for both activities"
        
        for activity_name, activity_stats in stats.items():
            assert 'duration' in activity_stats, "Should have duration"
            assert 'data_points' in activity_stats, "Should have data points count"
            assert 'metrics' in activity_stats, "Should have metrics"
            assert activity_stats['data_points'] > 0, "Should have positive data points count"
        
        # Compare activities by heart rate
        hr_comparison = analyzer.compare_activities('heart_rate')
        # At least one activity should have heart rate data
        assert len(hr_comparison) >= 1, "Should have heart rate comparison data"
        
        for activity_name, hr_stats in hr_comparison.items():
            assert 'min' in hr_stats, "Should have min heart rate"
            assert 'max' in hr_stats, "Should have max heart rate"
            assert 'avg' in hr_stats, "Should have avg heart rate"
            assert 'count' in hr_stats, "Should have count"
            assert hr_stats['min'] <= hr_stats['avg'] <= hr_stats['max'], \
                "Min <= Avg <= Max for heart rate"
        
        # Export to dict
        export_data = analyzer.export_to_dict()
        assert 'activities' in export_data, "Export should contain activities"
        assert 'statistics' in export_data, "Export should contain statistics"
        assert 'synchronized_data' in export_data, "Export should contain synchronized data"
        assert len(export_data['activities']) == 2, "Should export 2 activities"
        
        # Verify export data is JSON serializable
        json_str = json.dumps(export_data, default=str)
        assert len(json_str) > 0, "Should be able to serialize to JSON"
        
        # Clear and verify
        analyzer.clear()
        assert len(analyzer.get_activities()) == 0, "Should have no activities after clear"
        
    finally:
        # Cleanup
        os.unlink(gpx_file)
        os.unlink(tcx_file)


@pytest.mark.integration
def test_multiple_activities_comparison():
    """Test comparing multiple activities with different metrics."""
    gpx_file = create_sample_gpx_file()
    tcx_file = create_sample_tcx_file()
    
    try:
        analyzer = Analyzer()
        analyzer.load_files([gpx_file, tcx_file])
        
        # Test various metric comparisons
        metrics_to_test = ['heart_rate', 'cadence', 'altitude', 'distance']
        
        for metric in metrics_to_test:
            comparison = analyzer.compare_activities(metric)
            # At least some activities should have data for common metrics
            if len(comparison) > 0:
                for activity_name, stats in comparison.items():
                    assert stats['count'] > 0, f"Should have {metric} data"
                    if stats['min'] is not None and stats['max'] is not None:
                        assert stats['min'] <= stats['max'], \
                            f"Min should be <= Max for {metric}"
    
    finally:
        os.unlink(gpx_file)
        os.unlink(tcx_file)


@pytest.mark.integration
def test_analyzer_with_real_world_scenario():
    """Test analyzer with a scenario similar to DC Rainmaker analyzer usage."""
    # Scenario: User uploads two files from different devices recording the same activity
    # and wants to compare heart rate data
    
    gpx_file = create_sample_gpx_file()
    tcx_file = create_sample_tcx_file()
    
    try:
        analyzer = Analyzer()
        
        # Step 1: Load files
        success1 = analyzer.load_file(gpx_file)
        success2 = analyzer.load_file(tcx_file)
        
        assert success1 and success2, "Both files should load successfully"
        
        # Step 2: Verify data is synchronized
        synced_data = analyzer.get_synchronized_data()
        assert len(synced_data) == 2, "Should have synced data from both devices"
        
        # Step 3: Compare heart rate across devices
        hr_comparison = analyzer.compare_activities('heart_rate')
        
        # Both files have HR data, so we should get comparison
        if len(hr_comparison) == 2:
            # Get the two activities
            activities = list(hr_comparison.keys())
            activity1_hr = hr_comparison[activities[0]]
            activity2_hr = hr_comparison[activities[1]]
            
            # Both should have valid heart rate data
            assert activity1_hr['count'] > 0, "Activity 1 should have HR data"
            assert activity2_hr['count'] > 0, "Activity 2 should have HR data"
            
            # Heart rates should be in reasonable range (e.g., 40-220 bpm)
            for hr_data in [activity1_hr, activity2_hr]:
                assert 40 <= hr_data['min'] <= 220, "Min HR should be in reasonable range"
                assert 40 <= hr_data['max'] <= 220, "Max HR should be in reasonable range"
                assert 40 <= hr_data['avg'] <= 220, "Avg HR should be in reasonable range"
        
        # Step 4: Get detailed statistics
        stats = analyzer.get_statistics()
        
        for activity_name, activity_stats in stats.items():
            # Each activity should have a duration
            assert activity_stats['duration'] > 0, f"{activity_name} should have positive duration"
            
            # Should have multiple data points
            assert activity_stats['data_points'] >= 4, \
                f"{activity_name} should have multiple data points"
        
        # Step 5: Export for visualization
        export = analyzer.export_to_dict()
        
        # Export should be complete and ready for use in a web interface
        assert len(export['activities']) == 2
        assert len(export['synchronized_data']) == 2
        
        # Verify synchronized data has timestamps for charting
        for activity_name, points in export['synchronized_data'].items():
            for point in points:
                assert 'time' in point, "Each point should have relative time"
                assert 'timestamp' in point, "Each point should have absolute timestamp"
    
    finally:
        os.unlink(gpx_file)
        os.unlink(tcx_file)
