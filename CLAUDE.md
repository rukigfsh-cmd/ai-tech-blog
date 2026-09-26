# AIテックラボ ブログ — Claude作業ガイド

## セッション開始時の必須手順

**最初に必ず `state.json` を読む。** ファイルがあれば内容を把握してから作業を開始。なければ作業内容に応じて作成する。過去の会話履歴は読まない。

## state.json ルール

- **毎ステップ終了後、次のステップに進む前に `state.json` を更新する**
- 保存するのは「次のステップが必要とする現在の値」のみ
- 会話の要約・経緯・完了済み作業の詳細は書かない
- キー構成は毎回同じに保つ
- セッション終了時も必ず最新状態で保存する

```json
{
  "active_post": null,
  "active_post_status": null,
  "next_tasks": [],
  "recent_posts": [],
  "branch": "claude/token-savings-strategy-yfea2t",
  "notes": ""
}
```

## トークン節約ルール

1. **短く答える** — 不要な前置き・要約・説明は省く
2. **コードは差分のみ** — ファイル全体を出力しない（Editツール優先）
3. **確認は最小限** — 明らかな作業は即実行、曖昧なときだけ質問
4. **読み込みは必要箇所のみ** — `limit` と `offset` を使って部分読み込み

## このプロジェクトの基本情報

- Jekyll静的サイトジェネレータ
- 記事: `_posts/YYYY-MM-DD-タイトル.md`
- フロントマター必須: `layout`, `title`, `date`, `description`, `categories`, `tags`, `author`, `image`
- 言語: 日本語
- デプロイ先: GitHub Pages (`rukigfsh-cmd.github.io/ai-tech-blog`)
- 開発ブランチ: `claude/token-savings-strategy-yfea2t`
