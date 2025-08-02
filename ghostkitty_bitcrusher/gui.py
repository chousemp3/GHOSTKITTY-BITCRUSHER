"""
Epic Cyberpunk Hacker GUI for GhostKitty Bitcrusher 👻⚡
Dark theme with neon accents and smooth performance
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from typing import Optional, Callable
from .audio_engine import AudioEngine
from .bitcrusher import BitCrusher


class GhostKittyGUI:
    """
    Cyberpunk-themed GUI for the bitcrusher app 🔥
    Simple and fast
    """
    
    def __init__(self):
        # Set the appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Initialize the main window with SICK black styling
        self.root = ctk.CTk()
        self.root.title("��👻 GHOSTKITTY BITCRUSHER 👻🔥")
        self.root.geometry("1400x1000")  # Bigger window for more epic content
        self.root.configure(fg_color="#000000")  # Pure black background
        
        # Simple audio engine
        self.audio_engine = AudioEngine()
        self.bitcrusher = BitCrusher()
        
        # GUI state
        self.current_file = None
        self.is_playing = False
        self.is_live_mode = False
        
        # Animation variables
        self.glitch_counter = 0
        self.level_history = []
        
        # Create the GUI
        self._setup_styles()
        self._create_widgets()
        self._setup_bindings()
        self._start_animations()
        
        # Set up audio callbacks for real-time updates
        self.audio_engine.set_level_callback(self._update_level_meter)
        self.audio_engine.set_progress_callback(self._update_progress)
        self.audio_engine.set_waveform_callback(self._update_realtime_waveform)
    
    def _setup_styles(self):
        """Set up EPIC cyberpunk color scheme and fonts"""
        self.colors = {
            "bg_dark": "#000000",           # Pure black background
            "bg_medium": "#111111",         # Dark charcoal
            "bg_light": "#1a1a1a",          # Slightly lighter black
            "accent_neon_green": "#00ff00", # Bright matrix green
            "accent_cyber_blue": "#00ccff", # Electric blue
            "accent_hot_pink": "#ff0080",   # Hot pink
            "accent_purple": "#8800ff",     # Electric purple
            "accent_orange": "#ff4400",     # Neon orange
            "accent_red": "#ff0000",        # Pure red
            "accent_yellow": "#ffff00",     # Electric yellow
            "text_neon": "#00ff00",         # Neon green text
            "text_bright": "#ffffff",       # Pure white
            "text_dim": "#888888",          # Gray
            "border_glow": "#00ff00"        # Glowing border color
        }
        
        self.fonts = {
            "title": ("Courier New", 28, "bold"),     # Bigger, hacker font
            "heading": ("Courier New", 18, "bold"),   # Bold cyber headings
            "section": ("Courier New", 16, "bold"),   # Section headers
            "normal": ("Courier New", 14, "bold"),    # Normal text
            "small": ("Courier New", 12),             # Small text
            "tiny": ("Courier New", 10)               # Tiny text
        }
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["bg_dark"],
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Title header
        self._create_header()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_dark"],
            corner_radius=0
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create main layout
        self._create_file_section()
        self._create_controls_section()
        self._create_visualization_section()
        self._create_presets_section()
        self._create_output_section()
    
    def _create_header(self):
        """Create the EPIC animated header section"""
        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_medium"],
            height=100,  # Taller header
            corner_radius=0
        )
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # EPIC animated title with more emojis
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="��👻⚡ GHOSTKITTY BITCRUSHER ⚡👻🔥",
            font=self.fonts["title"],
            text_color=self.colors["accent_neon_green"]
        )
        self.title_label.pack(expand=True)
        
        # Cool status bar with neon styling
        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="⚡ SYSTEM READY FOR MAXIMUM AUDIO DESTRUCTION ⚡",
            font=self.fonts["normal"],
            text_color=self.colors["accent_cyber_blue"]
        )
        self.status_label.pack(side="bottom", pady=(0, 15))
    
    def _create_file_section(self):
        """Create file loading section"""
        file_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=10
        )
        file_frame.pack(fill="x", pady=(0, 10))
        
        # File section header with SICK styling
        file_header = ctk.CTkLabel(
            file_frame,
            text="🎵⚡ AUDIO INPUT MATRIX ⚡🎵",
            font=self.fonts["heading"],
            text_color=self.colors["accent_cyber_blue"]
        )
        file_header.pack(pady=(10, 5))
        
        # File controls frame
        file_controls = ctk.CTkFrame(
            file_frame,
            fg_color="transparent"
        )
        file_controls.pack(fill="x", padx=20, pady=(0, 10))
        
        # Load file button with NEON styling
        self.load_button = ctk.CTkButton(
            file_controls,
            text="🔥 LOAD AUDIO FILE 🔥",
            font=self.fonts["normal"],
            fg_color=self.colors["accent_neon_green"],
            hover_color=self.colors["accent_cyber_blue"],
            text_color=self.colors["bg_dark"],
            command=self._load_file,
            width=180,
            height=40,
            corner_radius=20
        )
        self.load_button.pack(side="left", padx=(0, 10))
        
        # Live input button with HOT PINK
        self.live_button = ctk.CTkButton(
            file_controls,
            text="🎙️ LIVE INPUT 🎙️",
            font=self.fonts["normal"],
            fg_color=self.colors["accent_hot_pink"],
            hover_color=self.colors["accent_purple"],
            text_color=self.colors["text_bright"],
            command=self._toggle_live_input,
            width=150,
            height=40,
            corner_radius=20
        )
        self.live_button.pack(side="left", padx=(0, 10))
        
        # File info
        self.file_info_label = ctk.CTkLabel(
            file_controls,
            text="No file loaded",
            font=self.fonts["small"],
            text_color=self.colors["text_dim"]
        )
        self.file_info_label.pack(side="left", padx=(20, 0))
        
        # Playback controls
        playback_frame = ctk.CTkFrame(
            file_controls,
            fg_color="transparent"
        )
        playback_frame.pack(side="right")
        
        # EPIC play button
        self.play_button = ctk.CTkButton(
            playback_frame,
            text="▶ PLAY",
            font=self.fonts["normal"],
            fg_color=self.colors["accent_neon_green"],
            hover_color=self.colors["accent_yellow"],
            text_color=self.colors["bg_dark"],
            command=self._toggle_playback,
            width=90,
            height=40,
            corner_radius=20
        )
        self.play_button.pack(side="left", padx=(0, 5))
        
        # SICK stop button
        self.stop_button = ctk.CTkButton(
            playback_frame,
            text="⏹ STOP",
            font=self.fonts["normal"],
            fg_color=self.colors["accent_red"],
            hover_color=self.colors["accent_orange"],
            text_color=self.colors["text_bright"],
            command=self._stop_playback,
            width=90,
            height=40,
            corner_radius=20
        )
        self.stop_button.pack(side="left")
    
    def _create_controls_section(self):
        """Create the main bitcrushing controls"""
        controls_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=10
        )
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Controls header with MAXIMUM DESTRUCTION styling
        controls_header = ctk.CTkLabel(
            controls_frame,
            text="⚡💀 MAXIMUM DESTRUCTION CONTROLS 💀⚡",
            font=self.fonts["heading"],
            text_color=self.colors["accent_hot_pink"]
        )
        controls_header.pack(pady=(10, 15))
        
        # Controls grid
        controls_grid = ctk.CTkFrame(
            controls_frame,
            fg_color="transparent"
        )
        controls_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Configure grid
        for i in range(3):
            controls_grid.columnconfigure(i, weight=1)
        
        # Bit Depth Control
        self._create_control_group(
            controls_grid, 0, 0,
            "BIT DEPTH",
            "1 bit", "16 bit",
            1, 16, 8,
            self._on_bit_depth_change
        )
        
        # Downsample Control  
        self._create_control_group(
            controls_grid, 1, 0,
            "DOWNSAMPLE",
            "Clean", "Crushed",
            1.0, 8.0, 1.0,
            self._on_downsample_change
        )
        
        # Mix Control
        self._create_control_group(
            controls_grid, 2, 0,
            "MIX",
            "Dry", "Wet", 
            0.0, 1.0, 1.0,
            self._on_mix_change
        )
        
        # Waveshape Control
        self._create_control_group(
            controls_grid, 0, 1,
            "WAVESHAPE",
            "Clean", "Distorted",
            0.0, 1.0, 0.0,
            self._on_waveshape_change
        )
        
        # Noise Control
        self._create_control_group(
            controls_grid, 1, 1,
            "NOISE",
            "Silent", "Noisy",
            0.0, 1.0, 0.0,
            self._on_noise_change
        )
    
    def _create_control_group(self, parent, col, row, title, min_label, max_label, 
                             min_val, max_val, default_val, callback):
        """Create a labeled slider control group"""
        group_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_light"],
            corner_radius=8
        )
        group_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Title with NEON glow effect
        title_label = ctk.CTkLabel(
            group_frame,
            text=title,
            font=self.fonts["normal"],
            text_color=self.colors["accent_cyber_blue"]
        )
        title_label.pack(pady=(10, 5))
        
        # Value display with NEON text
        value_label = ctk.CTkLabel(
            group_frame,
            text=str(default_val),
            font=self.fonts["normal"],
            text_color=self.colors["accent_neon_green"]
        )
        value_label.pack(pady=(0, 5))
        
        # EPIC slider with neon colors
        slider = ctk.CTkSlider(
            group_frame,
            from_=min_val,
            to=max_val,
            number_of_steps=100,
            fg_color=self.colors["bg_dark"],
            progress_color=self.colors["accent_neon_green"],
            button_color=self.colors["accent_hot_pink"],
            button_hover_color=self.colors["accent_cyber_blue"],
            command=lambda val, lbl=value_label, cb=callback: self._slider_callback(val, lbl, cb)
        )
        slider.set(default_val)
        slider.pack(padx=20, pady=(0, 5))
        
        # Min/Max labels
        labels_frame = ctk.CTkFrame(
            group_frame,
            fg_color="transparent"
        )
        labels_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        min_lbl = ctk.CTkLabel(
            labels_frame,
            text=min_label,
            font=self.fonts["small"],
            text_color=self.colors["text_dim"]
        )
        min_lbl.pack(side="left")
        
        max_lbl = ctk.CTkLabel(
            labels_frame, 
            text=max_label,
            font=self.fonts["small"],
            text_color=self.colors["text_dim"]
        )
        max_lbl.pack(side="right")
    
    def _create_visualization_section(self):
        """Create simple visualization section without matplotlib lag"""
        viz_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=10
        )
        viz_frame.pack(fill="x", pady=(0, 10))
        
        # Viz header with MATRIX styling
        viz_header = ctk.CTkLabel(
            viz_frame,
            text="📊⚡ SYSTEM STATUS MATRIX ⚡📊",
            font=self.fonts["heading"],
            text_color=self.colors["accent_neon_green"]
        )
        viz_header.pack(pady=(10, 10))
        
        # Simple level meter only - no complex matplotlib
        level_frame = ctk.CTkFrame(
            viz_frame,
            fg_color="transparent"
        )
        level_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # NEON level meter
        level_label = ctk.CTkLabel(
            level_frame,
            text="⚡ POWER LEVEL:",
            font=self.fonts["normal"],
            text_color=self.colors["accent_cyber_blue"]
        )
        level_label.pack(side="left")
        
        self.level_meter = ctk.CTkProgressBar(
            level_frame,
            width=400,  # Wider meter
            height=30,  # Taller meter
            fg_color=self.colors["bg_dark"],
            progress_color=self.colors["accent_neon_green"]
        )
        self.level_meter.pack(side="left", padx=(10, 0))
        self.level_meter.set(0)
        
        # Status info
        self.audio_status_label = ctk.CTkLabel(
            level_frame,
            text="Ready",
            font=self.fonts["small"],
            text_color=self.colors["text_dim"]
        )
        self.audio_status_label.pack(side="right")
    
    def _create_presets_section(self):
        """Create preset buttons section"""
        presets_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=10
        )
        presets_frame.pack(fill="x", pady=(0, 10))
        
        # EPIC presets header
        presets_header = ctk.CTkLabel(
            presets_frame,
            text="🎛️💥 DESTRUCTION PRESETS 💥🎛️",
            font=self.fonts["heading"],
            text_color=self.colors["accent_purple"]
        )
        presets_header.pack(pady=(10, 10))
        
        # Preset buttons
        buttons_frame = ctk.CTkFrame(
            presets_frame,
            fg_color="transparent"
        )
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        presets = self.bitcrusher.get_presets()
        preset_colors = [
            self.colors["accent_neon_green"],
            self.colors["accent_cyber_blue"], 
            self.colors["accent_hot_pink"],
            self.colors["accent_purple"],
            self.colors["accent_orange"],
            self.colors["accent_yellow"]
        ]
        
        for i, (name, _) in enumerate(presets.items()):
            color = preset_colors[i % len(preset_colors)]
            btn = ctk.CTkButton(
                buttons_frame,
                text=f"🔥 {name.upper()} 🔥",
                font=self.fonts["normal"],
                fg_color=color,
                hover_color=self.colors["bg_light"],
                text_color=self.colors["bg_dark"],
                command=lambda n=name: self._apply_preset(n),
                width=120,
                height=40,
                corner_radius=20
            )
            btn.pack(side="left", padx=5)
    
    def _create_output_section(self):
        """Create compact output/save section"""
        print("🔧 Creating output section...")  # Debug
        output_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=10
        )
        output_frame.pack(fill="x", pady=(0, 10))
        print("🔧 Output frame packed!")  # Debug
        
        # Simple horizontal layout
        output_controls = ctk.CTkFrame(
            output_frame,
            fg_color="transparent"
        )
        output_controls.pack(fill="x", padx=20, pady=15)
        
        # EPIC save label
        save_label = ctk.CTkLabel(
            output_controls,
            text="💾🔥 SAVE AUDIO:",
            font=self.fonts["heading"],
            text_color=self.colors["accent_neon_green"]
        )
        save_label.pack(side="left", padx=(0, 15))
        
        # MASSIVE save button
        self.save_button = ctk.CTkButton(
            output_controls,
            text="💾 SAVE TO FILE 💾",
            font=self.fonts["normal"],
            fg_color=self.colors["accent_neon_green"],
            hover_color=self.colors["accent_cyber_blue"],
            text_color=self.colors["bg_dark"],
            command=self._save_file,
            width=200,
            height=50,
            corner_radius=25
        )
        self.save_button.pack(side="left")
        print("🔧 Save button created and packed!")  # Debug
        
        # EPIC status info
        self.export_info_label = ctk.CTkLabel(
            output_controls,
            text="⚡ Load audio first ⚡",
            font=self.fonts["normal"],
            text_color=self.colors["accent_cyber_blue"]
        )
        self.export_info_label.pack(side="left", padx=(15, 0))
        print("🔧 Output section complete!")  # Debug
    
    def _setup_bindings(self):
        """Set up event bindings"""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Keyboard shortcuts
        self.root.bind("<space>", lambda e: self._toggle_playback())
        self.root.bind("<Control-o>", lambda e: self._load_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
    
    def _start_animations(self):
        """Start GUI animations"""
        self._animate_title()
        self._update_visualizations()
    
    def _animate_title(self):
        """EPIC title animation with more glitch effects"""
        def glitch_animation():
            glitch_chars = ["�", "⚡", "💀", "👾", "�", "�", "�", "🎵", "⚙️", "💎"]
            cyber_effects = ["[SYSTEM]", "[ERROR]", "[HACKED]", "[GLITCH]", "[MATRIX]"]
            
            if self.glitch_counter % 80 == 0:  # More frequent glitches
                # EPIC glitch effect
                original = "🔥👻⚡ GHOSTKITTY BITCRUSHER ⚡👻🔥"
                
                if np.random.random() < 0.3:  # 30% chance for cyber effect
                    effect = np.random.choice(cyber_effects)
                    glitched = f"{effect} {original} {effect}"
                else:
                    glitched = ""
                    for char in original:
                        if char.isalpha() and np.random.random() < 0.15:
                            glitched += np.random.choice(glitch_chars)
                        else:
                            glitched += char
                
                self.title_label.configure(text=glitched)
                
                # Reset after brief moment
                self.root.after(300, lambda: self.title_label.configure(text=original))
            
            self.glitch_counter += 1
            self.root.after(40, glitch_animation)  # Faster animation
        
        glitch_animation()
    
    def _update_visualizations(self):
        """Simple visualization updates - no complex matplotlib"""
        def update_viz():
            # Just update level meter if audio is playing
            if self.is_playing and hasattr(self, 'level_meter'):
                # Simple fake level animation
                import random
                level = random.random() * 0.5 + 0.2  # Random level between 0.2-0.7
                self.level_meter.set(level)
            
            # Update much less frequently to avoid lag
            self.root.after(500, update_viz)  # 2 FPS only for level meter
        
        update_viz()
    
    def _slider_callback(self, value, label, callback):
        """Handle slider value changes"""
        # Update display
        if isinstance(value, float):
            if value == int(value):
                label.configure(text=str(int(value)))
            else:
                label.configure(text=f"{value:.2f}")
        else:
            label.configure(text=str(value))
        
        # Call the parameter callback
        callback(value)
    
    def _on_bit_depth_change(self, value):
        """Handle bit depth changes"""
        self.audio_engine.update_processing_params(bit_depth=int(value))
    
    def _on_downsample_change(self, value):
        """Handle downsample factor changes"""
        self.audio_engine.update_processing_params(downsample_factor=float(value))
    
    def _on_mix_change(self, value):
        """Handle mix changes"""
        self.audio_engine.update_processing_params(mix=float(value))
    
    def _on_waveshape_change(self, value):
        """Handle waveshape changes"""
        self.audio_engine.update_processing_params(waveshape=float(value))
    
    def _on_noise_change(self, value):
        """Handle noise changes"""
        self.audio_engine.update_processing_params(noise=float(value))
    
    def _load_file(self):
        """Load an audio file"""
        filetypes = [
            ("Audio files", "*.wav *.mp3 *.flac *.ogg *.aiff *.au"),
            ("WAV files", "*.wav"),
            ("MP3 files", "*.mp3"),
            ("FLAC files", "*.flac"),
            ("OGG files", "*.ogg"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=filetypes
        )
        
        if filename:
            self._update_status("Loading audio file...")
            
            # Load synchronously - simple and fast
            success = self.audio_engine.load_audio_file(filename)
            self._on_file_loaded(filename, success)
    
    def _on_file_loaded(self, filename, success):
        """Handle file load completion"""
        if success:
            self.current_file = filename
            info = self.audio_engine.get_audio_info()
            
            if info:
                duration = info["duration"]
                channels = info["channels"]
                self.file_info_label.configure(
                    text=f"Loaded: {duration:.1f}s, {channels}ch"
                )
                self.export_info_label.configure(
                    text="Ready to save!"
                )
            
            self._update_status("Audio loaded successfully! ⚡")
        else:
            messagebox.showerror("Error", "Failed to load audio file")
            self._update_status("Failed to load audio file")
    
    def _toggle_playback(self):
        """Toggle audio playback"""
        if not self.is_playing:
            if self.audio_engine.current_audio is not None:
                success = self.audio_engine.start_playback()
                if success:
                    self.is_playing = True
                    self.play_button.configure(text="⏸ PAUSE")
                    self._update_status("Playing with REAL-TIME parameter updates! 🎵⚡")
                else:
                    messagebox.showerror("Error", "Failed to start playback")
            else:
                messagebox.showwarning("Warning", "Please load an audio file first")
        else:
            self._stop_playback()
    
    def _stop_playback(self):
        """Stop audio playback"""
        self.audio_engine.stop_playback()
        self.is_playing = False
        self.play_button.configure(text="▶ PLAY")
        self._update_status("Playback stopped")
    
    def _toggle_live_input(self):
        """Toggle live audio input processing"""
        if not self.is_live_mode:
            success = self.audio_engine.start_live_input()
            if success:
                self.is_live_mode = True
                self.live_button.configure(text="STOP LIVE")
                self._update_status("Live input processing active! 🎙️")
            else:
                messagebox.showerror("Error", "Failed to start live input")
        else:
            self.audio_engine.stop_live_input()
            self.is_live_mode = False
            self.live_button.configure(text="LIVE INPUT")
            self._update_status("Live input stopped")
    
    def _apply_preset(self, preset_name):
        """Apply a processing preset"""
        presets = self.bitcrusher.get_presets()
        if preset_name in presets:
            params = presets[preset_name]
            
            # Update all sliders (we'd need to store references to do this properly)
            # For now, just update the audio engine
            self.audio_engine.update_processing_params(**params)
            
            self._update_status(f"Applied {preset_name.upper()} preset! 🎛️")
    
    def _save_file(self):
        """Save the processed audio"""
        if self.audio_engine.current_audio is None:
            messagebox.showwarning("Warning", "Please load an audio file first")
            return
        
        filetypes = [
            ("WAV files", "*.wav"),
            ("FLAC files", "*.flac"),
            ("OGG files", "*.ogg"),
            ("AIFF files", "*.aiff")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="Save Crushed Audio",
            defaultextension=".wav",
            filetypes=filetypes
        )
        
        if filename:
            self._update_status("Saving crushed audio...")
            
            # Save synchronously - simple and fast
            if self.audio_engine.current_audio is None:
                self._on_file_saved(filename, False)
                return
            
            # Process the full audio first
            processed = self.bitcrusher.process_audio(
                self.audio_engine.current_audio,
                **self.audio_engine.processing_params
            )
            
            success = self.audio_engine.save_audio_file(filename, processed)
            self._on_file_saved(filename, success)
    
    def _on_file_saved(self, filename, success):
        """Handle file save completion"""
        if success:
            self._update_status(f"Audio saved successfully! 💾")
        else:
            messagebox.showerror("Error", "Failed to save audio file")
            self._update_status("Failed to save audio file")
    
    def _update_realtime_waveform(self, waveform_chunk):
        """Simple waveform update - no complex threading"""
        pass  # Simplified - no complex visualization
    
    def _update_level_meter(self, level):
        """Update the audio level meter"""
        # Add to history for smoothing
        self.level_history.append(level)
        if len(self.level_history) > 10:
            self.level_history.pop(0)
        
        # Use average for smoother display
        avg_level = np.mean(self.level_history)
        
        # Update meter (clamp to 0-1 range)
        display_level = min(1.0, avg_level * 3.0)  # Scale for visibility
        self.level_meter.set(display_level)
    
    def _update_progress(self, progress):
        """Update playback progress"""
        # Could add a progress bar here if desired
        pass
    
    def _update_status(self, message):
        """Update the status message"""
        self.status_label.configure(text=message)
    
    def _on_closing(self):
        """Handle application closing"""
        self.audio_engine.cleanup_audio()
        self.root.destroy()
    
    def run(self):
        """Start the GUI main loop"""
        self._update_status("GHOSTKITTY BITCRUSHER READY! 👻⚡")
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.mainloop()
