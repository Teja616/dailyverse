# DailyVerse ✨

## Your Personal AI Content Companion

### Live Site Link : https://dailyverse-hackhazards.streamlit.app/

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22%2B-FF4B4B)

In an age of overwhelming digital clutter, DailyVerse transforms how you consume content by delivering personalized, AI-generated creations straight to your inbox daily.



## 🌟 Features

- **Diverse Content Generation**: Create personalized stories, poems, blog posts, character backstories, puzzles, and more
- **News Digest with Real-Time Data**: Get a curated "Top 5 News Digest" powered by Tavily search integration
- **Multiple LLM Options**: Choose from various Groq-powered models including Llama 3.3, Mistral, Gemma, and more
- **Automated Email Delivery**: Schedule personalized content to arrive in your inbox every morning
- **Beautiful Email Format**: Receive aesthetically designed HTML emails that make your content shine
- **Firebase Backend**: User preferences and subscription details securely stored for consistent delivery

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Groq API key
- Tavily API key (for news integration)
- Firebase account and credentials
- SMTP email account for sending emails

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dailyverse.git
   cd dailyverse
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   EMAIL_HOST=your_email_address
   EMAIL_PASSWORD=your_email_password
   EMAIL_SERVER=smtp.yourserver.com
   EMAIL_PORT=587
   ```

4. Add your Firebase credentials as `firebase_config.json` in the project root

### Running the App

```bash
streamlit run app.py
```

## 🖼️ How It Works

1. **Select Your Content**: Choose from multiple content types to receive
2. **Provide a Prompt**: Enter a text prompt or theme for your content
3. **Choose Your Model**: Select your preferred Groq LLM model
4. **Schedule Delivery**: Opt-in for daily delivery or get a one-time email
5. **Enjoy Your Content**: Check your inbox for beautifully formatted personalized content

## 📚 Content Types

- **Personalized Story**: Unique tales inspired by your prompt
- **Themed Blog Post**: Informative articles on your chosen topic
- **Poem or Haiku**: Creative verses tailored to your theme
- **Character Backstory**: Detailed character backgrounds for storytelling or roleplaying
- **Dream Interpretation**: Imaginative analysis of dream themes
- **Daily Puzzle**: Brain teasers and riddles to start your day
- **Top 5 News Digest**: Real-time news curated around your interests
- **Fun Facts & Mini Lessons**: Learn something new every day

## 🛠️ Technologies

- **Streamlit**: For the intuitive user interface
- **LangChain & Groq**: For powerful LLM content generation
- **Firebase**: For user data storage and subscription management
- **Tavily Search API**: For real-time news and information retrieval
- **Python SMTP**: For email delivery

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Created for HackHazards India
- Powered by Groq LLMs
- News integration via Tavily Search API

---

DailyVerse - Transform your daily scroll into a daily spark! ✨
