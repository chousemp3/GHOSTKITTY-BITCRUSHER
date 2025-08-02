"""
Simple and Fast Audio Engine
No lag, no bugs - just pure audio destruction! ⚡
"""

import numpy as np
import soundfile as sf
import pygame
from typing import Optional, Dict, Any
from .bitcrusher import BitCrusher


class AudioEngine:
    """
    Simple and fast audio engine - no complex threading
    """
    
    def __init__(self):
        self.sample_rate = 44100
        self.channels = 2
        
        # Simple pygame setup
        pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=self.channels, buffer=512)
        
        self.bitcrusher = BitCrusher()
        self.current_audio = None
        self.processed_audio = None
        self.is_playing = False
        
        # Simple processing parameters
        self.processing_params = {
            "bit_depth": 8,
            "downsample_factor": 1.0,
            "mix": 1.0,
            "waveshape": 0.0,
            "noise": 0.0
        }
        
        # Dummy callbacks for compatibility
        self.level_callback = None
        self.progress_callback = None
        self.waveform_callback = None
    
    def load_audio_file(self, filename: str) -> bool:
        """Load audio file - simple and fast"""
        try:
            print(f"🎵 Loading audio file: {filename}")
            
            # Load audio with soundfile
            audio_data, sample_rate = sf.read(filename, dtype=np.float32)
            
            # Handle mono files
            if len(audio_data.shape) == 1:
                audio_data = np.column_stack((audio_data, audio_data))
            
            # Store original audio
            self.current_audio = audio_data
            self.sample_rate = sample_rate
            
            print(f"✅ Audio loaded: {audio_data.shape[0]/sample_rate:.1f}s, {audio_data.shape[1]}ch")
            
            # Process audio immediately
            self._process_audio()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load audio: {e}")
            return False
    
    def _process_audio(self):
        """Process the full audio with current parameters"""
        if self.current_audio is None:
            return
        
        print("🔧 Processing audio...")
        
        # Process the audio
        self.processed_audio = self.bitcrusher.process_audio(
            self.current_audio.copy(),
            **self.processing_params
        )
        
        print("✅ Audio processing complete!")
    
    def start_playback(self) -> bool:
        """Start audio playback"""
        if self.processed_audio is None:
            print("❌ No processed audio to play")
            return False
        
        try:
            # Stop any current playback
            pygame.mixer.stop()
            
            # Convert to pygame format
            audio_int = (self.processed_audio * 32767).astype(np.int16)
            
            # Create pygame sound
            sound = pygame.sndarray.make_sound(audio_int)
            
            # Play the sound
            sound.play()
            self.is_playing = True
            
            print("🎵 Playback started!")
            return True
            
        except Exception as e:
            print(f"❌ Playback failed: {e}")
            return False
    
    def stop_playback(self):
        """Stop audio playback"""
        pygame.mixer.stop()
        self.is_playing = False
        print("⏹ Playback stopped")
    
    def update_processing_params(self, **params):
        """Update processing parameters and reprocess audio"""
        # Update parameters
        self.processing_params.update(params)
        
        # Reprocess audio if loaded
        if self.current_audio is not None:
            self._process_audio()
            
            # If currently playing, restart playback with new processing
            if self.is_playing:
                self.start_playback()
    
    def get_audio_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the loaded audio"""
        if self.current_audio is None:
            return None
        
        return {
            "duration": len(self.current_audio) / self.sample_rate,
            "channels": self.current_audio.shape[1] if len(self.current_audio.shape) > 1 else 1,
            "sample_rate": self.sample_rate,
            "samples": len(self.current_audio)
        }
    
    def save_audio_file(self, filename: str, audio_data: Optional[np.ndarray] = None) -> bool:
        """Save processed audio to file"""
        try:
            # Use processed audio if no specific data provided
            if audio_data is None:
                audio_data = self.processed_audio
            
            if audio_data is None:
                print("❌ No audio data to save")
                return False
            
            # Save with soundfile
            sf.write(filename, audio_data, self.sample_rate)
            print(f"💾 Audio saved: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save audio: {e}")
            return False
    
    def start_live_input(self) -> bool:
        """Dummy method for compatibility"""
        print("🎙️ Live input not implemented in simple mode")
        return False
    
    def stop_live_input(self):
        """Dummy method for compatibility"""
        pass
    
    def cleanup_audio(self):
        """Clean up audio resources"""
        self.stop_playback()
        pygame.mixer.quit()
        print("🧹 Audio engine cleaned up")
    
    # Callback setters for GUI compatibility
    def set_level_callback(self, callback):
        self.level_callback = callback
    
    def set_progress_callback(self, callback):
        self.progress_callback = callback
    
    def set_waveform_callback(self, callback):
        self.waveform_callback = callback
