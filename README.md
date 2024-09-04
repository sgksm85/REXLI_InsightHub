REXLI_InsightHub/
│
├── app.py  # Home (デフォルトのページ)
└── static/
    └── styles.css  # CSSファイル
├── config.yaml               # 設定ファイル（クライアント情報、ページの設定など）
├── pages/
│   └── client_report.py  # Client Reportのページ
├── data/                     # レポートデータ
│   ├── clients/              # クライアント別データ
                └── R203_ホワイトニングカフェ/
                    ├── 2408/
                    │   ├── report1.md
                    │   ├── report2.md
                    │   ├── report3.md
                    │   ├── report4.md
                    │   └── report5.md
                    └── 2409/
                        ├── report1.md
                        ├── report2.md
                        ├── report3.md
                        ├── report4.md
                        └── report5.md
│   │   └── client_b/         # クライアントBのレポート
│   └── archived/             # アーカイブされたクライアント
│       └── client_c/         # アーカイブされたクライアントCのレポート
│
├── pages/                    # 複数ページの構成
│   ├── overview.py           # 総合ページ（全クライアントの要約など）
│   ├── client_report.py      # クライアント別レポートページのテンプレート
│   ├── industry_reports.py   # 業界レポートのページ（今後の拡張用）
│   └── case_studies.py       # 施策事例集のページ（今後の拡張用）
│
├── static/                   # 静的ファイル（CSSや画像、その他リソース）
│   └── styles.css            # カスタムCSS
│
└── utils/                    # ユーティリティ関数
    └── helpers.py            # ページ生成やデータ読み込みのヘルパー関数
