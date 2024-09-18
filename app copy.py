import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import os
import locale

# フォントファイルのパスを指定
font_path = os.path.join(os.path.dirname(__file__), 'NotoSansCJKjp-Medium.otf')

# フォントファイルが存在する場合のみ追加
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
else:
    print(f"Font file not found at {font_path}. Using system fonts.")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

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
@st.cache_data
def load_line_friends_data():
    sheet_id = '1Aw9EBFgiYQ4G7XzX9BwhjQt0oeDK3CmeJObsi5vabFI'
    gid = '0'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url, encoding='utf-8')
    
    # '年月'列が正しく認識されていない場、列名を修正
    if '年月' not in df.columns:
        df = df.rename(columns={df.columns[0]: '年月'})
    
    df['年月'] = pd.to_datetime(df['年月'], format='%Y-%m')
    return df

df = load_line_friends_data()

# データの処理部分
latest_date = df['年月'].max()
earliest_date = latest_date - pd.DateOffset(months=5)
df_last_6_months = df[(df['年月'] >= earliest_date) & (df['年月'] <= latest_date)]

# グラフの作成と表示
clients = df_last_6_months['クライアント名'].unique()

def create_client_chart(client):
    client_data = df_last_6_months[df_last_6_months['クライアント名'] == client]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))  # グラフのサイズを調整
    
    # フォントの色を設定
    font_color = '#4A4A4A'

    # 月末有効友だち数のプロット
    line_color = '#3AC0C4'  # 線の色（青）
    fill_color = '#E8F9F9'  # 塗りつぶしの色（薄い青）
    
    line1 = ax1.plot(client_data['年月'], client_data['月末有効友だち数'], marker='o', color=line_color, label='月末有効友だち数')
    ax1.fill_between(client_data['年月'], client_data['月末有効友だち数'], color=fill_color, alpha=0.3)
    ax1.set_ylabel('月末有効友だち数', fontsize=12, color=line_color)
    ax1.tick_params(axis='y', labelcolor=line_color, labelsize=13)  # Y軸のフォントサイズを変更
    
    # 友だちのY軸の範囲を調整
    min_friends = client_data['月末有効友だち数'].min()
    max_friends = client_data['月末有効友だち数'].max()
    y_margin = (max_friends - min_friends) * 0.5  # 50%のマージン
    ax1.set_ylim(min_friends - y_margin, max_friends + y_margin)
    
    # 月間ブロック数のプロット（棒グラフ）
    ax2 = ax1.twinx()
    bar_color = '#3AC0C4'  # オレンジ色
    bar_alpha = 0.8  # 透明度
    
    # 日付を数値に変換
    dates = mdates.date2num(client_data['年月'])
    
    bar2 = ax2.bar(dates, client_data['月間ブロック数'], 
                   width=20, alpha=bar_alpha, color=bar_color, label='月間ブロック数')
    ax2.set_ylabel('月間ブロック数', fontsize=12, color=bar_color)
    ax2.tick_params(axis='y', labelcolor=bar_color, labelsize=15)  # Y軸のフォントサイズを変更
    
    # ブロック数のY軸の最大値を有効友だち数の30%に設定
    max_friends = client_data['月末有効友だち数'].max()
    ax2.set_ylim(0, max_friends * 0.3)
    
    # X軸の設定を調整
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    # グラフの幅を調整（前後に5日分の余白を追加）
    plt.xlim(earliest_date - pd.Timedelta(days=5), latest_date + pd.Timedelta(days=5))
    
    # 月の間隔を設定
    date_range = pd.date_range(start=earliest_date, end=latest_date, freq='MS')
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
    
    plt.tight_layout()  # レイアウトを自動調整
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

# クライアントごとのデータを計算する関数
def calculate_client_stats(df):
    stats = []
    for client in df['クライアント名'].unique():
        client_data = df[df['クライアント名'] == client].sort_values('年月')
        latest_friends = client_data['月末有効友だち数'].iloc[-1]
        initial_friends = client_data['月末有効友だち数'].iloc[0]
        
        # 6ヶ月間の平均友だち増加数/月を計算
        if len(client_data) > 1:
            friend_changes = client_data['月末有効友だち数'].diff()
            avg_increase = friend_changes[1:].mean()
        else:
            avg_increase = 0
        
        # 成長率を計算
        growth_rate = ((latest_friends - initial_friends) / initial_friends) * 100 if initial_friends > 0 else 0
        
        stats.append({
            'クライアント名': client,
            '最新の友だち有効数': f'{latest_friends:,}',
            '平均友だち増加数/月': f'{round(avg_increase):,}',  # 四捨五入
            '成長率(%)': f'{growth_rate:.2f}'  # 小数点以下2桁で四捨五入
        })
    
    return pd.DataFrame(stats)

# テーブルを追加
st.subheader("クライアント別統計")
client_stats = calculate_client_stats(df_last_6_months)

# CSSスタイルを適用
st.markdown("""
<style>
    .custom-table th{
        border-color: #454545 !important;
    }
            
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        color: #454545;
    }
    .custom-table th {
        text-align: center;
        background-color: #f0f2f6;
        padding: 10px;
        border: 1px solid #e0e0e0;
    }
    .custom-table td {
        text-align: right;
        padding: 10px;
        border: 1px solid #e0e0e0;
    }
    .custom-table td:first-child {
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# データフレームをHTMLに変換
html = client_stats.to_html(classes='custom-table', index=False)

# HTMLテーブルを表示
st.markdown(html, unsafe_allow_html=True)

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
