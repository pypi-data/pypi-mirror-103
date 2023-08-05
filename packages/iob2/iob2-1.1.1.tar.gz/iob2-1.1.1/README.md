
English description is under construction.

## 日本語での説明
```python
import iob2
# iob2コーパス読み込み(ファイルから) [iob2]
corpus = iob2.load("./test_corpus.iob2")
# コーパスを文区切りにする
div_ls = [".", "?", "!"]	# 文区切り文字一覧
# iob2コーパス書き出し(ファイルへ) [iob2]
iob2.dump(sent_corpus, "./sent_corpus.iob2")
```
詳細な説明は執筆中です。

## ライセンスに関する注意
当ソフトウエアはクリエイティブ・コモンズライセンス(CC0)ですが、内部でMITライセンスのpypiツール`seqeval`を利用しています。
下記は`seqeval`のライセンス表示です。
```
@misc{seqeval,
  title={{seqeval}: A Python framework for sequence labeling evaluation},
  url={https://github.com/chakki-works/seqeval},
  note={Software available from https://github.com/chakki-works/seqeval},
  author={Hiroki Nakayama},
  year={2018},
}
```
