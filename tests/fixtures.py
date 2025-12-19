"""Test fixtures and sample data generators."""

from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import os


def create_sample_gpx_file(output_path: str = None) -> str:
    """Create a sample GPX file for testing."""
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix='.gpx')
        os.close(fd)
    
    gpx_content = '''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="U-Analyzer Test">
  <trk>
    <name>Test Activity</name>
    <trkseg>
      <trkpt lat="40.7128" lon="-74.0060">
        <ele>10.0</ele>
        <time>2024-01-01T10:00:00Z</time>
        <extensions>
          <gpxtpx:TrackPointExtension xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1">
            <gpxtpx:hr>120</gpxtpx:hr>
            <gpxtpx:cad>85</gpxtpx:cad>
          </gpxtpx:TrackPointExtension>
        </extensions>
      </trkpt>
      <trkpt lat="40.7138" lon="-74.0050">
        <ele>12.0</ele>
        <time>2024-01-01T10:00:05Z</time>
        <extensions>
          <gpxtpx:TrackPointExtension xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1">
            <gpxtpx:hr>125</gpxtpx:hr>
            <gpxtpx:cad>87</gpxtpx:cad>
          </gpxtpx:TrackPointExtension>
        </extensions>
      </trkpt>
      <trkpt lat="40.7148" lon="-74.0040">
        <ele>15.0</ele>
        <time>2024-01-01T10:00:10Z</time>
        <extensions>
          <gpxtpx:TrackPointExtension xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1">
            <gpxtpx:hr>130</gpxtpx:hr>
            <gpxtpx:cad>90</gpxtpx:cad>
          </gpxtpx:TrackPointExtension>
        </extensions>
      </trkpt>
      <trkpt lat="40.7158" lon="-74.0030">
        <ele>18.0</ele>
        <time>2024-01-01T10:00:15Z</time>
        <extensions>
          <gpxtpx:TrackPointExtension xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1">
            <gpxtpx:hr>135</gpxtpx:hr>
            <gpxtpx:cad>92</gpxtpx:cad>
          </gpxtpx:TrackPointExtension>
        </extensions>
      </trkpt>
    </trkseg>
  </trk>
</gpx>'''
    
    with open(output_path, 'w') as f:
        f.write(gpx_content)
    
    return output_path


def create_sample_tcx_file(output_path: str = None) -> str:
    """Create a sample TCX file for testing."""
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix='.tcx')
        os.close(fd)
    
    tcx_content = '''<?xml version="1.0" encoding="UTF-8"?>
<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2">
  <Activities>
    <Activity Sport="Running">
      <Id>2024-01-01T10:00:00Z</Id>
      <Lap StartTime="2024-01-01T10:00:00Z">
        <Track>
          <Trackpoint>
            <Time>2024-01-01T10:00:00Z</Time>
            <Position>
              <LatitudeDegrees>40.7128</LatitudeDegrees>
              <LongitudeDegrees>-74.0060</LongitudeDegrees>
            </Position>
            <AltitudeMeters>10.0</AltitudeMeters>
            <DistanceMeters>0.0</DistanceMeters>
            <HeartRateBpm>
              <Value>140</Value>
            </HeartRateBpm>
            <Cadence>80</Cadence>
          </Trackpoint>
          <Trackpoint>
            <Time>2024-01-01T10:00:05Z</Time>
            <Position>
              <LatitudeDegrees>40.7138</LatitudeDegrees>
              <LongitudeDegrees>-74.0050</LongitudeDegrees>
            </Position>
            <AltitudeMeters>12.0</AltitudeMeters>
            <DistanceMeters>100.0</DistanceMeters>
            <HeartRateBpm>
              <Value>145</Value>
            </HeartRateBpm>
            <Cadence>82</Cadence>
          </Trackpoint>
          <Trackpoint>
            <Time>2024-01-01T10:00:10Z</Time>
            <Position>
              <LatitudeDegrees>40.7148</LatitudeDegrees>
              <LongitudeDegrees>-74.0040</LongitudeDegrees>
            </Position>
            <AltitudeMeters>15.0</AltitudeMeters>
            <DistanceMeters>200.0</DistanceMeters>
            <HeartRateBpm>
              <Value>150</Value>
            </HeartRateBpm>
            <Cadence>85</Cadence>
          </Trackpoint>
          <Trackpoint>
            <Time>2024-01-01T10:00:15Z</Time>
            <Position>
              <LatitudeDegrees>40.7158</LatitudeDegrees>
              <LongitudeDegrees>-74.0030</LongitudeDegrees>
            </Position>
            <AltitudeMeters>18.0</AltitudeMeters>
            <DistanceMeters>300.0</DistanceMeters>
            <HeartRateBpm>
              <Value>155</Value>
            </HeartRateBpm>
            <Cadence>88</Cadence>
          </Trackpoint>
        </Track>
      </Lap>
    </Activity>
  </Activities>
</TrainingCenterDatabase>'''
    
    with open(output_path, 'w') as f:
        f.write(tcx_content)
    
    return output_path


def create_sample_fit_file(output_path: str = None) -> str:
    """
    Create a sample FIT file for testing.
    Note: This is a simplified version. In reality, FIT files are binary.
    For actual testing, we'll need the fitparse library to create real FIT files.
    """
    # FIT files are binary and complex to generate without proper tools
    # For now, we'll return None and handle this in tests
    return None
