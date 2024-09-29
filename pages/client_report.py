import streamlit as st
import os
from urllib.parse import quote, unquote

# ページの設定を最初に行う
st.set_page_config(page_title="Client Report", page_icon="📊")

# クライアントフォルダパスの設定
base_client_folder = "/Users/shigikasumi/Dropbox/Projects/Projects/01_REXLI/__General_Tasks/REXLI_InsightHub/data/clients"

# クライアントリストをあいうえお順にソート
clients = [client for client in os.listdir(base_client_folder) if os.path.isdir(os.path.join(base_client_folder, client))]
clients.sort(key=lambda x: x.lower())

# サイドバーにクライアント名をリンク形式で表示（変更なし）
st.sidebar.title("Client Reports")
for client in clients:
    client_encoded = quote(client)
    st.sidebar.markdown(f'<a href="?client={client_encoded}" target="_self">{client}</a>', unsafe_allow_html=True)

# クライアントが選択されている場合、URLパラメータから取得
query_params = st.query_params
selected_client = unquote(query_params.get("client", ""))

if not selected_client:
    # クライアントが選択されていない場合のみ、メインエリアにクライアントリストを表示
    st.title("クライアントレポート")
    st.write("以下のクライアントから選択してください：")

    # クライアントリストを1列で表示
    for client in clients:
        client_encoded = quote(client)
        st.markdown(f'<a href="?client={client_encoded}" target="_self" class="main-client-link">{client}</a>', unsafe_allow_html=True)
else:
    # クライアントが選択されている場合のみレポート表示
    if selected_client not in clients:
        st.error(f"クライアント '{selected_client}' は存在しません。正しいクライアント名を選択してください。")
    else:
        st.title(f"{selected_client} のレポート")

        # クライアントフォルダの設定
        client_folder = os.path.join(base_client_folder, selected_client)
        
        # クライアントフォルダが存在するか確認
        if not os.path.exists(client_folder):
            st.error(f"クライアント '{selected_client}' のフォルダが見つかりません。")
        else:
            # 月別フォルダのリストを取得
            months = [folder for folder in os.listdir(client_folder) if os.path.isdir(os.path.join(client_folder, folder))]

            if months:
                # 月を降順（最新が上）にソート
                months.sort(reverse=True)

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



