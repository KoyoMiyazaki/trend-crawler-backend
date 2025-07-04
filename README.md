# 📡 trend-crawler-backend

**Qiita**、**Zenn** から記事を定期的に収集し、**Supabase** に保存する Python バックエンドシステムです。AWS Lambda + EventBridge により自動化されており、REST API を通じて Supabase にデータを保存します。

---

## 🛠 技術スタック

| 技術            | 用途                            |
| --------------- | ------------------------------- |
| Python          | クローラ & バックエンド         |
| AWS Lambda      | 実行環境                        |
| AWS EventBridge | スケジューラ                    |
| Supabase        | データベース（PostgreSQL）+ API |
| Requests        | Supabase API 連携               |

---

## 🔐 環境変数

ローカル実行・Lambda デプロイ用に `.env` ファイルを用意してください：

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_API_KEY=your_anon_or_service_role_key

QIITA_ACCESS_TOKEN=your_qiita_access_token
```

---

## ✅ ローカル実行手順

```bash
# 仮想環境作成
python3 -m venv venv
source venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt

# 実行
PYTHONPATH=. python3 scripts/run_local.py
```

---

## ☁️ Lambda デプロイ構成

### デプロイ方法

1. `lambda_build/` ディレクトリを ZIP にまとめる
2. AWS Lambda にアップロード
3. EventBridge で定期実行を設定（例: 1 日 1 回）

### Lambda での環境変数

Lambda コンソールから次の環境変数を追加してください：

| Key                  | Value                       |
| -------------------- | --------------------------- |
| `SUPABASE_URL`       | `https://xxxxx.supabase.co` |
| `SUPABASE_API_KEY`   | `your service_role key`     |
| `QIITA_ACCESS_TOKEN` | `your qiita access_token`   |
