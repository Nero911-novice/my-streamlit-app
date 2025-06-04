import streamlit as st
import seaborn as sns
from app_tabs import main

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Демоверсия вероятностных законов", layout="wide")

if __name__ == "__main__":
    main()
