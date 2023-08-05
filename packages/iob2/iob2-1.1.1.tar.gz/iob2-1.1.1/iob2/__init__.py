
# iob2コーパスの操作 [iob2]

import sys
from sout import sout
from tqdm import tqdm
from seqeval.metrics import classification_report

# iob2コーパス読み込み(文字列から) [iob2]
def loads(iob2_str):
	# 整形
	corpus = []
	rec_buff = []
	row_ls = iob2_str.split("\n")
	row_ls.append("")	# 末尾の処理用 
	for row in row_ls:
		# レコードの切れ目の場合
		if row.strip() == "":
			corpus.append(rec_buff)
			rec_buff = []
			continue
		# 通常の追加
		word, tag = row.split('\t')
		rec_buff.append((word, tag))
	return corpus

# iob2コーパス読み込み(ファイルから) [iob2]
def load(filename):
	# ファイル読み込み
	with open(filename, "r", encoding = "utf-8") as f:
		iob2_str = f.read()
	# iob2コーパス読み込み(文字列から) [iob2]
	corpus = loads(iob2_str)
	return corpus

# iob2コーパス書き出し(文字列へ) [iob2]
def dumps(corpus):
	if len(corpus) == 0: return ""
	ret_ls = []
	for rec in corpus:
		for word, tag in rec:
			ret_ls.append(word + "\t" + tag)
		ret_ls.append("")
	ret_ls.pop()	# 末尾の余分な空行を除去
	return "\n".join(ret_ls)

# iob2コーパス書き出し(ファイルへ) [iob2]
def dump(corpus, filename):
	# iob2コーパス書き出し(文字列へ) [iob2]
	iob2_str = dumps(corpus)
	# ファイル読み込み
	with open(filename, "w", encoding = "utf-8") as f:
		f.write(iob2_str)

# flatten [iob2]
def flatten(orig_ls):
	flatten_ls = []
	for ls in orig_ls:
		for e in ls:
			flatten_ls.append(e)
	return flatten_ls

# 文をいくつかずつまとめる
def chunk_combine(sent_split_corpus, chunk_len):
	sent_n = len(sent_split_corpus)
	ret_corpus = []
	chunk_buffer = []
	for i in range(sent_n):
		sent = sent_split_corpus[i]
		if len(chunk_buffer) > 0:	# 最初の文はどのみち入れるのでチェックしない
			if len(chunk_buffer) + len(sent) > chunk_len:
				ret_corpus.append(chunk_buffer)
				chunk_buffer = []
		for e in sent: chunk_buffer.append(e)
	# 最後の文の処理
	if len(chunk_buffer) > 0:
		ret_corpus.append(chunk_buffer)
		chunk_buffer = []
	return ret_corpus

# コーパスを文単位に区切り直す [iob2]
def split_sent(
	original_corpus,
	div_ls,
	chunk_len = None	# n形態素を上限としていくつかの文をまとめる (1文が長いときはchunk_nを超えることもある; None指定の場合は1文ずつ区切る)
):
	# 区切り文字一覧
	div_dic = {k:1 for k in div_ls}
	# flatten
	flatten_corpus = flatten(original_corpus)
	# 終了メタ記号を追加
	div_dic[None] = 1
	flatten_corpus.append([None, ""])
	# 構造を見ていく
	sent_split_corpus = []
	sent_buff = []
	for word, tag in flatten_corpus:
		if word is not None: sent_buff.append((word, tag))
		# 文の切れ目の場合
		if word in div_dic:
			if len(sent_buff) > 0:
				sent_split_corpus.append(sent_buff)
			sent_buff = []
	# 文をいくつかずつまとめる
	if chunk_len is None:
		return sent_split_corpus
	else:
		return chunk_combine(sent_split_corpus, chunk_len)	# 文をいくつかずつまとめる

# タグ位置を列挙するツール
def find_tags(arg_corpus, tag_name):
	if type(arg_corpus) != type([]):
		raise Exception("[find_tags() error] arg_corpusは2重のリストの形である必要があります")
	tag_ls = []
	for rec_idx, rec in enumerate(tqdm(arg_corpus)):
		# 着目タグのみのiobリストを作る
		tr_dic = {"B-"+tag_name: "b", "I-"+tag_name: "i"}
		iob_ls = [tr_dic.get(tag, "o") for word,tag in rec]
		# biiの位置をすべて特定する
		iob_ls.append("o")	# ダミー終端タグを追加 (実装を容易にするため)
		mode = "outer"
		begin_idx = None
		for w_idx,tag in enumerate(iob_ls):
			# tag終端の認識
			if mode == "inner" and tag != "i":
				tag_ls.append((rec_idx, begin_idx, len_cnt))	# 追記
				len_cnt = None
				mode = "outer"
			# tag開始の認識
			if tag == "b":
				begin_idx = w_idx
				len_cnt = 0
				mode = "inner"
			# tag内のときはlenをカウントアップ
			if mode == "inner": len_cnt += 1
	return tag_ls

# 使用されているタグ名をすべて列挙
def listup_tag_name(iob2_ls):
	if type(iob2_ls) != type([]): raise Exception("[listup_tag_name() error] arg_corpusは2重のリストの形である必要があります")
	# タグの列挙
	tag_dic = {}
	for rec in iob2_ls:
		for _, tag in rec: tag_dic[tag] = 1
	# I, Bタグの整合性の確認
	i_dic = {tag[2:]:1 for tag in tag_dic
		if tag[:2] == "I-"}
	b_dic = {tag[2:]:1 for tag in tag_dic
		if tag[:2] == "B-"}
	for i_tag in i_dic:
		if i_tag not in b_dic: raise Exception("[listup_tag_name() error] I-tag, B-tagの名前に不整合が存在します")
	return list(b_dic)

# 文の長さを揃える (BERTが文を切り落としている可能性があるため)
def cut_corpus(true_corpus, pred_corpus):
	data_n = len(true_corpus)
	ret_true_corpus = []
	error_flag = False
	for i in range(data_n):
		t, p = true_corpus[i], pred_corpus[i]
		if len(t) < len(p): raise Exception("[cut_corpus() error] 未知のエラーです")
		if len(t) > len(p): error_flag = True
		# cutして追記
		ret_true_corpus.append(t[:len(p)])
	if error_flag is True:
		print("----------")
		print("[cut_corpus() warning] BERTが文を切り落としているサンプルがあります。切り落とした範囲で評価します。")
		print("----------")
	return ret_true_corpus, pred_corpus

# 精度評価 [iob2]
def evaluate(
	arg_pred_corpus,	# 評価対象コーパス (iob2のリスト形式)
	arg_true_corpus,	# 正解コーパス (iob2のリスト形式)
	cut_corpus_flag = False,	# 文の長さを揃える機能 (BERT等を利用する場合に、長い文の冒頭・末尾が切り落とされている可能性があるため)
	ore_eval_debug = False
):
	# 文の長さを揃える (BERTが文を切り落としている可能性があるため)
	if cut_corpus_flag is True:
		true_corpus, pred_corpus = cut_corpus(arg_true_corpus, arg_pred_corpus)
	else:
		true_corpus, pred_corpus = arg_true_corpus, arg_pred_corpus
	# flatten
	flatten_true = flatten(true_corpus)	# flatten [iob2]
	flatten_pred = flatten(pred_corpus)	# flatten [iob2]
	# バグ検知
	if len(flatten_true) != len(flatten_pred): raise Exception("[iob2eval() error] 草ァ！(文の長さが不一致です)")
	# タグ部分だけ取り出し
	true_tag = [e[1] for e in flatten_true]
	pred_tag = [e[1] for e in flatten_pred]
	# debug: ORE_eval
	if ore_eval_debug is True:
		ore_ls = [(tr[0] == "B", pr[0] == "B") for tr,pr in zip(true_tag, pred_tag)]
		ore_dic = {}
		for key in ore_ls:
			if key not in ore_dic: ore_dic[key] = 0
			ore_dic[key] += 1
		print("ORE_eval:")
		sout(ore_dic)
		print("再現率: %.2f"%(ore_dic[(True,True)]/(ore_dic[(True,False)]+ore_dic[(True,True)])))
		print("適合率: %.2f"%(ore_dic[(True,True)]/(ore_dic[(False,True)]+ore_dic[(True,True)])))
	eval_result = classification_report(true_tag, pred_tag)
	return eval_result
