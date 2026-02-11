"""
GhostKitty Bitcrusher GUI.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from typing import Optional, Callable, Dict, Any
from .audio_engine import AudioEngine
from .bitcrusher import BitCrusher


class GhostKittyGUI:
    """Main application GUI."""
    
    def __init__(self):
        # Set the appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("GhostKitty Bitcrusher")
        self.root.geometry("1200x900")
        self.root.configure(fg_color="#0a0a0a")

        self.audio_engine = AudioEngine()
        self.bitcrusher = BitCrusher()

        # GUI state
        self.current_file = None
        self.is_playing = False
        self.is_live_mode = False

        # Slider references for preset updates
        self.sliders: Dict[str, Any] = {}
        self.slider_labels: Dict[str, ctk.CTkLabel] = {}
        self.level_history = []
        
        # Create the GUI
        self._setup_styles()
        self._create_widgets()
        self._setup_bindings()

        self.audio_engine.set_level_callback(self._update_level_meter)
        self.audio_engine.set_progress_callback(self._update_progress)
        self.audio_engine.set_waveform_callback(self._update_realtime_waveform)
    
    def _setup_styles(self):
        """Set up color scheme and fonts."""
        self.colors = {
            "bg_dark": "#0a0a0a",
            "bg_medium": "#141414",
            "bg_light": "#1e1e1e",
            "primary": "#3b82f6",       # Blue
            "primary_hover": "#2563eb",
            "secondary": "#6366f1",     # Indigo
            "accent": "#10b981",        # Emerald
            "accent_hover": "#059669",
            "danger": "#ef4444",
            "danger_hover": "#dc2626",
            "warning": "#f59e0b",
            "text_primary": "#f1f5f9",
            "text_secondary": "#94a3b8",
            "text_muted": "#64748b",
            "border": "#334155",
        }

        self.fonts = {
            "title": ("Segoe UI", 22, "bold"),
            "heading": ("Segoe UI", 15, "bold"),
            "section": ("Segoe UI", 13, "bold"),
            "normal": ("Segoe UI", 12),
            "small": ("Segoe UI", 11),
            "tiny": ("Segoe UI", 10),
        }
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["bg_dark"],
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self._create_header()

        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_dark"],
            corner_radius=0
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self._create_file_section()
        self._create_controls_section()
        self._create_visualization_section()
        self._create_presets_section()
        self._create_output_section()
    
    def _create_header(self):
        """Create the header section."""
        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_medium"],
            height=80,
            corner_radius=0
        )
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="GHOSTKITTY BITCRUSHER",
            font=self.fonts["title"],
            text_color=self.colors["text_primary"]
        )
        self.title_label.pack(expand=True)

        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="Ready",
            font=self.fonts["small"],
            text_color=self.colors["text_secondary"]
        )
        self.status_label.pack(side="bottom", pady=(0, 10))
    
    def _create_file_section(self):
        """Create file loading section."""
        file_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=8
        )
        file_frame.pack(fill="x", pady=(0, 8))

        file_header = ctk.CTkLabel(
            file_frame,
            text="Audio Input",
            font=self.fonts["heading"],
            text_color=self.colors["text_primary"]
        )
        file_header.pack(pady=(10, 5))

        file_controls = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_controls.pack(fill="x", padx=20, pady=(0, 10))

        self.load_button = ctk.CTkButton(
            file_controls,
            text="Load File",
            font=self.fonts["normal"],
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            text_color=self.colors["text_primary"],
            command=self._load_file,
            width=140,
            height=36,
            corner_radius=6
        )
        self.load_button.pack(side="left", padx=(0, 8))

        self.live_button = ctk.CTkButton(
            file_controls,
            text="Live Input",
            font=self.fonts["normal"],
            fg_color=self.colors["secondary"],
            hover_color=self.colors["primary_hover"],
            text_color=self.colors["text_primary"],
            command=self._toggle_live_input,
            width=120,
            height=36,
            corner_radius=6
        )
        self.live_button.pack(side="left", padx=(0, 8))

        self.file_info_label = ctk.CTkLabel(
            file_controls,
            text="No file loaded",
            font=self.fonts["small"],
            text_color=self.colors["text_muted"]
        )
        self.file_info_label.pack(side="left", padx=(12, 0))

        playback_frame = ctk.CTkFrame(file_controls, fg_color="transparent")
        playback_frame.pack(side="right")

        self.play_button = ctk.CTkButton(
            playback_frame,
            text="Play",
            font=self.fonts["normal"],
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color=self.colors["text_primary"],
            command=self._toggle_playback,
            width=80,
            height=36,
            corner_radius=6
        )
        self.play_button.pack(side="left", padx=(0, 5))

        self.stop_button = ctk.CTkButton(
            playback_frame,
            text="Stop",
            font=self.fonts["normal"],
            fg_color=self.colors["danger"],
            hover_color=self.colors["danger_hover"],
            text_color=self.colors["text_primary"],
            command=self._stop_playback,
            width=80,
            height=36,
            corner_radius=6
        )
        self.stop_button.pack(side="left")
    
    def _create_controls_section(self):
        """Create the main bitcrushing controls."""
        controls_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=8
        )
        controls_frame.pack(fill="x", pady=(0, 8))

        controls_header = ctk.CTkLabel(
            controls_frame,
            text="Processing Controls",
            font=self.fonts["heading"],
            text_color=self.colors["text_primary"]
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
            "BIT DEPTH", "bit_depth",
            "1 bit", "16 bit",
            1, 16, 8,
            self._on_bit_depth_change
        )

        # Downsample Control
        self._create_control_group(
            controls_grid, 1, 0,
            "DOWNSAMPLE", "downsample_factor",
            "1x", "8x",
            1.0, 8.0, 1.0,
            self._on_downsample_change
        )

        # Mix Control
        self._create_control_group(
            controls_grid, 2, 0,
            "MIX", "mix",
            "Dry", "Wet",
            0.0, 1.0, 1.0,
            self._on_mix_change
        )

        # Waveshape Control
        self._create_control_group(
            controls_grid, 0, 1,
            "WAVESHAPE", "waveshape",
            "Off", "Full",
            0.0, 1.0, 0.0,
            self._on_waveshape_change
        )

        # Noise Control
        self._create_control_group(
            controls_grid, 1, 1,
            "NOISE", "noise",
            "Off", "Full",
            0.0, 1.0, 0.0,
            self._on_noise_change
        )
    
    def _create_control_group(self, parent, col, row, title, param_key,
                             min_label, max_label,
                             min_val, max_val, default_val, callback):
        """Create a labeled slider control group and store references."""
        group_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_light"],
            corner_radius=6
        )
        group_frame.grid(row=row, column=col, padx=8, pady=8, sticky="ew")

        title_label = ctk.CTkLabel(
            group_frame,
            text=title,
            font=self.fonts["section"],
            text_color=self.colors["text_primary"]
        )
        title_label.pack(pady=(10, 4))

        value_label = ctk.CTkLabel(
            group_frame,
            text=str(default_val),
            font=self.fonts["normal"],
            text_color=self.colors["accent"]
        )
        value_label.pack(pady=(0, 4))

        slider = ctk.CTkSlider(
            group_frame,
            from_=min_val,
            to=max_val,
            number_of_steps=100,
            fg_color=self.colors["bg_dark"],
            progress_color=self.colors["primary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["primary_hover"],
            command=lambda val, lbl=value_label, cb=callback: self._slider_callback(val, lbl, cb)
        )
        slider.set(default_val)
        slider.pack(padx=20, pady=(0, 4))

        # Store references so presets can update sliders
        self.sliders[param_key] = slider
        self.slider_labels[param_key] = value_label
        
        labels_frame = ctk.CTkFrame(group_frame, fg_color="transparent")
        labels_frame.pack(fill="x", padx=20, pady=(0, 10))

        min_lbl = ctk.CTkLabel(
            labels_frame,
            text=min_label,
            font=self.fonts["tiny"],
            text_color=self.colors["text_muted"]
        )
        min_lbl.pack(side="left")

        max_lbl = ctk.CTkLabel(
            labels_frame,
            text=max_label,
            font=self.fonts["tiny"],
            text_color=self.colors["text_muted"]
        )
        max_lbl.pack(side="right")
    
    def _create_visualization_section(self):
        """Create level meter section."""
        viz_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=8
        )
        viz_frame.pack(fill="x", pady=(0, 8))

        level_frame = ctk.CTkFrame(viz_frame, fg_color="transparent")
        level_frame.pack(fill="x", padx=20, pady=12)

        level_label = ctk.CTkLabel(
            level_frame,
            text="Level:",
            font=self.fonts["normal"],
            text_color=self.colors["text_secondary"]
        )
        level_label.pack(side="left")

        self.level_meter = ctk.CTkProgressBar(
            level_frame,
            width=400,
            height=20,
            fg_color=self.colors["bg_dark"],
            progress_color=self.colors["accent"]
        )
        self.level_meter.pack(side="left", padx=(10, 10))
        self.level_meter.set(0)

        self.audio_status_label = ctk.CTkLabel(
            level_frame,
            text="Idle",
            font=self.fonts["small"],
            text_color=self.colors["text_muted"]
        )
        self.audio_status_label.pack(side="right")
    
    def _create_presets_section(self):
        """Create preset buttons section."""
        presets_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=8
        )
        presets_frame.pack(fill="x", pady=(0, 8))

        presets_header = ctk.CTkLabel(
            presets_frame,
            text="Presets",
            font=self.fonts["heading"],
            text_color=self.colors["text_primary"]
        )
        presets_header.pack(pady=(10, 10))

        buttons_frame = ctk.CTkFrame(presets_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 15))

        presets = self.bitcrusher.get_presets()

        for name, _ in presets.items():
            btn = ctk.CTkButton(
                buttons_frame,
                text=name.upper(),
                font=self.fonts["normal"],
                fg_color=self.colors["bg_light"],
                hover_color=self.colors["primary"],
                text_color=self.colors["text_primary"],
                border_width=1,
                border_color=self.colors["border"],
                command=lambda n=name: self._apply_preset(n),
                width=110,
                height=34,
                corner_radius=6
            )
            btn.pack(side="left", padx=4)
    
    def _create_output_section(self):
        """Create output/save section."""
        output_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=8
        )
        output_frame.pack(fill="x", pady=(0, 8))

        output_controls = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_controls.pack(fill="x", padx=20, pady=12)

        save_label = ctk.CTkLabel(
            output_controls,
            text="Export:",
            font=self.fonts["heading"],
            text_color=self.colors["text_primary"]
        )
        save_label.pack(side="left", padx=(0, 12))

        self.save_button = ctk.CTkButton(
            output_controls,
            text="Save to File",
            font=self.fonts["normal"],
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            text_color=self.colors["text_primary"],
            command=self._save_file,
            width=160,
            height=36,
            corner_radius=6
        )
        self.save_button.pack(side="left")

        self.export_info_label = ctk.CTkLabel(
            output_controls,
            text="Load audio first",
            font=self.fonts["small"],
            text_color=self.colors["text_muted"]
        )
        self.export_info_label.pack(side="left", padx=(12, 0))
    
    def _setup_bindings(self):
        """Set up event bindings."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.bind("<space>", lambda e: self._toggle_playback())
        self.root.bind("<Control-o>", lambda e: self._load_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
    
    def _slider_callback(self, value, label, callback):
        """Handle slider value changes."""
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
        """Handle bit depth changes."""
        self.audio_engine.update_processing_params(bit_depth=int(value))

    def _on_downsample_change(self, value):
        """Handle downsample factor changes."""
        self.audio_engine.update_processing_params(downsample_factor=float(value))

    def _on_mix_change(self, value):
        """Handle mix changes."""
        self.audio_engine.update_processing_params(mix=float(value))

    def _on_waveshape_change(self, value):
        """Handle waveshape changes."""
        self.audio_engine.update_processing_params(waveshape=float(value))

    def _on_noise_change(self, value):
        """Handle noise changes."""
        self.audio_engine.update_processing_params(noise=float(value))
    
    def _load_file(self):
        """Load an audio file."""
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
            self._update_status("Loading...")
            success = self.audio_engine.load_audio_file(filename)
            self._on_file_loaded(filename, success)
    
    def _on_file_loaded(self, filename, success):
        """Handle file load completion."""
        if success:
            self.current_file = filename
            info = self.audio_engine.get_audio_info()

            if info:
                duration = info["duration"]
                channels = info["channels"]
                sr = info["sample_rate"]
                self.file_info_label.configure(
                    text=f"{duration:.1f}s | {channels}ch | {sr}Hz"
                )
                self.export_info_label.configure(text="Ready to export")
                self.audio_status_label.configure(text="Loaded")

            self._update_status("Audio loaded")
        else:
            messagebox.showerror("Error", "Failed to load audio file.")
            self._update_status("Load failed")
    
    def _toggle_playback(self):
        """Toggle audio playback."""
        if not self.is_playing:
            if self.audio_engine.current_audio is not None:
                success = self.audio_engine.start_playback()
                if success:
                    self.is_playing = True
                    self.play_button.configure(text="Pause")
                    self.audio_status_label.configure(text="Playing")
                    self._update_status("Playing")
                else:
                    messagebox.showerror("Error", "Playback failed.")
            else:
                messagebox.showwarning("Warning", "Load an audio file first.")
        else:
            self._stop_playback()

    def _stop_playback(self):
        """Stop audio playback."""
        self.audio_engine.stop_playback()
        self.is_playing = False
        self.play_button.configure(text="Play")
        self.audio_status_label.configure(text="Stopped")
        self.level_meter.set(0)
        self._update_status("Stopped")
    
    def _toggle_live_input(self):
        """Toggle live audio input."""
        if not self.is_live_mode:
            success = self.audio_engine.start_live_input()
            if success:
                self.is_live_mode = True
                self.live_button.configure(text="Stop Live")
                self._update_status("Live input active")
            else:
                messagebox.showinfo("Info", "Live input is not available in this version.")
        else:
            self.audio_engine.stop_live_input()
            self.is_live_mode = False
            self.live_button.configure(text="Live Input")
            self._update_status("Live input stopped")
    
    def _apply_preset(self, preset_name):
        """Apply a processing preset and update sliders."""
        presets = self.bitcrusher.get_presets()
        if preset_name in presets:
            params = presets[preset_name]
            self.audio_engine.update_processing_params(**params)

            # Sync sliders to preset values
            for key, value in params.items():
                if key in self.sliders:
                    self.sliders[key].set(value)
                if key in self.slider_labels:
                    if isinstance(value, float) and value != int(value):
                        self.slider_labels[key].configure(text=f"{value:.2f}")
                    else:
                        self.slider_labels[key].configure(text=str(int(value) if isinstance(value, float) and value == int(value) else value))

            self._update_status(f"Preset: {preset_name.upper()}")
    
    def _save_file(self):
        """Save the processed audio."""
        if self.audio_engine.current_audio is None:
            messagebox.showwarning("Warning", "Load an audio file first.")
            return

        filetypes = [
            ("WAV files", "*.wav"),
            ("FLAC files", "*.flac"),
            ("OGG files", "*.ogg"),
            ("AIFF files", "*.aiff")
        ]

        filename = filedialog.asksaveasfilename(
            title="Save Processed Audio",
            defaultextension=".wav",
            filetypes=filetypes
        )

        if filename:
            self._update_status("Saving...")

            processed = self.bitcrusher.process_audio(
                self.audio_engine.current_audio,
                **self.audio_engine.processing_params
            )

            success = self.audio_engine.save_audio_file(filename, processed)
            self._on_file_saved(filename, success)

    def _on_file_saved(self, filename, success):
        """Handle file save completion."""
        if success:
            self._update_status("Saved successfully")
        else:
            messagebox.showerror("Error", "Failed to save audio file.")
            self._update_status("Save failed")
    
    def _update_realtime_waveform(self, waveform_chunk):
        """Waveform callback (no-op for now)."""
        pass

    def _update_level_meter(self, level):
        """Update the audio level meter."""
        self.level_history.append(level)
        if len(self.level_history) > 10:
            self.level_history.pop(0)

        avg_level = np.mean(self.level_history)
        display_level = min(1.0, avg_level * 3.0)
        self.level_meter.set(display_level)

    def _update_progress(self, progress):
        """Update playback progress (no-op for now)."""
        pass

    def _update_status(self, message):
        """Update the status bar message."""
        self.status_label.configure(text=message)

    def _on_closing(self):
        """Handle application closing."""
        self.audio_engine.cleanup_audio()
        self.root.destroy()

    def run(self):
        """Start the GUI main loop."""
        self._update_status("Ready")
        self.root.mainloop()
