import re
import pandas as pd

def delete_tag(text):
    text = re.sub(r"#.+。+", "", text)
    result = re.sub(r"#.+", "", text)
    return result

def delete_none(sr):
    tf = []
    for text in sr:
        if len(text) == 0:
            tf.append(False)
            continue
        if len(text.replace("。","")) == 0:
            tf.append(False)
        else:
            tf.append(True)
    return tf

talk = pd.read_csv("./result/sarinatalk.csv")
favorite = pd.read_csv("./result/my_favorite.csv")

out = talk.copy()
out["favorite"] = False

for index, row in talk.iterrows():
    length = len(favorite[favorite["id"] == row["id"]])
    if length == 1:
        out["favorite"].iloc[index] = True
    out["text"].iloc[index] = delete_tag(talk["text"].iloc[index])

out = out[out["name"] != "yumemita1"]
out = out[delete_none(out["text"])]
out.to_csv("./result/teaching_data.csv", index = False)