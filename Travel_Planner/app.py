# app.py

import streamlit as st
from langchain_core.messages import HumanMessage
from main import graph  

st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("🧭 AI Travel Planner")
st.write("Plan your trip with the help of an AI team of travel experts!")

user_input = st.text_input("Where do you want to go and what is your budget?", placeholder="E.g., I want to visit Islamabad with a budget of Rs5000")

if st.button("Plan my trip") and user_input:
    with st.spinner("Planning your trip..."):
        final_state = graph.invoke({
        "messages": [HumanMessage(content=user_input)],
        "next": "supervisor"
    })

        final_output = final_state["messages"][-1].content if "messages" in final_state else None

    if final_output:
        st.success("Here's your travel plan!")
        st.markdown(final_output, unsafe_allow_html=True)

    else:
        st.error("Sorry, I couldn't generate a plan. Try again or rephrase your request.")

