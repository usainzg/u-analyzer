"""U-Analyzer: A fitness data analyzer for comparing and analyzing workout data."""

from .analyzer import Analyzer
from .parsers import FITParser, GPXParser, TCXParser
from .models import ActivityData, DataPoint

__version__ = "0.1.0"
__all__ = ["Analyzer", "FITParser", "GPXParser", "TCXParser", "ActivityData", "DataPoint"]
