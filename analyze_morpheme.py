import pandas as pd
from mlask import MLAsk

data = pd.read_csv("./result/teaching_data.csv")
emotion_analyzer = MLAsk()

no_count = 0
score = 0
pos = 0
nega = 0
neutral = 0
favo_pos = 0
favo_nega = 0
favo_neutral = 0

for index, sr in data.iterrows():
    text = sr["text"]
    if text == "":
        continue
    result = emotion_analyzer.analyze(text)
    if len(result) == 2:
        no_count += 1
        continue
    if result["orientation"] == "POSITIVE":
        if sr["favorite"] is True:
            favo_pos += 1
        elif sr["favorite"] is False:
            pos += 1
    elif result["orientation"] == "NEGATIVE":
        if sr["favorite"] is True:
            favo_nega += 1
        elif sr["favorite"] is False:
            nega += 1
    elif result["orientation"] == "NEUTRAL":
        if sr["favorite"] is True:
            favo_neutral += 1
        elif sr["favorite"] is False:
            neutral += 1

sum = pos + nega + neutral
favo_sum = favo_pos + favo_nega + favo_neutral
print(f"no_count={no_count}, count={sum+favo_sum}")
print(f"pos={pos/sum}, nega={nega/sum}, neutral={neutral/sum}")
print(f"pos={favo_pos/favo_sum}, nega={favo_nega/favo_sum}, neutral={favo_neutral/favo_sum}")
print(f"pos={pos}, nega={nega}, neutral={neutral}")
print(f"pos={favo_pos}, nega={favo_nega}, neutral={favo_neutral}")
