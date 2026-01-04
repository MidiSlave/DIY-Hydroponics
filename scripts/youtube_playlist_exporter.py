#!/usr/bin/env python3
"""
YouTube Playlist URL Exporter
Exports all video URLs from a YouTube playlist to a text file.
"""

import sys
import json
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def get_playlist_id(playlist_url):
    """Extract playlist ID from YouTube URL."""
    parsed_url = urlparse(playlist_url)

    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'list' in query_params:
            return query_params['list'][0]

    raise ValueError("Invalid YouTube playlist URL. Please provide a valid playlist URL.")


def fetch_playlist_videos(playlist_id, api_key):
    """Fetch all video URLs from a YouTube playlist using the YouTube Data API."""
    videos = []
    next_page_token = None

    while True:
        # Build API request URL
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key={api_key}"

        if next_page_token:
            url += f"&pageToken={next_page_token}"

        try:
            # Make request
            req = Request(url)
            with urlopen(req) as response:
                data = json.loads(response.read().decode())

            # Extract video IDs and titles
            for item in data.get('items', []):
                video_id = item['snippet']['resourceId']['videoId']
                title = item['snippet']['title']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                videos.append({'url': video_url, 'title': title})

            # Check for more pages
            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                break

        except HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            if e.code == 403:
                print("API key may be invalid or quota exceeded.")
            sys.exit(1)
        except URLError as e:
            print(f"URL Error: {e.reason}")
            sys.exit(1)

    return videos


def export_to_file(videos, output_file, include_titles=True):
    """Export video URLs to a text file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for video in videos:
            if include_titles:
                f.write(f"{video['title']}\n{video['url']}\n\n")
            else:
                f.write(f"{video['url']}\n")

    print(f"Exported {len(videos)} video URLs to {output_file}")


def main():
    print("YouTube Playlist URL Exporter")
    print("=" * 50)

    # Get playlist URL
    if len(sys.argv) > 1:
        playlist_url = sys.argv[1]
    else:
        playlist_url = input("Enter YouTube playlist URL: ").strip()

    # Get API key
    if len(sys.argv) > 2:
        api_key = sys.argv[2]
    else:
        api_key = input("Enter your YouTube Data API key: ").strip()

    # Get output filename
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
    else:
        output_file = input("Enter output filename (default: playlist_urls.txt): ").strip()
        if not output_file:
            output_file = "playlist_urls.txt"

    try:
        # Extract playlist ID
        playlist_id = get_playlist_id(playlist_url)
        print(f"\nPlaylist ID: {playlist_id}")

        # Fetch videos
        print("Fetching playlist videos...")
        videos = fetch_playlist_videos(playlist_id, api_key)

        if not videos:
            print("No videos found in playlist.")
            return

        # Export to file
        export_to_file(videos, output_file, include_titles=True)
        print(f"\n✓ Successfully exported {len(videos)} videos!")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
