"""
GhostKitty Bitcrusher - Epic Audio Destruction Tool 👻⚡

Main entry point for the application.
Run this file to launch the cyberpunk GUI!
"""

import sys
import os

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghostkitty_bitcrusher import GhostKittyGUI


def main():
    """
    Launch the GhostKitty Bitcrusher application
    """
    print("🚀 Starting GhostKitty Bitcrusher...")
    print("👻 Preparing for epic audio destruction! ⚡")
    
    try:
        # Create and run the GUI
        app = GhostKittyGUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👻 GhostKitty Bitcrusher shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💀 Something went wrong! Check your audio setup.")
        print("Make sure all dependencies are installed:")
        print("pip install numpy scipy pygame customtkinter Pillow soundfile matplotlib")
        return 1
    finally:
        print("🔥 Thanks for using GhostKitty Bitcrusher! 🔥")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
