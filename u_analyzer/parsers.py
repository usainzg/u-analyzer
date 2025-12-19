"""File parsers for different fitness data formats."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import logging

from .models import ActivityData, DataPoint

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Base class for all file format parsers."""
    
    @abstractmethod
    def parse(self, file_path: str) -> Optional[ActivityData]:
        """Parse a file and return ActivityData."""
        pass
    
    @abstractmethod
    def supports_file(self, file_path: str) -> bool:
        """Check if this parser supports the given file."""
        pass


class FITParser(BaseParser):
    """Parser for FIT (Flexible and Interoperable Data Transfer) files."""
    
    def supports_file(self, file_path: str) -> bool:
        """Check if file is a FIT file."""
        return file_path.lower().endswith('.fit')
    
    def parse(self, file_path: str) -> Optional[ActivityData]:
        """Parse a FIT file."""
        try:
            from fitparse import FitFile
        except ImportError:
            logger.error("fitparse library not installed. Run: pip install fitparse")
            return None
        
        try:
            fitfile = FitFile(file_path)
            activity = ActivityData(
                name=Path(file_path).stem,
                source_file=file_path
            )
            
            for record in fitfile.get_messages('record'):
                point = DataPoint()
                
                for field in record:
                    if field.name == 'timestamp':
                        point.timestamp = field.value
                    elif field.name == 'position_lat':
                        # Convert semicircles to degrees
                        point.latitude = field.value * (180.0 / 2**31) if field.value else None
                    elif field.name == 'position_long':
                        point.longitude = field.value * (180.0 / 2**31) if field.value else None
                    elif field.name == 'altitude':
                        point.altitude = field.value
                    elif field.name == 'heart_rate':
                        point.heart_rate = field.value
                    elif field.name == 'cadence':
                        point.cadence = field.value
                    elif field.name == 'speed':
                        point.speed = field.value
                    elif field.name == 'distance':
                        point.distance = field.value
                    elif field.name == 'power':
                        point.power = field.value
                    elif field.name == 'temperature':
                        point.temperature = field.value
                
                if point.timestamp:
                    activity.add_data_point(point)
            
            return activity if activity.data_points else None
            
        except Exception as e:
            logger.error(f"Error parsing FIT file {file_path}: {e}")
            return None


class GPXParser(BaseParser):
    """Parser for GPX (GPS Exchange Format) files."""
    
    def supports_file(self, file_path: str) -> bool:
        """Check if file is a GPX file."""
        return file_path.lower().endswith('.gpx')
    
    def parse(self, file_path: str) -> Optional[ActivityData]:
        """Parse a GPX file."""
        try:
            import gpxpy
            from lxml import etree
        except ImportError:
            logger.error("gpxpy or lxml library not installed. Run: pip install gpxpy lxml")
            return None
        
        try:
            # Parse the GPX file with lxml to get extensions
            tree = etree.parse(file_path)
            root = tree.getroot()
            
            # Get namespace
            ns = {'gpxtpx': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'}
            
            activity = ActivityData(
                name=Path(file_path).stem,
                source_file=file_path
            )
            
            # Also parse with gpxpy for basic data
            with open(file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
            
            # Build a mapping of trackpoints with extensions (no namespace for gpx elements in our test files)
            trkpts = root.xpath('.//trkpt')
            
            point_index = 0
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        data_point = DataPoint(
                            timestamp=point.time,
                            latitude=point.latitude,
                            longitude=point.longitude,
                            altitude=point.elevation
                        )
                        
                        # Try to extract heart rate and cadence from XML extensions
                        if point_index < len(trkpts):
                            trkpt = trkpts[point_index]
                            
                            # Extract heart rate
                            hr_elem = trkpt.find('.//gpxtpx:hr', ns)
                            if hr_elem is not None and hr_elem.text:
                                try:
                                    data_point.heart_rate = int(hr_elem.text)
                                except (ValueError, AttributeError):
                                    pass
                            
                            # Extract cadence
                            cad_elem = trkpt.find('.//gpxtpx:cad', ns)
                            if cad_elem is not None and cad_elem.text:
                                try:
                                    data_point.cadence = int(cad_elem.text)
                                except (ValueError, AttributeError):
                                    pass
                        
                        point_index += 1
                        
                        if data_point.timestamp:
                            activity.add_data_point(data_point)
            
            return activity if activity.data_points else None
            
        except Exception as e:
            logger.error(f"Error parsing GPX file {file_path}: {e}")
            return None


class TCXParser(BaseParser):
    """Parser for TCX (Training Center XML) files."""
    
    def supports_file(self, file_path: str) -> bool:
        """Check if file is a TCX file."""
        return file_path.lower().endswith('.tcx')
    
    def parse(self, file_path: str) -> Optional[ActivityData]:
        """Parse a TCX file."""
        try:
            from lxml import etree
            from dateutil import parser as date_parser
        except ImportError:
            logger.error("lxml or dateutil not installed. Run: pip install lxml python-dateutil")
            return None
        
        try:
            tree = etree.parse(file_path)
            root = tree.getroot()
            
            # Handle XML namespace
            ns = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
            
            activity = ActivityData(
                name=Path(file_path).stem,
                source_file=file_path
            )
            
            # Find all trackpoints
            for trackpoint in root.xpath('//tcx:Trackpoint', namespaces=ns):
                point = DataPoint()
                
                # Time
                time_elem = trackpoint.find('tcx:Time', ns)
                if time_elem is not None and time_elem.text:
                    point.timestamp = date_parser.parse(time_elem.text)
                
                # Position
                position = trackpoint.find('tcx:Position', ns)
                if position is not None:
                    lat_elem = position.find('tcx:LatitudeDegrees', ns)
                    lon_elem = position.find('tcx:LongitudeDegrees', ns)
                    if lat_elem is not None and lat_elem.text:
                        point.latitude = float(lat_elem.text)
                    if lon_elem is not None and lon_elem.text:
                        point.longitude = float(lon_elem.text)
                
                # Altitude
                alt_elem = trackpoint.find('tcx:AltitudeMeters', ns)
                if alt_elem is not None and alt_elem.text:
                    point.altitude = float(alt_elem.text)
                
                # Heart Rate
                hr_elem = trackpoint.find('.//tcx:HeartRateBpm/tcx:Value', ns)
                if hr_elem is not None and hr_elem.text:
                    point.heart_rate = int(hr_elem.text)
                
                # Cadence
                cad_elem = trackpoint.find('tcx:Cadence', ns)
                if cad_elem is not None and cad_elem.text:
                    point.cadence = int(cad_elem.text)
                
                # Distance
                dist_elem = trackpoint.find('tcx:DistanceMeters', ns)
                if dist_elem is not None and dist_elem.text:
                    point.distance = float(dist_elem.text)
                
                # Speed (in Extensions)
                speed_elem = trackpoint.find('.//tcx:Speed', ns)
                if speed_elem is not None and speed_elem.text:
                    point.speed = float(speed_elem.text)
                
                # Power (in Extensions)
                power_elem = trackpoint.find('.//tcx:Watts', ns)
                if power_elem is not None and power_elem.text:
                    point.power = int(power_elem.text)
                
                if point.timestamp:
                    activity.add_data_point(point)
            
            return activity if activity.data_points else None
            
        except Exception as e:
            logger.error(f"Error parsing TCX file {file_path}: {e}")
            return None
