# AIテックラボ ＋ 稼ぎエンジン

このリポジトリは、ブログ「AIテックラボ」（Jekyll / GitHub Pages）と、それを Claude が毎日自動で運用する「稼ぎエンジン」のしくみをまとめたものです。

## しくみ

```
毎日 4:47（日本時間）  Claude の定期実行が起動
        │  automation/PLAYBOOK.md の手順どおりに動く
        ├─ HQ アプリから、あなたの入力（完了したタスク・指示・承認）を読む
        ├─ 稼ぎ方をリサーチして「稼ぎ案」に追加（根拠URLとスコア付き）
        ├─ ブログ記事の修正・新記事・デジタル商品づくり
        ├─ 変更をパッチにして HQ の publish に置く（このセッションは書き込み権限なし）
        └─ レポートを HQ に書き、あなたにしかできない作業を「やること」に積む

毎日 6:17 / 18:17  公開係（書き込み権限を持つ専用セッション）が起動
        └─ publish の変更を確かめて claude/kasegi-daily に push
           → GitHub Actions（auto-publish）が main にマージして Pages を再ビルド
```

- **HQ アプリ**（スマホ用の司令塔）: claude.ai の Artifact「稼ぎエンジン」。中身はオーナーだけが見られます。ソースは `hq/app.html`。
- **手順書**: `automation/PLAYBOOK.md`（定期実行の Claude が毎回読む）
- **自動公開**: `.github/workflows/auto-publish.yml`。`_posts/` `_data/` `assets/` `automation/state/` だけを変更した `[auto-publish]` 付きの push に限り、main にマージして Pages を再ビルドします。レイアウト・設定・ワークフロー・アプリ本体の変更は、人がマージするまで公開されません。
- **品質チェックリスト**: `automation/state/content-audit.md`
- **道具**: `automation/tools/`（OGP画像生成、PDF作成、ビルド確認）

## 止めたいとき

- 一時停止: claude.ai の「スケジュール済みタスク」で「稼ぎエンジン 日次サイクル」（作業）と「稼ぎエンジン 公開係」（公開）をオフにする
- 自動公開だけ止める: 「稼ぎエンジン 公開係」をオフにするか、GitHub の Actions で `auto-publish` ワークフローを無効にする

## 注意

- 収益は保証されません。登録・本人確認・税金の申告など、法律上オーナー本人が行うことは HQ の「やること」に出ます。
- 売り物のファイル（PDF など）はこの公開リポジトリには置かず、HQ の非公開アセットに保存します。
