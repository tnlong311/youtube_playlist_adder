# YouTube Playlist Adder

A Python script to automatically add videos from multiple source playlists to a target playlist.

## Setup

### 1. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Choose "Desktop application"
6. Add your email address in "Test users" under "Audience" page
7. Download the JSON file and rename it to `client_secret.json`
8. Place `client_secret.json` in the project root

### 2. Local Setup

```bash
# Create virtual environment (if not exists)
python3 -m venv venv

# Enable & activate virtual environment
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Adjust CONFIG in main.py
# - Set TARGET_PLAYLIST_URL (where videos will be added)
# - Set SOURCE_PLAYLIST_URLS (list of source playlist URLs)

# Run the script
python3 main.py
```

## Configuration

Edit the CONFIG section in `main.py`:

```python
TARGET_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLAcKFUUZmOjvl0-ZDNRRGp_iSGtrQmDJL"  # Your target playlist
SOURCE_PLAYLIST_URLS = [
    "https://www.youtube.com/playlist?list=PLxxxxxx",  # Source playlists
    "https://www.youtube.com/playlist?list=PLyyyyyy",
]
```

## Usage

The script will:
1. Extract video IDs from all source playlists
2. Add all videos to the target playlist
3. Show progress and results
