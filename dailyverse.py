import streamlit as st
from PIL import Image
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os
import schedule
import time

# Updated imports for the latest LangChain version
from langchain_groq import ChatGroq
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables (if using .env)
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")  # Added Tavily API key

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        # Try to use streamlit secrets (for deployment)
        firebase_creds = dict(st.secrets["firebase"])
        cred = credentials.Certificate(firebase_creds)
    except:
        # Fall back to file for local development
        cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize session state variables if they don't exist
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False

# --- Page Config ---
st.set_page_config(page_title="DailyVerse", page_icon="✨", layout="centered")

# --- Title ---
st.title("🌟 Welcome to DailyVerse")
st.markdown("Create your own daily personalized content using text or images.")

# --- Sidebar ---
st.sidebar.header("📋 Customize Your DailyVerse")

# Email input
user_email = st.sidebar.text_input("📧 Enter your email for delivery:", placeholder="you@example.com")

# Select content types
content_options = st.sidebar.multiselect(
    "Choose content to receive:",
    [
        "Personalized Story",
        "Themed Blog Post",
        "Poem or Haiku",
        "Character Backstory",
        "Dream Interpretation",
        "Daily Puzzle",
        "Top 5 News Digest",
        "Fun Facts & Mini Lessons"
    ],
    default=["Personalized Story"]
)

# Groq Model Selector
model_choice = st.sidebar.selectbox(
    "🧠 Choose your LLM Model:",
    ["llama-3.3-70b-versatile","llama3-70b-8192", "mistral-saba-24b", "gemma-9b-it","deepseek-r1-distill-llama-70b","qwen-2.5-32b"],
    help="Choose your preferred LLM model for content generation."
)

# Option for daily delivery
daily_delivery = st.sidebar.checkbox("📬 Opt-in for daily content delivery")

# Initialize Tavily Search Tool
def get_tavily_search_tool():
    try:
        # Updated to use the newer TavilySearchResults tool
        return TavilySearchResults(api_key=tavily_api_key)
    except Exception as e:
        st.error(f"Error initializing Tavily search: {e}")
        return None

# --- Generate news digest using Tavily Search ---
def generate_news_digest(prompt):
    try:
        search_tool = get_tavily_search_tool()
        if not search_tool:
            return "Unable to generate news digest due to search service error."
        
        # Extract topic from prompt
        search_topic = prompt.strip()
        if not search_topic:
            search_topic = "current events"
        
        # Initialize the LLM
        llm = ChatGroq(
            temperature=0.5,
            model_name=model_choice,
            groq_api_key=groq_api_key
        )
        
        # Create the search chain using the newer LangChain structure
        template = """
        Based on the following search results, create a concise "Top 5 News Digest" on the topic of {topic}.
        
        For each news item:
        1. Include a catchy headline
        2. Write a brief 2-3 sentence summary
        3. Include the source and publication date if available
        
        Format it as a clean, easy-to-read digest with numbered items.
        
        SEARCH RESULTS:
        {search_results}
        """
        
        prompt_template = ChatPromptTemplate.from_template(template)
        
        # Create the chain using the newer functional approach
        search_chain = (
            {"topic": lambda x: x, "search_results": lambda x: search_tool.invoke(x)}
            | prompt_template
            | llm
            | StrOutputParser()
        )
        
        # Execute the chain
        news_digest = search_chain.invoke(search_topic)
        return news_digest
    
    except Exception as e:
        return f"Unable to generate news digest. Error: {str(e)}"

# --- Backend Placeholder (LangChain + Groq) ---
def generate_content(prompt, content_type, model_choice):
    # Special handling for news digest
    if content_type == "Top 5 News Digest":
        return generate_news_digest(prompt)
    
    # Standard content generation for other types
    llm = ChatGroq(
        temperature=0.7,
        model_name=model_choice,
        groq_api_key=groq_api_key
    )
    
    # Use the newer message format
    messages = [
        SystemMessage(content=f"You are an expert at creating {content_type.lower()}. Make it engaging and relevant to the prompt."),
        HumanMessage(content=f"Generate a {content_type.lower()} based on this prompt: {prompt}")
    ]
    
    return llm.invoke(messages).content

# --- Enhanced Email System ---
def send_email(recipient, content_dict, model_used):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "🌟 Your DailyVerse Magic Has Arrived!"
    msg['From'] = os.getenv("EMAIL_HOST")
    msg['To'] = recipient

    # Get current date for the email
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    # Enhanced HTML template with better styling
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 650px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #6C63FF 0%, #4834d4 100%);
                color: white;
                padding: 25px;
                border-radius: 15px 15px 0 0;
                text-align: center;
                margin-bottom: 0;
            }}
            .content {{
                background-color: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-top: none;
                border-radius: 0 0 15px 15px;
                padding: 20px 25px;
            }}
            .content-item {{
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            }}
            h2 {{
                margin-top: 0;
                font-weight: 600;
            }}
            h3 {{
                color: #6C63FF;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 0.9em;
                color: #666;
            }}
            .date {{
                color: white;
                opacity: 0.9;
                font-size: 1.1em;
                margin-top: 5px;
            }}
            .model-info {{
                color: #666;
                font-size: 0.85em;
                font-style: italic;
                text-align: right;
            }}
            .news-item {{
                border-left: 3px solid #6C63FF;
                padding-left: 15px;
                margin-bottom: 15px;
            }}
            .news-headline {{
                font-weight: bold;
                color: #333;
                margin-bottom: 5px;
            }}
            .news-source {{
                font-style: italic;
                color: #666;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>✨ Your DailyVerse Magic ✨</h2>
            <div class="date">{current_date}</div>
        </div>
        <div class="content">
            <p>Here's your uniquely crafted content, made just for you:</p>
    """
    
    # Add each content item with enhanced styling
    for title, body in content_dict.items():
        # Special formatting for news digest
        if title == "Top 5 News Digest":
            html_content += f"""
                <div class="content-item">
                    <h3>📰 {title}</h3>
                    <div>{format_news_digest(body)}</div>
                </div>
            """
        else:
            html_content += f"""
                <div class="content-item">
                    <h3>💫 {title}</h3>
                    <div>{body.replace('\n', '<br>')}</div>
                </div>
            """
    
    html_content += f"""
            <div class="model-info">Generated using {model_used}</div>
            <div class="footer">
                <p>Made with ❤️ by DailyVerse | For HackHazards India</p>
                <p>Want more? Check your email tomorrow for fresh content!</p>
            </div>
        </div>
    </body>
    </html>
    """

    part = MIMEText(html_content, 'html')
    msg.attach(part)

    with smtplib.SMTP(os.getenv("EMAIL_SERVER"), int(os.getenv("EMAIL_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_HOST"), os.getenv("EMAIL_PASSWORD"))
        server.sendmail(msg['From'], recipient, msg.as_string())

# Helper function to format news digest for better display
def format_news_digest(content):
    # Try to identify news items and format them with special styling
    formatted_content = content
    
    # Look for numbered items (1., 2., etc.) and apply formatting
    import re
    news_pattern = r'(\d+\.\s*)(.*?)(?=\d+\.|$)'
    
    def replace_with_formatting(match):
        number = match.group(1)
        content = match.group(2).strip()
        
        # Try to extract headline and source if available
        headline_match = re.search(r'^(.*?)(?:\(|Source:|From:)', content)
        if headline_match:
            headline = headline_match.group(1).strip()
            rest = content[len(headline):].strip()
            
            return f'<div class="news-item"><div class="news-headline">{number}{headline}</div>{rest}</div>'
        else:
            return f'<div class="news-item"><div class="news-headline">{number}</div>{content}</div>'
    
    formatted_content = re.sub(news_pattern, replace_with_formatting, content, flags=re.DOTALL)
    
    return formatted_content

# --- Daily Scheduled Job ---
def send_daily_verse():
    users_ref = db.collection("dailyverse_users")
    docs = users_ref.stream()
    for doc in docs:
        data = doc.to_dict()
        if data.get("subscribed"):
            prompt = data.get("prompt")
            email = data.get("email")
            types = data.get("content_types", [])
            model = data.get("model_choice", "llama-3.3-70b-versatile")
            content_dict = {t: generate_content(prompt, t, model) for t in types}
            send_email(email, content_dict, model)

# Schedule daily job (run this in a background process or server environment)
schedule.every().day.at("08:00").do(send_daily_verse)  # 8:00 AM daily

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Only show input area if email hasn't been sent
if not st.session_state.email_sent:
    # Input area
    st.subheader("🎨 Your Input")
    
    # Change prompt description based on content selection
    prompt_description = "Enter a text prompt:"
    if "Top 5 News Digest" in content_options and len(content_options) == 1:
        prompt_description = "Enter a news topic (or leave blank for general news):"
    
    user_prompt = st.text_area(prompt_description, placeholder="Describe your mood, an idea, or a scene...")
    uploaded_image = st.file_uploader("Or upload an image:", type=["jpg", "jpeg", "png"])

    # --- Generate Button ---
    if st.button("🚀 Generate & Send DailyVerse"):
        if not user_email:
            st.warning("Please enter your email address.")
        elif not user_prompt and not uploaded_image:
            st.warning("Please provide a prompt or upload an image.")
        else:
            with st.spinner(f"✨ Crafting your personalized content with {model_choice}..."):
                try:
                    generated_content = {}
                    
                    # Check if Tavily API Key is available when News Digest is selected
                    if "Top 5 News Digest" in content_options and not tavily_api_key:
                        st.warning("⚠️ Tavily API Key not found. News digest will use AI-generated content instead of real-time news.")
                    
                    for content in content_options:
                        with st.status(f"Generating {content}..."):
                            generated_content[content] = generate_content(user_prompt, content, model_choice)

                    send_email(user_email, generated_content, model_choice)
                    
                    # Update session state
                    st.session_state.email_sent = True
                    
                    # Store to Firebase for daily delivery tracking
                    if daily_delivery:
                        db.collection("dailyverse_users").document(user_email).set({
                            "email": user_email,
                            "prompt": user_prompt,
                            "content_types": content_options,
                            "model_choice": model_choice,
                            "subscribed": True,
                            "timestamp": datetime.datetime.utcnow().isoformat()
                        })
                    
                    # Force a rerun to refresh the page and hide the input fields
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
else:
    # Show success message after email is sent
    st.success("✅ Your DailyVerse has been sent to your email! Check your inbox shortly.")
    
    # Show subscription info if applicable
    if daily_delivery:
        st.info("🔄 You're now subscribed for daily content delivery! Same content types will be sent daily at 8:00 AM.")
    
    # Button to create a new DailyVerse
    if st.button("✨ Create Another DailyVerse"):
        st.session_state.email_sent = False
        st.rerun()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for HackHazards India")