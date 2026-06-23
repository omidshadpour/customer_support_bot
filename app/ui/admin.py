import streamlit as st
import requests
import uuid

API_URL = "https://om1d-customer-support-backend.hf.space"

st.set_page_config(
    page_title="Customer Support Admin",
    layout="wide"
)

st.title("🎯 Customer Support Bot — Admin Panel")

# ---- Sidebar ----

st.sidebar.header("⚙️ Settings")
company_id = st.sidebar.text_input(
    "Company_id",
    placeholder="e.g. apple, samsung, myshop",
    help="This is your unique company identifier"
)

if not company_id:
    st.info("👈 Please enter your Company ID in the sidebar to get started.")
    st.stop()

# ---- Tabs ----
tab1, tab2, tab3 = st.tabs([
    "📄 Upload Documents",
    "📊 Analytics",
    "🧪 Test Chatbot"
])

# ========================
# Tab 1: Upload Documents
# ========================

with tab1:
    st.header("Upload Documents")
    st.write("Upload your FAQ, policy, or any document you want the chatbot to learn from.")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
    )

    if uploaded_file:
        col1 , col2 = st.columns(2)

        with col1:
            st.write(f"📄 **File:** {uploaded_file.name}")
        
        with col2:
            st.write(f"📦 **Size:** {uploaded_file.size / 1024:.1f} KB")
        
        if st.button("⬆️ Upload Document" , type="primary"):
            
            with st.spinner("Uploading and processing..."):
                
                try:
                    response = requests.post(
                        f"{API_URL}/admin/upload",
                        files={"file": (uploaded_file.name , uploaded_file , "application/pdf")},
                        data={"company_id": company_id},
                        timeout=120
                    )

                    if response.status_code ==200:
                        st.success("✅ Document uploaded and processed successfully!")
                        st.info(f"Your chatbot is now ready for company: **{company_id}**")

                    else:
                        st.error(f"❌ Upload failed: {response.text}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


# ========================
# Tab 2: Analytics
# ========================

with tab2:
    st.header("Analytics")
    st.write("See what your customers are asking about.")

    if st.button("🔄 Refresh Analytics"):

        try:
            response = requests.get(
                f"{API_URL}/admin/analytics/{company_id}"
            )

            if response.status_code == 200:
                data = response.json()

                st.metric(
                    label="Total Questions Asked",
                    value=data["total_question"]
                )

                st.subheader("Recent Question")

                if data["recent_question"]:
                    for q in data["recent_question"]:

                        with st.expander(f"❓ {q['question'][:80]}..."):
                            st.write(f"**Question** {q['question']}")
                            st.write(f"**Answer** {q['answer']}")
                            st.caption(f"🕐 {q['timestamp']}")

                else:
                    st.info("No questions yet. Share your widget with customers!")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ========================
# Tab 3: Test Chatbot
# ========================

with tab3:
    st.header("Test Your Chatbot")
    st.write("Test how your chatbot responds to customer questions.")

    if "test_session_id" not in st.session_state:
        st.session_state.test_session_id = str(uuid.uuid4())

    if "test_message" not in st.session_state:
        st.session_state.test_message = []

    for msg in st.session_state.test_message:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask a test question...")

    if user_input:
        st.session_state.test_message.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):

            try:
                response = requests.post(
                    f"{API_URL}/chat/ask",
                    json={
                        "question": user_input,
                        "company_id": company_id,
                        "session_id": st.session_state.test_session_id 
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    st.write(answer)

                    sources = data.get("sources" , [])

                    if sources:
                        st.caption("📚 Sources:")
                        for s in sources:
                            st.write(f"- Page P{s['page']} | {s['source']}")

                    st.session_state.test_message.append({
                        "role": "assistant",
                        "content": answer
                    })

                else:
                    st.error("Error getting response")

            except Exception as e:
                st.error(f"Error: {str(e)}")

