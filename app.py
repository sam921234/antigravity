import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from backend.llm_service import llm_service

# 1. Page Configuration & Aesthetic Setup
st.set_page_config(
    page_title="Vitality AI | Fitness Dashboard",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Constants
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Helper Functions for Persistence
def save_user_data(username, data):
    with open(DATA_DIR / f"{username}.json", "w") as f:
        # Convert DataFrame to dict for JSON serialization
        data_to_save = data.copy()
        data_to_save["activity_log"] = data["activity_log"].to_dict(orient="records")
        json.dump(data_to_save, f)

def load_user_data(username):
    file_path = DATA_DIR / f"{username}.json"
    if file_path.exists():
        with open(file_path, "r") as f:
            data = json.load(f)
            data["activity_log"] = pd.DataFrame(data["activity_log"])
            return data
    return None

# Load environment variables
load_dotenv()

# Custom CSS for Premium Design
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { color: #e0e0e0; }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #3d4156;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    h1, h2, h3 { color: #00ff88 !important; }
    .stButton>button {
        background-color: #00ff88;
        color: #0e1117;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00cc6a;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Login Section
if "username" not in st.session_state:
    st.title("🏋️‍♂️ Vitality AI")
    st.subheader("Please sign in to access your fitness dashboard")
    
    with st.form("login_form"):
        user_input = st.text_input("Enter your Username").strip().lower()
        login_submit = st.form_submit_button("Sign In / Register")
        
        if login_submit and user_input:
            st.session_state.username = user_input
            loaded_data = load_user_data(user_input)
            
            if loaded_data:
                st.session_state.activity_log = loaded_data["activity_log"]
                # Migration: Convert old string history to new dict format if necessary
                raw_history = loaded_data.get("coach_history", [])
                st.session_state.coach_history = [
                    msg if isinstance(msg, dict) else {"role": "assistant", "content": msg}
                    for msg in raw_history
                ]
                st.session_state.user_age = loaded_data.get("age", 25)
                st.session_state.user_goal = loaded_data.get("goal", "Stay Active")
                st.session_state.display_name = loaded_data.get("display_name", user_input.capitalize())
            else:
                st.session_state.activity_log = pd.DataFrame(columns=["Date", "Activity", "Duration", "Feeling"])
                st.session_state.coach_history = []
                st.session_state.user_age = 25
                st.session_state.user_goal = "Stay Active"
                st.session_state.display_name = user_input.capitalize()
            
            st.rerun()
    st.stop()

# 3. Sidebar - User Profile Setup
st.sidebar.title(f"👤 {st.session_state.display_name}")
user_age = st.sidebar.number_input("Age", min_value=13, max_value=100, value=st.session_state.user_age)
user_goal = st.sidebar.selectbox(
    "Fitness Goal",
    ["Build Muscle", "Lose Weight", "Endurance Training", "Stay Active", "Flexibility"],
    index=["Build Muscle", "Lose Weight", "Endurance Training", "Stay Active", "Flexibility"].index(st.session_state.user_goal)
)

if st.sidebar.button("Logout"):
    # Wipe ALL session state so no data bleeds into the next login
    st.session_state.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.info("Tip: Log your daily activity to get precise AI coaching!")

# Persistence Trigger (Save State)
user_data_to_save = {
    "display_name": st.session_state.display_name,
    "age": user_age,
    "goal": user_goal,
    "activity_log": st.session_state.activity_log,
    "coach_history": st.session_state.coach_history
}
save_user_data(st.session_state.username, user_data_to_save)

# 4. Main Dashboard Header
st.title(f"🚀 Welcome back, {st.session_state.display_name}!")
col1, col2, col3 = st.columns(3)

# Metrics calculation
total_workouts = len(st.session_state.activity_log)
total_duration = st.session_state.activity_log["Duration"].sum() if total_workouts > 0 else 0

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Workouts", total_workouts)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Minutes", f"{total_duration}m")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Fitness Goal", user_goal)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 5. Activity Log Section
tab1, tab2, tab3 = st.tabs(["📝 Log Activity", "📊 Progress View", "🤖 AI Fitness Coach"])

with tab1:
    st.subheader("Record Your Workout")
    with st.form("workout_form", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        activity = col_f1.text_input("Activity (e.g. Running, Yoga, Weights)")
        duration = col_f2.number_input("Duration (minutes)", min_value=1, value=30)
        feeling = st.select_slider("How did it feel?", options=["Tiring", "Challenging", "Good", "Easy", "Energized"])
        
        submit = st.form_submit_button("Save Entry")
        
        if submit and activity:
            new_log = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Activity": activity,
                "Duration": duration,
                "Feeling": feeling
            }])
            st.session_state.activity_log = pd.concat([st.session_state.activity_log, new_log], ignore_index=True)
            st.success(f"Successfully logged {activity}!")

with tab2:
    st.subheader("Your Journey So Far")
    if not st.session_state.activity_log.empty:
        st.dataframe(st.session_state.activity_log, use_container_width=True)
        
        # Visualization
        fig = px.area(
            st.session_state.activity_log, 
            x="Date", 
            y="Duration", 
            title="Activity Duration Trends",
            color_discrete_sequence=['#00ff88']
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Start logging your activities to see your progress charts!")

with tab3:
    col_chat_header, col_new_chat = st.columns([5, 1])
    col_chat_header.subheader("💬 Chat with Vitality AI")
    if col_new_chat.button("🗑️ New Chat", use_container_width=True):
        st.session_state.coach_history = []
        save_user_data(st.session_state.username, {
            **user_data_to_save,
            "coach_history": []
        })
        st.rerun()

    if llm_service:
        # Chat history display area
        chat_container = st.container(height=420)
        with chat_container:
            if not st.session_state.coach_history:
                st.info("👋 Hi! Ask me anything about your fitness goals, workouts, or nutrition!")
            else:
                for msg in st.session_state.coach_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

        # Contained chat input using a form (not floating)
        with st.form("chat_form", clear_on_submit=True):
            col_input, col_send = st.columns([6, 1])
            prompt = col_input.text_input(
                "Your message",
                placeholder="Ask me anything about your fitness journey...",
                label_visibility="collapsed"
            )
            send = col_send.form_submit_button("Send", use_container_width=True)

        if send and prompt:
            # Add user message
            st.session_state.coach_history.append({"role": "user", "content": prompt})

            # Get AI response
            with st.spinner("Vitality AI is thinking..."):
                user_context = {"name": st.session_state.display_name, "age": user_age, "goal": user_goal}
                response_text = llm_service.get_fitness_guidance(
                    user_context,
                    st.session_state.activity_log,
                    st.session_state.coach_history
                )

            # Add assistant message to history
            st.session_state.coach_history.append({"role": "assistant", "content": response_text})

            # Save chat history
            user_data_to_save["coach_history"] = st.session_state.coach_history
            save_user_data(st.session_state.username, user_data_to_save)
            st.rerun()
    else:
        st.warning("Please configure your GEMINI_API_KEY in the .env file to use the AI Coach.")

# 7. Safety Footer
st.sidebar.divider()
st.sidebar.caption("⚠️ **Disclaimer:** Vitality AI is for general fitness guidance only. Always consult a physician before starting a new exercise regimen.")
