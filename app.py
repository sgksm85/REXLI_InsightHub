import streamlit as st

# Homeページのコンテンツ
st.title("Welcome to REXLI InsightHub powered by Kasumi")
st.write("ここはホームページです。クライアントレポート以外のページは、工事中です。")

# クライアントレポートセクション
st.markdown("### Client Reports")
st.write("クライアント別のレポートを見ることができます")

# CSSファイルを読み込み
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSSの適用
load_css("static/styles.css")
