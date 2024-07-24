
import streamlit as st
st.title("Palindrome Checker")
a = st.text_input(label="Enter the string (name)")
if st.button("Submit"):
    try:
        name=a
        if name==name[::-1]:
            st.write("Palindrome")
        else:
            st.write("Not a Palindrome")
    except ValueError:
        st.write("Please enter a valid name (positive integer)")
