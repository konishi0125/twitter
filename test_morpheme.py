import pandas as pd
import MeCab
from mlask import MLAsk

data = pd.read_csv("./result/teaching_data.csv")

mecab = MeCab.Tagger()
text = "今日は楽しいパーティー"

print(mecab.parse(data["text"].iloc[100]))
#print(mecab_.parse(text))


#emotion_analyzer = MLAsk()
#print(emotion_analyzer.analyze('彼のことは嫌いではない！(;´Д`)'))
#print(emotion_analyzer.analyze("今日は楽しいパーティー")["orientation"])

#print(mecab.parse(text))
