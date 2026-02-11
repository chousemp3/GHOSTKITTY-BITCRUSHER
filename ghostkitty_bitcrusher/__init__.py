"""
GhostKitty Bitcrusher - Audio bitcrusher with real-time preview.
"""

__version__ = "2.0.0"
__author__ = "CATHOUSEMP3"

from .bitcrusher import BitCrusher
from .gui import GhostKittyGUI
from .audio_engine import AudioEngine

__all__ = ["BitCrusher", "GhostKittyGUI", "AudioEngine"]
