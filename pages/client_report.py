# Client report template
import streamlit as st
import os
from urllib.parse import quote, unquote
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(page_title="Client Report", page_icon="📊")

# JavaScriptを使ってページのトップにスクロール
scroll_js = """
<script>
    setTimeout(function() {
        window.scrollTo(0, 0);
    }, 100); // ページが完全にロードされてからスクロール
</script>
"""
components.html(scroll_js)

# クライアントのフォルダパス
base_client_folder = "data/clients"
clients = [client for client in os.listdir(base_client_folder) if os.path.isdir(os.path.join(base_client_folder, client))]

# サイドバーにクライアント名をリンク形式で並べて表示
st.sidebar.title("Client Reports")
for client in clients:
    client_encoded = quote(client)
    st.sidebar.markdown(f"[{client}](?client={client_encoded})", unsafe_allow_html=True)

# クライアントが選択されている場合、URLパラメータから取得
query_params = st.experimental_get_query_params()
selected_client = unquote(query_params.get("client", [""])[0])

if selected_client:
    st.title(f"{selected_client} のレポート")

    # クライアントのフォルダパスを設定
    client_folder = os.path.join(base_client_folder, selected_client)

    # 月別フォルダのリストを取得
    months = [folder for folder in os.listdir(client_folder) if os.path.isdir(os.path.join(client_folder, folder))]

    if months:
        # 月別フォルダを選択
        selected_month = st.selectbox("月を選択", months)

        # 選択された月のフォルダパスを設定
        month_folder = os.path.join(client_folder, selected_month)

        # 月のフォルダ内のレポートファイルを取得し、あいうえお順に並べ替え
        report_files = sorted([f for f in os.listdir(month_folder) if f.endswith('.md')])

        # レポートを選択
        selected_report = st.selectbox("レポートを選択", report_files)

        # 選択されたレポートを表示
        report_path = os.path.join(month_folder, selected_report)
        with open(report_path, 'r') as file:
            report_content = file.read()

        st.markdown(report_content)

# CSSファイルを読み込み
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSSの適用
load_css("static/styles.css")



