# YouTube Playlist URL Exporter

A Python tool to export all video URLs from a YouTube playlist to a text file.

## Setup

### 1. Get a YouTube Data API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the "YouTube Data API v3"
4. Go to "Credentials" and create an API key
5. Copy your API key

### 2. Requirements

- Python 3.6 or higher (no additional packages required - uses standard library only)

## Usage

### Interactive Mode

Run the script and follow the prompts:

```bash
python3 youtube_playlist_exporter.py
```

### Command Line Mode

Provide arguments directly:

```bash
python3 youtube_playlist_exporter.py "PLAYLIST_URL" "YOUR_API_KEY" "output.txt"
```

### Example

```bash
python3 youtube_playlist_exporter.py "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" "AIzaSyD..." "my_playlist.txt"
```

## Output Format

The script creates a text file with video titles and URLs:

```
Video Title 1
https://www.youtube.com/watch?v=abc123

Video Title 2
https://www.youtube.com/watch?v=def456

...
```

## Features

- Exports all videos from a playlist (handles pagination automatically)
- Includes video titles alongside URLs
- No external dependencies required
- Handles playlists of any size

## Notes

- The YouTube Data API has a daily quota limit (10,000 units per day by default)
- Each request costs approximately 1 unit, so you can export many playlists per day
- The playlist must be public or unlisted to access via the API
