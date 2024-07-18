import streamlit as st
from main_page import main_page
from result_page import result_page

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Main Page", "Result Page"])

    if page == "Main Page":
        main_page()
    elif page == "Result Page":
        result_page()

if __name__ == "__main__":
    main()
