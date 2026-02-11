# GhostKitty Bitcrusher

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com)

**Audio bitcrusher with real-time preview.**

Created by **CATHOUSEMP3**.

## Features

### Processing Controls
- **Bit Depth Reduction** — 16-bit down to 1-bit quantization
- **Downsampling** — Sample rate reduction with aliasing artifacts
- **Waveshaping** — Tanh-based harmonic saturation
- **Noise Injection** — Gaussian white noise
- **Wet/Dry Mix** — Blend processed and original signals

### Presets
- **Subtle** — Light processing
- **Retro** — Classic 8-bit character
- **Harsh** — Aggressive digital distortion
- **Destroy** — Maximum bit reduction
- **Lo-Fi** — Warm low-fidelity tone
- **Gameboy** — 4-bit console style
- **Telephone** — Band-limited degradation

### Audio I/O
- Supports WAV, MP3, FLAC, OGG, AIFF
- Real-time parameter updates during playback
- Export processed audio to WAV, FLAC, OGG, AIFF

## Installation

### Requirements
- Python 3.8+
- Windows, macOS, or Linux

### Setup
```bash
git clone https://github.com/CATHOUSEMP3/ghostkitty-bitcrusher.git
cd ghostkitty-bitcrusher
pip install -r requirements.txt
python main.py
```

### Dependencies
- `numpy` — Numerical processing
- `scipy` — Signal processing
- `soundfile` — Audio file I/O
- `pygame` — Audio playback
- `customtkinter` — GUI framework
- `Pillow` — Image support for GUI

## Usage

1. **Load** an audio file (Ctrl+O or click Load File)
2. **Adjust** the processing controls — changes apply immediately
3. **Play** to preview (Space bar or click Play)
4. **Save** the processed result (Ctrl+S or click Save to File)

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Space` | Play / Pause |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save file |

## Technical Details

### Audio Engine
- Sample rate: 44.1 kHz (matches source file)
- Bit depth: Variable (1–16 bit)
- Processing: Full-file with pygame playback

### Algorithms
- **Bit Crushing** — Quantization-based bit depth reduction
- **Downsampling** — `scipy.signal.resample` with proper axis handling for stereo
- **Waveshaping** — `tanh` soft-clipping with adjustable drive
- **Noise** — Gaussian white noise injection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.

## Credits

Created by **CATHOUSEMP3**.

Dependencies: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), [Pygame](https://www.pygame.org/), [NumPy](https://numpy.org/), [SoundFile](https://github.com/bastibe/python-soundfile), [SciPy](https://scipy.org/).
