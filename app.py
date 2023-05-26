import streamlit as st
from streamlit_chat import message
import pickle
import os
from utils.query import get_chain


# Open vectorstore with documenation data
if os.path.exists("vectorstore.pkl"):
    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)

        
# Get the chain (see utils/query.py)
chain = get_chain(vectorstore)


# Streamlit App

# Session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "history" not in st.session_state:
    st.session_state["history"] = []

# Title
st.title("Telnyx SMS Guidelines Assistant")

# Description
st.markdown(
        ''' 
        > :blue[**An AI chatbot built with LangChain, OpenAI GPT-3.5 and Streamlit
        > that can assist customers with the guidelines for sending SMS to each country with Telnyx**]
        ''')

# Input bar
def get_text():
    input_text = st.text_input(
        "You:", 
        value="", 
        key="input",
        placeholder="Enter your question here",
        label_visibility="hidden"
        )
    return input_text

user_input = get_text()

# Generate output upon user input
if user_input:

    # Generate output
    output = chain.run(
        chat_history=st.session_state["history"],
        question=user_input
    )
    
    # Update session states
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    st.session_state.history.append((user_input, output))

    # Display output in chatbot
    if st.session_state["generated"]:

        # loop backwards in the generated list
        for i in range(len(st.session_state["generated"]) -1, -1, -1):

            # Using the streamlit-chat library "message" function
            # dispay the output generated by the chatbot
            message(st.session_state["generated"][i], key=str(i))
            # display the past input from the user
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            
