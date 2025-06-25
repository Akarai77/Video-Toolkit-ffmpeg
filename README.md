# Video-Toolkit-ffmpeg

**Video-Toolkit-ffmpeg** is a powerful and versatile command-line application designed to manage all your video and audio processing needs from a single unified interface. The toolkit supports downloading, clipping, converting, extracting, and codec management of multimedia files, all accessible via a comprehensive **main menu**.

---

## Features

* **Unified Main Menu:** One central interface to access all functionalities including downloading, clipping, converting, extracting, and codec conversion.
* **YouTube Media Download:** Download YouTube videos or audio in selectable formats and resolutions.
* **Video and Audio Clipping:** Create consecutive or custom clips from videos.
* **Media Conversion:** Convert between numerous popular audio and video formats.
* **Codec Management:** Change video and audio codecs for files effortlessly.
* **Media Extraction:** Extract audio tracks, mute videos, or extract subtitles from files.
* **Interactive Command-Line Interface:** Easy to navigate menus with clear prompts and colored messages for success and errors.

---

## Installation

### Prerequisites

* Python 3.8+
* [FFmpeg](https://ffmpeg.org/download.html) installed and added to system PATH
* Python dependencies as specified in `requirements.txt`

### Setup

Install the required Python packages via:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the main application script:

```bash
python main.py
```

You will be greeted by a comprehensive main menu that allows you to:

* Download and convert YouTube media
* Clip videos with customizable options
* Convert audio and video files between formats
* Extract audio, video (mute), or subtitles from media
* Change codecs of video and audio streams

Simply follow the interactive prompts to perform your desired operations.

---

## Project Structure

* `main.py` — The entry point providing the main menu and orchestrating all features.
* `clips.py` — Tools for clipping videos.
* `changeCodecs.py` — Change audio and video codecs.
* `convert.py` — Media format conversion utilities.
* `extract.py` — Extract audio, video, or subtitles.
* `ytConvert.py` — Download and convert YouTube media.
* Utility modules:

  * `menu.py` — Interactive CLI menu system.
  * `colorPrint.py` — Colored terminal output for improved user experience.
  * `IOFunctions.py` — Input/output helpers for file management.
  * `getCodecs.py` — Extract codec information from media files.

---

## Notes

* The toolkit requires FFmpeg accessible via the system PATH.
* Ensure you comply with all legal requirements and platform terms when downloading or processing media.
* Designed for users comfortable with command-line interfaces.

---

## License

Released under the MIT License.

---
