"""
Core Bitcrusher Audio Processing Engine.
"""

import numpy as np
from scipy import signal
from typing import Optional
import threading


class BitCrusher:
    """Advanced bitcrusher with multiple processing algorithms."""
    
    def __init__(self):
        self.sample_rate = 44100
        self.is_processing = False
        self.processing_lock = threading.Lock()
        # Use 64-bit float for better quality and performance
        self.dtype = np.float64
        
    def reduce_bit_depth(self, audio: np.ndarray, bit_depth: int) -> np.ndarray:
        """
        Reduce bit depth for quantization distortion.

        Args:
            audio: Input audio array.
            bit_depth: Target bit depth (1-16).

        Returns:
            Bit-reduced audio.
        """
        if bit_depth >= 16:
            return audio
            
        # Calculate quantization levels
        levels = 2 ** bit_depth
        max_val = levels - 1
        
        # Normalize to 0-1 range, quantize, then scale back
        normalized = (audio + 1.0) / 2.0
        quantized = np.round(normalized * max_val) / max_val
        
        return (quantized * 2.0) - 1.0
    
    def downsample_and_upsample(self, audio: np.ndarray, factor: float) -> np.ndarray:
        """
        Downsample then upsample for aliasing artifacts.

        Args:
            audio: Input audio array (mono or stereo).
            factor: Downsampling factor (1.0 = no change, higher = more crushing).

        Returns:
            Processed audio with aliasing artifacts.
        """
        if factor <= 1.0:
            return audio

        original_len = len(audio)
        target_len = max(1, int(original_len / factor))

        # Handle mono vs stereo via axis parameter
        if audio.ndim == 1:
            downsampled = signal.resample(audio, target_len)
            upsampled = signal.resample(downsampled, original_len)
        else:
            downsampled = signal.resample(audio, target_len, axis=0)
            upsampled = signal.resample(downsampled, original_len, axis=0)

        return upsampled
    
    def apply_waveshaping(self, audio: np.ndarray, drive: float = 0.5) -> np.ndarray:
        """
        Apply waveshaping distortion.

        Args:
            audio: Input audio array.
            drive: Distortion amount (0.0-1.0).

        Returns:
            Waveshaped audio.
        """
        if drive <= 0.0:
            return audio
            
        # Apply soft clipping with adjustable drive
        driven = audio * (1.0 + drive * 3.0)
        return np.tanh(driven) * 0.8
    
    def add_noise(self, audio: np.ndarray, amount: float = 0.1) -> np.ndarray:
        """
        Add digital noise.

        Args:
            audio: Input audio array.
            amount: Noise amount (0.0-1.0).

        Returns:
            Audio with added noise.
        """
        if amount <= 0.0:
            return audio
            
        noise = np.random.normal(0, amount * 0.1, audio.shape)
        return audio + noise
    
    def process_audio(
        self,
        audio: np.ndarray,
        bit_depth: int = 8,
        downsample_factor: float = 1.0,
        mix: float = 1.0,
        waveshape: float = 0.0,
        noise: float = 0.0,
    ) -> np.ndarray:
        """
        Main processing pipeline with all effects.

        Args:
            audio: Input audio array.
            bit_depth: Target bit depth (1-16).
            downsample_factor: Downsampling factor (1.0+).
            mix: Wet/dry mix (0.0-1.0).
            waveshape: Waveshaping amount (0.0-1.0).
            noise: Noise amount (0.0-1.0).

        Returns:
            Processed audio.
        """
        with self.processing_lock:
            self.is_processing = True
            
            try:
                # Start with a copy of the original in 64-bit
                processed = audio.astype(self.dtype)
                original = processed.copy()  # Keep original for mix
                
                # Apply bit depth reduction
                processed = self.reduce_bit_depth(processed, bit_depth)
                
                # Apply downsampling/upsampling
                if downsample_factor > 1.0:
                    processed = self.downsample_and_upsample(processed, downsample_factor)
                
                # Apply waveshaping
                if waveshape > 0.0:
                    processed = self.apply_waveshaping(processed, waveshape)
                
                # Add noise
                if noise > 0.0:
                    processed = self.add_noise(processed, noise)
                
                # Apply wet/dry mix with original 64-bit precision
                if mix < 1.0:
                    processed = original * (1.0 - mix) + processed * mix
                
                # Ensure we don't clip
                processed = np.clip(processed, -1.0, 1.0)
                
                # Ensure output is C-contiguous for pygame compatibility
                if not processed.flags['C_CONTIGUOUS']:
                    processed = np.ascontiguousarray(processed)
                
                return processed
                
            finally:
                self.is_processing = False
    
    def process_realtime_chunk(
        self,
        chunk: np.ndarray,
        bit_depth: int = 8,
        downsample_factor: float = 1.0,
        mix: float = 1.0,
        waveshape: float = 0.0,
        noise: float = 0.0,
    ) -> np.ndarray:
        """Process a small chunk for real-time playback (low latency)."""
        # Create a copy for processing
        processed = chunk.astype(np.float32, copy=True)
        original = chunk.astype(np.float32, copy=True)
        
        # Quick bit depth reduction - most audible effect
        if bit_depth < 16:
            levels = 2 ** bit_depth
            max_val = levels - 1
            # Normalize, quantize, denormalize
            normalized = (processed + 1.0) / 2.0
            quantized = np.round(normalized * max_val) / max_val
            processed = (quantized * 2.0) - 1.0
        
        # Fast downsampling simulation
        if downsample_factor > 1.0:
            step = max(1, int(downsample_factor))
            if step > 1:
                # Simple hold-and-repeat for aliasing effect
                for i in range(0, len(processed), step):
                    end_idx = min(i + step, len(processed))
                    if i < len(processed):
                        processed[i:end_idx] = processed[i]
        
        # Waveshaping — consistent with full processing pipeline
        if waveshape > 0.0:
            driven = processed * (1.0 + waveshape * 3.0)
            processed = np.tanh(driven).astype(np.float32) * 0.8
        
        # Add noise
        if noise > 0.0:
            noise_data = np.random.normal(0, noise * 0.05, processed.shape).astype(np.float32)
            processed = processed + noise_data
        
        # Apply mix
        if mix < 1.0:
            processed = original * (1.0 - mix) + processed * mix
        
        # Clip and ensure C-contiguous
        result = np.clip(processed, -1.0, 1.0)
        if not result.flags['C_CONTIGUOUS']:
            result = np.ascontiguousarray(result)
            
        return result
    
    def get_presets(self) -> dict:
        """Get built-in processing presets."""
        return {
            "subtle": {
                "bit_depth": 12,
                "downsample_factor": 1.5,
                "mix": 0.3,
                "waveshape": 0.1,
                "noise": 0.0
            },
            "retro": {
                "bit_depth": 8,
                "downsample_factor": 2.0,
                "mix": 0.7,
                "waveshape": 0.2,
                "noise": 0.05
            },
            "harsh": {
                "bit_depth": 4,
                "downsample_factor": 4.0,
                "mix": 0.9,
                "waveshape": 0.4,
                "noise": 0.1
            },
            "destroy": {
                "bit_depth": 2,
                "downsample_factor": 8.0,
                "mix": 1.0,
                "waveshape": 0.6,
                "noise": 0.2
            },
            "lofi": {
                "bit_depth": 6,
                "downsample_factor": 3.0,
                "mix": 0.8,
                "waveshape": 0.3,
                "noise": 0.15
            },
            "gameboy": {
                "bit_depth": 4,
                "downsample_factor": 2.5,
                "mix": 1.0,
                "waveshape": 0.1,
                "noise": 0.05
            },
            "telephone": {
                "bit_depth": 3,
                "downsample_factor": 6.0,
                "mix": 1.0,
                "waveshape": 0.5,
                "noise": 0.1
            }
        }
    
    def analyze_audio(self, audio: np.ndarray) -> dict:
        """Analyze audio and return metrics."""
        return {
            "rms": np.sqrt(np.mean(audio**2)),
            "peak": np.max(np.abs(audio)),
            "length": len(audio),
            "dynamic_range": np.max(audio) - np.min(audio),
            "zero_crossings": len(np.where(np.diff(np.signbit(audio)))[0])
        }
