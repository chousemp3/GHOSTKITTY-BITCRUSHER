"""
🐱💀 GhostKitty Bitcrusher 💀🐱
Epic cyberpunk audio bitcrusher with real-time preview
"""

__version__ = "1.0.0"
__author__ = "GhostKitty"
__email__ = "ghostkitty@example.com"

from .bitcrusher import BitCrusher
from .gui import GhostKittyGUI
from .audio_engine import AudioEngine

__all__ = ["BitCrusher", "GhostKittyGUI", "AudioEngine"]
