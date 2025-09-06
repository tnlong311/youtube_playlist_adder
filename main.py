import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# === CONFIG ===
# Target playlist URL to add videos to
TARGET_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLAcKFUUZmOjtCr4KHIYuYFHhXyr-i-qSc"

# Source playlist URLs to extract video IDs from
SOURCE_PLAYLIST_URLS = [
    "https://www.youtube.com/playlist?list=PLACpTROxW9U0aH4X5mtHWPyUe0DirdhEu",
    "https://www.youtube.com/playlist?list=PLACpTROxW9U0BP8X9GlXqofLlFl_a7nLs&jct=pQNW4biXTxPDOZz3Q6ukvA"
]

# === AUTHENTICATION ===
scopes = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

def get_youtube_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes
    )
    creds = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
    return youtube

def extract_playlist_id(url: str) -> str:
    """
    Extracts the playlist ID from a YouTube URL.
    Example: https://www.youtube.com/playlist?list=PLxxxxxx
    """
    match = re.search(r"list=([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError(f"Invalid playlist URL: {url}")
    return match.group(1)

def get_video_ids(youtube, playlist_id: str):
    """
    Fetch all video IDs from a playlist.
    """
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

def add_video_to_playlist(youtube, video_id, target_playlist_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": target_playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    print(f"✅ Added video {video_id}")

if __name__ == "__main__":
    youtube = get_youtube_service()
    
    # Extract target playlist ID from URL
    target_playlist_id = extract_playlist_id(TARGET_PLAYLIST_URL)
    
    # Collect all video IDs from source playlists
    all_video_ids = []
    
    for playlist_url in SOURCE_PLAYLIST_URLS:
        try:
            playlist_id = extract_playlist_id(playlist_url)
            print(f"📋 Fetching videos from playlist: {playlist_url}")
            video_ids = get_video_ids(youtube, playlist_id)
            all_video_ids.extend(video_ids)
            print(f"   Found {len(video_ids)} videos")
        except Exception as e:
            print(f"❌ Failed to fetch playlist {playlist_url}: {e}")
    
    print(f"\n🎯 Total videos to add: {len(all_video_ids)}")
    print(f"📝 Video IDs: {all_video_ids}")
    
    # Add all videos to target playlist
    for video_id in all_video_ids:
        try:
            add_video_to_playlist(youtube, video_id, target_playlist_id)
        except Exception as e:
            print(f"❌ Failed to add {video_id}: {e}")
    
    print(f"\n✅ Process completed! Added {len(all_video_ids)} videos.\nCheck the playlist: {TARGET_PLAYLIST_URL}")
