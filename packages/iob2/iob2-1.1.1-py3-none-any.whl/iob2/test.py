
# iob2コーパスの操作 [iob2]
# 【動作確認 / 使用例】

import sys
from sout import sout
from relpath import add_import_path
add_import_path("../")
# iob2コーパスの操作 [iob2]
import iob2

# iob2コーパス読み込み(ファイルから) [iob2]
corpus = iob2.load("./test_corpus.iob2")
# 結果確認
sout(corpus)

# コーパスを文区切りにする
div_ls = [".", "?", "!"]	# 文区切り文字一覧
sent_corpus = iob2.split_sent(corpus, div_ls)	# コーパスを文単位に区切り直す [iob2]
# 結果確認
sout(sent_corpus)

# iob2コーパス書き出し(ファイルへ) [iob2]
iob2.dump(sent_corpus, "./sent_corpus.iob2")
