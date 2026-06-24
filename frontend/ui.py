import streamlit as st
import requests
from datetime import datetime, UTC
import time
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="chatbot_",
    password="your-secret-password"
)

if not cookies.ready():
    st.stop()
    
def stream_text(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.03)
        
API_BASE = "http://backend:8000"

if "token" not in st.session_state:
    st.session_state.token = cookies.get("token")
    
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# AUTH FUNCTIONS
def login(username, password):
    try:
        res = requests.post(f"{API_BASE}/api/v1/auth/login", json={
            "username": username,
            "password": password
        })

        data = res.json() if res.content else {}

        if res.status_code == 200:
            token = data.get("access_token")

            if not token:
                st.error("Login failed: No token returned")
                return

            st.session_state.token = token
            cookies["token"] = token
            cookies.save()

            st.success("Login successful 🎉")
            st.rerun()

        else:
            error_msg = data.get("detail") or data.get("message") or "Invalid credentials"
            st.error(f"Login failed: {error_msg}")

    except Exception as e:
        st.error(f"Login error: {str(e)}")
        
def register(username, password):
    try:
        res = requests.post(f"{API_BASE}/api/v1/auth/register", json={
            "username": username,
            "password": password
        })

        data = res.json() if res.content else {}

        if res.status_code == 200 or res.status_code == 201:
            st.success("Account created successfully 🎉 Please login.")
            st.info("You can now switch to Login tab.")

        else:
            error_msg = data.get("detail") or data.get("message") or "Register failed"
            st.error(f"Register failed: {error_msg}")

    except Exception as e:
        st.error(f"Register error: {str(e)}")
        
# SESSION API
def get_conversations():
    res = requests.get(
        f"{API_BASE}/api/v1/conversations",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )

    if res.status_code != 200:
        st.error(res.text)
        return []

    return res.json()

def create_conversation():
    res = requests.post(
        f"{API_BASE}/api/v1/conversations",
        json={},
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )

    if res.status_code != 200:
        st.error(f"Create session failed: {res.text}")
        return None

    return res.json()

def delete_conversation(conversation_id):
    response = requests.delete(
        f"{API_BASE}/api/v1/conversations/{conversation_id}",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    print(response.status_code, response.text)

# CHAT API
def send_message(conversation_id, message):
    res = requests.post(
        f"{API_BASE}/api/v1/messages/chat/",
        json={
            "query": message,
            "conversation_id": conversation_id
        },
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )

    if res.status_code != 200:
        st.error(res.text)
        return None

    return res.json().get("content") or res.json().get("answer")

def get_messages(conversation_id):
    res = requests.get(
        f"{API_BASE}/api/v1/messages/messages/{conversation_id}",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )

    if res.status_code != 200:
        return []

    return res.json()

# LOGIN UI
if not st.session_state.token:
    st.title("🔐 Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            login(username, password)
            st.rerun()

    with tab2:
        username = st.text_input("Username", key="reg_user")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            register(username, password)

    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.token = None

    cookies["token"] = ""
    cookies.save()

    st.rerun()
# SIDEBAR (SESSIONS)
st.sidebar.title("💬 Conversations")

if st.sidebar.button("➕ New Chat"):
    new_s = create_conversation()

    if not new_s:
        st.error("Create conversation failed (no response)")
        st.stop()

    conversation_id = new_s.get("conversation_id") if isinstance(new_s, dict) else new_s

    if not conversation_id:
        st.error(f"Invalid conversation response: {new_s}")
        st.stop()

    st.session_state.current_conversation = conversation_id
    st.session_state.messages = []
    st.rerun()


conversations = get_conversations()

if not isinstance(conversations, list):
    st.sidebar.error("Invalid conversations data")
    st.sidebar.write(conversations)
    st.stop()


for s in conversations:
    if not isinstance(s, dict):
        continue

    conversation_id = s.get("conversation_id")
    if not conversation_id:
        continue

    conversation_id = str(conversation_id)

    col1, col2 = st.sidebar.columns([4, 1])

    created_at = s.get("created_at", "")
    if created_at:
        dt = datetime.fromisoformat(created_at)
        dt = dt.astimezone()
        formatted_time = dt.strftime("%d/%m %H:%M")
    else:
        formatted_time = "No time"
    label = f"{conversation_id[:8]} | {formatted_time}"

    if col1.button(label, key=f"open_{conversation_id}"):
        st.session_state.current_conversation = conversation_id
        st.session_state.messages = get_messages(conversation_id)
        st.rerun()

    if col2.button("❌", key=f"del_{conversation_id}"):
        delete_conversation(conversation_id)
        st.rerun()

# MAIN CHAT UI
st.title("🤖 AI Chatbot")

if not st.session_state.current_conversation:
    st.info("Select or create a chat session")
    st.stop()

for msg in st.session_state.messages:
    created_at = msg.get("created_at")

    if created_at:
        dt = datetime.fromisoformat(created_at)
        dt = dt.astimezone()
        time_text = dt.strftime("%H:%M")
    else:
        time_text = ""

    with st.chat_message(msg["role"]):

        cols = st.columns([8, 2])

        with cols[0]:
            st.write(msg["content"])

        with cols[1]:
            st.caption(time_text)

user_input = st.chat_input("Type your message...")

if user_input:
    if not st.session_state.messages:
        st.session_state.messages = []

    st.session_state.messages.append({
    "role": "user",
    "content": user_input,
    "created_at": datetime.now(UTC).isoformat()
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        answer = send_message(
            st.session_state.current_conversation,
            user_input
        )

    if answer is None:
        st.error("No response from server")
        st.stop()

    st.session_state.messages.append({
    "role": "assistant",
    "content": answer,
    "created_at": datetime.now(UTC).isoformat()
    })

    with st.chat_message("assistant"):
        streamed_text = st.write_stream(stream_text(answer))