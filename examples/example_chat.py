from src.llm.gemini_api import configure_gemini, analyze_comments_with_gemini

comments = ["Good video!", "What about Tata Motors?", "Mutual funds are better."]
configure_gemini("YOUR_GEMINI_API_KEY")
summary = analyze_comments_with_gemini(comments)
print(summary)
