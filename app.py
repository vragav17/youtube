import streamlit as st
import requests
from textblob import TextBlob
import plotly.express as px
import yaml
from src.llm.gemini_api import configure_gemini, analyze_comments_with_gemini_flash
import re

# Load config
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

YOUTUBE_API_KEY = config["youtube_api_key"]
GEMINI_API_KEY = config["gemini_api_key"]
MAX_COMMENTS = config["max_comments"]

def fetch_comments(video_id, api_key, max_comments=200):
    comments = []
    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    params = {'part': 'snippet', 'videoId': video_id, 'maxResults': 100,
              'textFormat': 'plainText', 'key': api_key}

    while len(comments) < max_comments:
        res = requests.get(url, params=params).json()
        for item in res.get('items', []):
            comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            if len(comments) >= max_comments:
                break
        if 'nextPageToken' in res:
            params['pageToken'] = res['nextPageToken']
        else:
            break
    return comments

def get_sentiment(comment):
    polarity = TextBlob(comment).sentiment.polarity
    return "Positive" if polarity > 0.1 else "Negative" if polarity < -0.1 else "Neutral"

def generate_sentiment_chart(comments):
    sentiments = [get_sentiment(c) for c in comments]
    sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
    fig = px.pie(names=sentiment_counts.keys(), values=sentiment_counts.values(),
                 title="Sentiment Distribution", color_discrete_sequence=["green", "gray", "red"])
    return fig

# Streamlit UI
st.set_page_config(page_title="YouTube Comments Analyzer")
st.title("📊 YouTube Comments Analyzer ")
st.markdown("made with ❤️ for Anand Sir & Money Pechu Team, by [@vragav17](https://www.linkedin.com/in/vragav17/)")


video_input = st.text_input("Enter YouTube Video URL or ID")
def extract_video_id(url_or_id):
    # If input is just the ID (11 chars, letters/numbers/_/-)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id
    # Try to extract from common YouTube URL formats
    patterns = [
        r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})",
        r"youtube\.com\/shorts\/([A-Za-z0-9_-]{11})"
    ]
    for pat in patterns:
        match = re.search(pat, url_or_id)
        if match:
            return match.group(1)
    return ""
video_id = extract_video_id(video_input)
if st.button("Analyze") and video_id:
    comments = fetch_comments(video_id, YOUTUBE_API_KEY, MAX_COMMENTS)
    st.success(f"Fetched {len(comments)} comments.")
    # st.download_button("📥 Download Comments", "\n".join(comments), "comments.txt")
    

    st.subheader("🧠 Summary")
    configure_gemini(GEMINI_API_KEY)
    summary = analyze_comments_with_gemini_flash(comments)
    st.markdown(summary)
    # st.download_button("📥 Download Summary", summary, "summary.txt")
    
    st.subheader("📈 Sentiment Analysis")
    st.plotly_chart(generate_sentiment_chart(comments), use_container_width=True)
    st.balloons()
    # st.download_button("📥 Download Comments", "\n".join(comments), "comments.txt")
    st.download_button("📥 Download Summary and Comments",summary + "\n Comments: \n"+ "\n".join(comments), "summary&comments.txt")