import streamlit as st
import os
from urllib.parse import quote, unquote

# ページの設定を最初に行う
st.set_page_config(page_title="Client Report", page_icon="📊")

# クライアントフォルダパスの設定
base_client_folder = "data/clients"
clients = [client for client in os.listdir(base_client_folder) if os.path.isdir(os.path.join(base_client_folder, client))]

# クライアントリストをあいうえお順にソート
clients.sort(key=lambda x: x.lower())

# サイドバーにクライアント名をリンク形式で表示
st.sidebar.title("Client Reports")
for client in clients:
    client_encoded = quote(client)
    st.sidebar.markdown(f'<a href="?client={client_encoded}" target="_self">{client}</a>', unsafe_allow_html=True)

# クライアントが選択されている場合、URLパラメータから取得
query_params = st.experimental_get_query_params()
selected_client = unquote(query_params.get("client", [""])[0])

# クライアントが選択されている場合のみレポート表示
if selected_client:
    st.title(f"{selected_client} のレポート")

    # クライアントフォルダの設定
    client_folder = os.path.join(base_client_folder, selected_client)

    # 月別フォルダのリストを取得
    months = [folder for folder in os.listdir(client_folder) if os.path.isdir(os.path.join(client_folder, folder))]

    if months:
        # 月を昇順（あいうえお順）にソート
        months.sort()

        # 月を選択
        selected_month = st.selectbox("月を選択", months)

        # レポートファイルのリストを取得し、あいうえお順にソート
        month_folder = os.path.join(client_folder, selected_month)
        report_files = sorted([f for f in os.listdir(month_folder) if f.endswith('.md')])

        if report_files:
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

# JavaScriptを追加してリンクの挙動を制御
st.markdown("""
<script>
    document.addEventListener('DOMContentLoaded', (event) => {
        const sidebarLinks = document.querySelectorAll('.sidebar a');
        sidebarLinks.forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                window.history.pushState({}, '', e.target.href);
                window.location.reload();
            });
        });
    });
</script>
""", unsafe_allow_html=True)