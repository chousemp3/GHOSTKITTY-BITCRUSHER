"""
GhostKitty Bitcrusher - Audio Bitcrushing Tool

Main entry point for the application.
"""

import sys
import os

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghostkitty_bitcrusher import GhostKittyGUI


def main():
    """Launch the GhostKitty Bitcrusher application."""
    print("Starting GhostKitty Bitcrusher...")

    try:
        app = GhostKittyGUI()
        app.run()

    except KeyboardInterrupt:
        print("\nGhostKitty Bitcrusher shutting down.")
    except Exception as e:
        print(f"Error: {e}")
        print("Check your audio setup and ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
