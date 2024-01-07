import streamlit as st

# Displaying the company logo
st.image("logo.png", width=200)
st.header('CritiBot', divider='rainbow')


import random
import time
import streamlit as st

from chat_bot import CritiBot
from util import local_settings
from prompt_list import prompts

#                                                                                         
# Initialize FrontEnd App                                                                    
#                                                                                           

def initialize() -> None:
    """
    Initialize the app
    """

    with st.expander("Bot Configuration"):
        st.selectbox(label="Prompt", options=["prompt", "prompt1"])
        st.session_state.system_behavior = st.text_area(
            label="Prompt",
            value=prompts[1]["prompt1"]
        )

    st.sidebar.image("logo.png", width=100)
    st.sidebar.title("🤖 🎞️")


    if "chatbot" not in st.session_state:
        st.session_state.chatbot = CritiBot(st.session_state.system_behavior)

    with st.sidebar:
        st.markdown(
            f"ChatBot in use: <font color='green'>{st.session_state.chatbot.__str__()}</font>", unsafe_allow_html=True
        )

#                                                                                          
# Display History Message                                                                    
#                                                                                         

def display_history_messages():
    # Display chat messages from history on app rerun
    for message in st.session_state.chatbot.memory:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


####
# Display User Message                                                                       
####                                                                                        
def display_user_msg(message: str):
    """
    Display user message in chat message container
    """
    with st.chat_message("user", avatar="🧠"):
        st.markdown(message)


####                                                                                            
# Display User Message                                                                       
####                                                                                            
def display_assistant_msg(message: str, animated=True):
    """
    Display assistant message
    """

    if animated:
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()

            # Simulate stream of response with milliseconds delay
            full_response = ""
            for chunk in message.split():
                full_response += chunk + " "
                time.sleep(0.05)

                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message)


####                                                                                           
# MAIN                                                                                       
####                                                                                            
if __name__ == "__main__":
    initialize()

    # Display History 
    display_history_messages()

    if prompt := st.chat_input("Type here..."):

        #  Request & Response 
        display_user_msg(message=prompt)
        assistant_response = st.session_state.chatbot.generate_response(
            message=prompt
        )
        display_assistant_msg(message=assistant_response)


    #  Sidebar 
    with st.sidebar:
        with st.expander("Information"):
            if local_settings.OPENAI_API_KEY:
                st.write(f"🔑 Key loaded: { local_settings.OPENAI_API_KEY[0:6]}...")

            st.text("💬 MEMORY")
            st.write(st.session_state.chatbot.memory)

