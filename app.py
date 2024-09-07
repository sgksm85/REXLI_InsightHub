import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import math
import japanize_matplotlib
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np

# カスタムCSSを追加
st.markdown("""
<style>
body {
  font-family: 'Noto Sans CJK JP', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# Matplotlibのフォント設定
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['font.size'] = 15  # 基本のフォントサイズ

# Homeページのコンテンツ
st.title("Welcome to REXLI InsightHub powered by Kasumi")
st.write("ここはホームページです。クライアントレポートページ以外は、工事中です。")

# 更新情報のセクション
st.subheader("更新情報")

# 更新情報のリスト
updates = [
    {"date": "2024年9月8日", "description": "わたしが友だち推移数を追加しました。"}
]

# 更新情報の表示
for update in updates:
    st.write(f"**{update['date']}**: {update['description']}")

# 空白行を追加してセクションを分ける
st.write("")

# LINEフレンドデータの取得と表示
def load_line_friends_data():
    sheet_id = '1Aw9EBFgiYQ4G7XzX9BwhjQt0oeDK3CmeJObsi5vabFI'
    gid = '0'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url, encoding='utf-8')
    
    # 列名を確認し、必要に応じて修正
    print(df.columns)
    
    # '年月'列が正しく認識されていない場合、列名を修正
    if '年月' not in df.columns:
        df = df.rename(columns={df.columns[0]: '年月'})
    
    df['年月'] = pd.to_datetime(df['年月'], format='%Y-%m')
    return df

df = load_line_friends_data()

# 最新の日付を取得
latest_date = df['年月'].max()

# 6ヶ月前の日付を計算
six_months_ago = latest_date - pd.DateOffset(months=5)

# データを最新6ヶ月分に制限
df_last_6_months = df[df['年月'] > six_months_ago]

# グラフの作成と表示
clients = df_last_6_months['クライアント名'].unique()

def create_client_chart(client):
    client_data = df_last_6_months[df_last_6_months['クライアント名'] == client]
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 月末有効友だち数のプロット
    color1 = '#1f77b4'  # 青色
    line1 = ax1.plot(client_data['年月'], client_data['月末有効友だち数'], marker='o', color=color1, label='月末有効友だち数')
    ax1.set_ylabel('月末有効友だち数', fontsize=12, color=color1)
    ax1.tick_params(axis='y', labelcolor=color1, labelsize=10)
    
    # 友だち数のY軸の範囲を調整
    min_friends = client_data['月末有効友だち数'].min()
    max_friends = client_data['月末有効友だち数'].max()
    y_margin = (max_friends - min_friends) * 0.3  # 30%のマージン
    ax1.set_ylim(min_friends - y_margin, max_friends + y_margin)
    
    # 月間ブロック数のプロット（棒グラフ）
    ax2 = ax1.twinx()
    bar_color = '#ff7f0e'  # オレンジ色
    bar_alpha = 0.5  # 透明度
    
    # 日付を数値に変換
    dates = mdates.date2num(client_data['年月'])
    
    bar2 = ax2.bar(dates, client_data['月間ブロック数'], 
                   width=15, alpha=bar_alpha, color=bar_color, label='月間ブロック数')
    ax2.set_ylabel('月間ブロック数', fontsize=12, color=bar_color)
    ax2.tick_params(axis='y', labelcolor=bar_color, labelsize=10)
    
    # ブロック数のY軸の最大値を有効友だち数の30%に設定
    max_friends = client_data['月末有効友だち数'].max()
    ax2.set_ylim(0, max_friends * 0.3)
    
    # X軸の設定を調整
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    # グラフの幅を調整
    plt.xlim(six_months_ago - pd.Timedelta(days=15), latest_date + pd.Timedelta(days=15))
    
    # 月の間隔を狭める
    date_range = pd.date_range(start=six_months_ago, end=latest_date + pd.Timedelta(days=31), freq='MS')
    ax1.set_xticks(date_range)
    
    # X軸のラベルを回転させて重なりを防ぐ
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # タイトルとレイアウトの設定
    plt.title(client, fontsize=24, fontweight='bold', pad=20)
    ax1.tick_params(axis='x', rotation=45, labelsize=15)
    ax1.grid(True, alpha=0.3)
    
    # 凡例の設定
    lines = line1 + [bar2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=15)
    
    plt.tight_layout()
    return fig

# Streamlitアプリケーションの部分
st.subheader("クライアント別 月末有効友だち数とブロック数の推移（最新6ヶ月）")

# 2列のレイアウトを作成
col1, col2 = st.columns(2)

for i, client in enumerate(clients):
    # 偶数番目のクライアントは左列、奇数番目は右列に配置
    if i % 2 == 0:
        with col1:
            st.pyplot(create_client_chart(client))
    else:
        with col2:
            st.pyplot(create_client_chart(client))

    # 各グラフの後に余白を追加
    st.markdown("<br>", unsafe_allow_html=True)

# CSSファイルを読み込み
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSSの適用
load_css("static/styles.css")

# カスタムCSSを追加
st.markdown("""
<style>
    .stPlotlyChart {
        margin-bottom: 2rem;
    }
    .st-emotion-cache-1629p8f h1, .st-emotion-cache-1629p8f h2, .st-emotion-cache-1629p8f h3 {
        font-size: 28px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
