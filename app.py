import streamlit as st

# Homeページの設定
st.set_page_config(page_title="Home", page_icon="🏠")

st.title("Welcome to REXLI_Innovision feat.K Project")
st.write("ここはホームページです。左のメニューからクライアントレポートページに移動してください。")

# CSSファイルを読み込み
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSSの適用
load_css("static/styles.css")
