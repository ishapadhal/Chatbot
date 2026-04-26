import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid
#...........................utility function............................
def generate_thread_id():
    thread_id = str(uuid.uuid4())
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if 'thread_id' not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)

# st.session_state -> dict -> 

#..........................Session Setup..........................
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = []

if st.session_state['thread_id'] not in st.session_state['chat_thread']:
    add_thread(st.session_state['thread_id'])

# ---------------- CONFIG  ----------------
CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}



#..........................SidebarUI..........................
st.sidebar.title("LangGarpgh Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_thread']:
    if st.sidebar.button(thread_id,key = f"thread_{thread_id}"):
        st.session_state['thread_id'] = thread_id
        st.session_state['message_history'] = []


#........................MainUI..........................
# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    
    ai_message = response['messages'][-1].content
    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)