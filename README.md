# JAPRadio

<p align="center">
	<img src="icon.png" alt="JAPRadio icon" width="180">
</p>

JAPRadio is a small Japanese radio content generator built for beginner learners. It creates simple topic ideas, rewrites them into natural radio-style Japanese, generates TTS audio, and stores every episode so you can browse it later in the included viewer.

## What It Does

- Generates a new topic while avoiding semantic overlap with earlier topics.
- Rewrites that topic into a casual, JLPT N5-friendly Japanese radio script.
- Produces TTS audio for the final script.
- Saves each episode as structured JSON in `scripts/` and audio in `audio/`.
- Lets you browse the generated episodes from the HTML viewer.

## Project Structure

- `JAPRadio.ipynb` - main notebook version of the workflow.
- `JAPRadio.py` - exported Python script from the notebook.
- `index.html` - simple browser-based episode viewer.
- `topics.json` - history of previously used topics.
- `scripts/` - saved episode metadata and scripts.
- `audio/` - generated MP3 files.
- `bgm.mp3` - background music used when mixing the final audio output.
- `icon.png` - project icon used in this README and for the app icon.

## Requirements

Install the Python dependencies listed in `requirements.txt`.

You will also need an OpenAI API key available in your environment.

## Setup

1. Create and activate a Python virtual environment.
2. Install the dependencies from `requirements.txt`.
3. Set `OPENAI_API_KEY` in your environment.
4. Run `JAPRadio.py` or execute the notebook in `JAPRadio.ipynb`.

## Output Files

Each run typically produces:

- A new topic appended to `topics.json`.
- A script record saved in `scripts/<timestamp>.json`.
- An MP3 file saved in `audio/<timestamp>.mp3`, mixed with `bgm.mp3` when that background music file is present.

## Viewer

The `index.html` file reads the generated episode metadata and audio files so you can browse them in a simple interface.

If you open it locally, serve the repository through a web server so the browser can load the JSON files correctly.
