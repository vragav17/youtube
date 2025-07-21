import google.generativeai as genai

def configure_gemini(api_key):
    genai.configure(api_key=api_key)

def _format_comments_with_usernames(comments_dict):
    return "\n".join(f"{user}: {comment}" for user, comment in comments_dict.items())

def analyze_comments_with_gemini_flash(comments_dict):
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    formatted_comments = "\n".join(comments_dict)
    prompt = f"""
You are an intelligent assistant for a Tamil-based YouTube finance channel that focuses on stock market analysis, mutual fund advice, personal finance Q&A, and economic commentary. The comments may contain English, Tamil, or a mix (Tanglish), and they reflect the opinions, questions, and emotions of a highly engaged retail investor audience.

Analyze the following YouTube comments and produce the following structured summary:

##🧾 **Viewer Questions for Q&A (in English or Tamil)**:
   - Extract clear, specific questions asked by users. These may be related to:
     - Specific stock analysis (e.g., Tata Motors vs Ashok Leyland)
     - Mutual funds, index funds, SIP performance
     - Gold investment via GoldBees or physical
     - Home loan, insurance, tax questions
     - Bond investments or other savings options
   - Provide full question text as-is, including any Tamil phrases.
   - If a question is not clear, mention it as "Unclear question".
   - 

## 💬 **Common Discussion Topics / Clusters**:
   - Identify and summarize main discussion themes from the comments.
     - For example:
       - Mutual fund performance comparisons
       - Active vs passive investing strategies
       - Gold ETF calculations
       - Home loan closure tips
   - Group comments into topics and provide a short summary of opinions expressed.
   - Mention any frequently discussed stocks or mutual funds by name.
   - Repeated questions should be summarized as "Multiple users asked about [topic]".
   - Group comments into topics (e.g., mutual fund returns, active vs passive investing, gold ETF calculation, home loan closure tips).
   - For each topic, give a short summary of opinions expressed.
   - Mention any frequent stock or mutual fund names discussed.

## 📊 **Sentiment Breakdown**:
   - Count and list how many comments are:
     - Positive / appreciative
     - Neutral / informational
     - Critical / challenging / sarcastic

## 🎯 **Suggestions or Challenges to Host**:
   - Identify any demands or challenges from viewers (e.g., “prove the Pattasu list beat the index”, “please show 1Y/3Y returns”)
   - Mention whether users ask for proof, data transparency, or show trust/concern.

## ❤️ **Appreciation & Praise**:
   - Highlight usernames who praised the host/channel.
   - Include emojis or regional phrases as-is (e.g., “super sir”, “vera level”, “❤️❤️🎉”)

## 📝 **General Observations**:
   - Any trends about audience expectations?
   - Are people asking for video on specific topics (e.g., bonds, BRICS currency, infra stocks)?
   - Is there trust or confusion about investment advice?

Here are the comments:

{formatted_comments}
"""
    response = model.generate_content(prompt)
    return response.text