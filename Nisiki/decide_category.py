#pip3 install ginza
#pip3 install sklearn
#pip3 install numpy


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


    return category


def text_analyze(text):
    import collections
    
    c = collections.Counter(text)
    print(c.most_common(20))

if __name__ == '__main__':
    category = decide_category('人事さんに質問です．会社の雰囲気を改めて教えて下さい．')
    #category = analyze('同期は何人くらい居ますか？')
    #category = analyze('研修についてお聞きしたいです．')

    text_analyze('人事さんに質問です．会社の雰囲気を改めて教えて下さい．')    
