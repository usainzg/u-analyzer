"""Tests for file parsers."""

import pytest
import tempfile
import os
from datetime import datetime

from u_analyzer.parsers import FITParser, GPXParser, TCXParser
from tests.fixtures import create_sample_gpx_file, create_sample_tcx_file


class TestGPXParser:
    """Tests for GPX file parser."""
    
    def test_supports_file(self):
        """Test file type detection."""
        parser = GPXParser()
        assert parser.supports_file('activity.gpx') is True
        assert parser.supports_file('activity.GPX') is True
        assert parser.supports_file('activity.tcx') is False
        assert parser.supports_file('activity.fit') is False
    
    def test_parse_gpx_file(self):
        """Test parsing a GPX file."""
        parser = GPXParser()
        gpx_file = create_sample_gpx_file()
        
        try:
            activity = parser.parse(gpx_file)
            
            assert activity is not None
            assert activity.name == os.path.splitext(os.path.basename(gpx_file))[0]
            assert activity.source_file == gpx_file
            assert len(activity.data_points) == 4
            
            # Check first data point
            first_point = activity.data_points[0]
            assert first_point.latitude == pytest.approx(40.7128, abs=0.0001)
            assert first_point.longitude == pytest.approx(-74.0060, abs=0.0001)
            assert first_point.altitude == 10.0
            assert first_point.heart_rate == 120
            assert first_point.cadence == 85
            
            # Check duration
            duration = activity.get_duration()
            assert duration == 15.0  # 15 seconds from first to last point
            
        finally:
            os.unlink(gpx_file)
    
    def test_parse_nonexistent_file(self):
        """Test parsing a file that doesn't exist."""
        parser = GPXParser()
        activity = parser.parse('/nonexistent/file.gpx')
        assert activity is None
    
    def test_parse_invalid_gpx(self):
        """Test parsing an invalid GPX file."""
        parser = GPXParser()
        
        # Create invalid GPX file
        fd, temp_file = tempfile.mkstemp(suffix='.gpx')
        os.write(fd, b'invalid gpx content')
        os.close(fd)
        
        try:
            activity = parser.parse(temp_file)
            assert activity is None
        finally:
            os.unlink(temp_file)


class TestTCXParser:
    """Tests for TCX file parser."""
    
    def test_supports_file(self):
        """Test file type detection."""
        parser = TCXParser()
        assert parser.supports_file('activity.tcx') is True
        assert parser.supports_file('activity.TCX') is True
        assert parser.supports_file('activity.gpx') is False
        assert parser.supports_file('activity.fit') is False
    
    def test_parse_tcx_file(self):
        """Test parsing a TCX file."""
        parser = TCXParser()
        tcx_file = create_sample_tcx_file()
        
        try:
            activity = parser.parse(tcx_file)
            
            assert activity is not None
            assert activity.name == os.path.splitext(os.path.basename(tcx_file))[0]
            assert activity.source_file == tcx_file
            assert len(activity.data_points) == 4
            
            # Check first data point
            first_point = activity.data_points[0]
            assert first_point.latitude == pytest.approx(40.7128, abs=0.0001)
            assert first_point.longitude == pytest.approx(-74.0060, abs=0.0001)
            assert first_point.altitude == 10.0
            assert first_point.distance == 0.0
            assert first_point.heart_rate == 140
            assert first_point.cadence == 80
            
            # Check duration
            duration = activity.get_duration()
            assert duration == 15.0
            
        finally:
            os.unlink(tcx_file)
    
    def test_parse_nonexistent_file(self):
        """Test parsing a file that doesn't exist."""
        parser = TCXParser()
        activity = parser.parse('/nonexistent/file.tcx')
        assert activity is None
    
    def test_parse_invalid_tcx(self):
        """Test parsing an invalid TCX file."""
        parser = TCXParser()
        
        # Create invalid TCX file
        fd, temp_file = tempfile.mkstemp(suffix='.tcx')
        os.write(fd, b'invalid tcx content')
        os.close(fd)
        
        try:
            activity = parser.parse(temp_file)
            assert activity is None
        finally:
            os.unlink(temp_file)


class TestFITParser:
    """Tests for FIT file parser."""
    
    def test_supports_file(self):
        """Test file type detection."""
        parser = FITParser()
        assert parser.supports_file('activity.fit') is True
        assert parser.supports_file('activity.FIT') is True
        assert parser.supports_file('activity.gpx') is False
        assert parser.supports_file('activity.tcx') is False
    
    def test_parse_without_fitparse_library(self):
        """Test that parser handles missing fitparse library gracefully."""
        parser = FITParser()
        
        # Create a dummy FIT file
        fd, temp_file = tempfile.mkstemp(suffix='.fit')
        os.write(fd, b'dummy fit content')
        os.close(fd)
        
        try:
            # This will fail because fitparse might not be installed
            # or the file is not a valid FIT file
            activity = parser.parse(temp_file)
            # We expect None if library is missing or file is invalid
            assert activity is None or isinstance(activity, type(None))
        finally:
            os.unlink(temp_file)
