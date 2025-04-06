import streamlit as st
import requests
import subprocess
import threading
import time
import os
import atexit

# --- Start FastAPI Backend ---
backend_process = None

def run_fastapi():
    global backend_process
    if os.name == 'nt':
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        creationflags = 0

    backend_process = subprocess.Popen(
        ["uvicorn", "api:app", "--reload"],
        creationflags=creationflags
    )

# Gracefully shut down FastAPI when Streamlit exits
def cleanup():
    global backend_process
    if backend_process and backend_process.poll() is None:
        print("🛑 Terminating FastAPI backend...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()

atexit.register(cleanup)

# Start backend in background thread
threading.Thread(target=run_fastapi, daemon=True).start()

# Wait until backend is ready
def wait_for_backend(url="http://127.0.0.1:8000/docs", timeout=10):
    for _ in range(timeout):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ FastAPI backend is running!")
                return
        except:
            time.sleep(1)
    print("❌ FastAPI backend didn't start in time.")

wait_for_backend()

# --- Streamlit UI ---
st.set_page_config(page_title="SHL Assessment Recommender", page_icon="🔍", layout="centered")

# --- Header ---
st.markdown("""
    <h1 style='text-align: center; color: #4B8BBE;'>🔍 SHL Assessment Recommender</h1>
    <p style='text-align: center;'>Enter a short job description or hiring goal to get recommended SHL assessments.</p>
    <hr style='margin-top: 10px;'>
""", unsafe_allow_html=True)

# --- Input Box ---
with st.container():
    query = st.text_area("📝 Paste Job Description Here", height=180, placeholder="e.g., Hiring for a software engineer with problem-solving skills...")

    submit_col, _ = st.columns([1, 1])
    with submit_col:
        submit = st.button("🚀 Get Recommendations", use_container_width=True)

# --- Handle Button Click ---
if submit:
    if not query.strip():
        st.warning("⚠️ Please enter a job description before submitting.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/recommend",
                json={"query": query}
            )
            if response.status_code == 200:
                results = response.json()["results"]
                if not results:
                    st.info("ℹ️ No recommendations found for the given job description.")
                else:
                    st.success("🎯 Recommended Assessments:")
                    for res in results:
                        with st.expander(f"📌 {res['Assessment Name']}"):
                            st.markdown(f"**🔗 Link:** [{res['Assessment Name']}]({res['URL']})")
                            st.markdown(f"**📘 Test Type:** `{res['Test Type']}`")
                            st.markdown(f"**🌐 Remote Testing Support:** `{res['Remote Testing Support']}`")
                            st.markdown(f"**📊 Adaptive/IRT Support:** `{res['Adaptive/IRT Support']}`")
                            st.markdown(f"**⭐ Score:** `{res['Score']}`")
            else:
                st.error("❌ API returned an error. Please try again.")
        except Exception as e:
            st.error(f"🚫 Could not connect to API: `{e}`")
