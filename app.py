import streamlit as st

# Homeページの設定
st.set_page_config(page_title="Home", page_icon="🏠")

st.title("Welcome to REXLI Insight hub feat.Kasumi")
st.write("ここはホームページです。左のメニューからクライアントレポートページに移動してください。他のページは、工事中です。")

# CSSファイルを読み込み
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSSの適用
load_css("static/styles.css")
