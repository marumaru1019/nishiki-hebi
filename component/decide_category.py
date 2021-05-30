#pip3 install ginza
#pip3 install sklearn
#pip3 install numpy
#pip3 install mlask


def decide_category(text):
    import spacy
    nlp = spacy.load('ja_ginza')

    category = 'その他'
    doc = nlp.tokenizer(text)

    for token in doc:
        # token.lemma_は，分かち書きされた単語（の原型）
        # カテゴリと単語は自由に設定して下さい
    
        if token.lemma_ in {'人事'}:
            category = '人事宛'
        elif token.lemma_ in {'同期'}:
            category = '同期について'
        elif token.lemma_ in {'研修','新人研修'}:
            category = '新人研修について'
        elif token.lemma_ in {'おはよう','こんにちは','こんばんは','お疲れ','元気？'}:
            category = '挨拶'
        elif token.lemma_ in {'自己紹介'}:
            category = '自己紹介'


    return category


def text_analyze(text):
    import collections
    import spacy
    nlp = spacy.load('ja_ginza')
    doc = nlp.tokenizer(text)

    c = collections.Counter(doc)
    print(c.most_common(20))
    
    
def text_visualize(text_list):
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer
    import spacy
    nlp = spacy.load('ja_ginza')

    category = 'その他'
    POS = ['VERB', 'NOUN', 'ADJ', 'ADV', 'PROPN']
    docs = list(nlp.pipe(text_list, disable=['ner']))
    tokens = []
    for doc in docs:
        tokens.append(" ".join([token.lemma_ for token in doc if token.pos_  in POS]))
    
    NGRAM=1 # NGRAM=2なら，２単語ずつの塊を分析
    MAX_DF=0.95
    MIN_DF=0.03
    NUM_VOCAB=1000
    
    cv = CountVectorizer(ngram_range=(NGRAM,NGRAM),  max_features=NUM_VOCAB)
    X_bow = cv.fit_transform(tokens).toarray()
    vocab  = cv.vocabulary_ 

    TOP_K = 20
    sum_all = np.sum(X_bow, axis=0)
    indices_topk = np.argsort(sum_all)[::-1][:TOP_K]
    X_bow_topk = np.take(X_bow, indices_topk, axis=1)
    reverse_vocab = {vocab[k]:k for k in vocab.keys()}
    words = [reverse_vocab[i] for i in indices_topk]
    sum_group = np.sum(X_bow_topk, axis=0) 
    print(sum_group)
    
    from matplotlib import pyplot as plt
    import matplotlib as mpl
    import matplotlib.cm as cm
    from matplotlib.font_manager import FontProperties
    
    mpl.rcParams['font.family'] = 'Hiragino Maru Gothic Pro'    # WindowsならYu GothicまたはMeiryo
    left = np.array(list(range(len(words))))
    f, ax = plt.subplots(figsize=(6,3), dpi=180)
    bottom = np.zeros(len(words))
    for i in range(len(sum_group)):
        vector = sum_group[i]
        plt.bar(left, vector, bottom=bottom)

    ax.legend(loc='upper right')
    plt.xticks(left, words, rotation=290)
    plt.ylabel("出現数")
    plt.title('頻出単語')
    plt.tick_params(labelsize=6)
    plt.legend(fontsize=6)
    plt.show()
    
    
def emotion_analyzer(text):
    #ポジネガ分析をする関数(MeCabが入るなら使える)
    from mlask import MLAsk    

    # mecab -Dで辞書のパスを確認し，引数に渡す(末尾のsys.dicは削除)
    emotion_analyzer = MLAsk('-d /usr/local/lib/mecab/dic/ipadic/')
    analyze = emotion_analyzer.analyze(text)
    
    return analyze


if __name__ == '__main__':
    text_list = []
    text_list.append('人事さんに質問です．会社の雰囲気を改めて教えて下さい．')
    text_list.append('同期は何人くらい居ますか？')
    text_list.append('研修についてお聞きしたいです．')

    #category = decide_category('text_list[0])
    #category = analyze('text_list[1])
    #category = analyze('text_list[2]')

    # text_analyze(text_list[0])   

    # analyze = emotion_analyzer('ゆにしすちゃん嫌い！')
    # print(analyze)
    # print()
    # PojiNega = analyze['orientation']
    # print(PojiNega)
    
    text_visualize(text_list)
