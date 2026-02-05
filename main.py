import streamlit as st
import time
import json
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

# --- UI Configuration ---
st.set_page_config(
    page_title="AI Ops Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Operations Assistant")
st.markdown("""
Welcome to your multi-agent assistant. This system uses a **Planner**, **Executor**, and **Verifier** to solve complex tasks using real-time data from GitHub, Weather, News, and more.
""")

# --- Initialize Agents ---
# We use @st.cache_resource to ensure agents aren't re-initialized on every click
@st.cache_resource
def init_agents():
    return PlannerAgent(), ExecutorAgent(), VerifierAgent()

planner, executor, verifier = init_agents()

# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Interaction Loop ---
if user_input := st.chat_input("Ask me something (e.g., 'Latest AI news and weather in Lucknow')"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Create placeholders for a professional "agentic" feel
        status_container = st.container()
        response_placeholder = st.empty()
        
        # Self-Correction Loop (Max 2 attempts for efficiency)
        current_query = user_input
        final_output = ""
        
        for attempt in range(2):
            with status_container:
                with st.status(f"Running Agent Loop (Attempt {attempt + 1})...", expanded=True) as status:
                    # 1. Planning Phase
                    st.write("🧠 **Planner**: Generating execution plan...")
                    plan = planner.create_plan(current_query)
                    
                    # 2. Execution Phase
                    st.write("⚙️ **Executor**: Calling APIs and gathering data...")
                    report = executor.execute_plan(plan)
                    
                    # 3. Verification Phase
                    st.write("🕵️ **Verifier**: Auditing results for accuracy...")
                    verification_result = verifier.verify_and_format(user_input, report)
                    
                    status.update(label="Loop Complete!", state="complete", expanded=False)

            if verification_result["status"] == "SUCCESS":
                final_output = verification_result["content"]
                break
            else:
                # SELF-CORRECTION LOGIC
                # If Verifier fails, it provides a 'retry_instruction' 
                # which we feed back into the next loop
                retry_instruction = verification_result.get("instruction", "Retry with more context")
                current_query = f"{user_input}\n\n[Previous Attempt Failed. Instruction: {retry_instruction}]"
                st.warning(f"⚠️ Retrying with more context...")
                time.sleep(1)

        # Final display
        if final_output:
            response_placeholder.markdown(final_output)
            st.session_state.messages.append({"role": "assistant", "content": final_output})
        else:
            error_msg = "❌ I'm sorry, I couldn't complete the task after multiple attempts. Please try rephrasing."
            response_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# --- Sidebar Info ---
with st.sidebar:
    st.header("System Status")
    st.success("LLM: Groq (Llama-3.3) Active")
    st.info("Tools: GitHub, Weather, News, Media")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()