from fastapi import FastAPI

from youtube_transcript_api import YouTubeTranscriptApi

class TranscriptExtractor:
 


 

        
if __name__ == "__main__":
    # Example usage
    video_url = "https://www.youtube.com/watch?v=EN9lEZgyymI"
    get_transcriptor = TranscriptExtractor(video_url).get_transcript()
    if get_transcriptor:
        print(get_transcriptor)
    else:
        print("No transcript available.")

        
