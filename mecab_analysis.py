import re
import collections
import pandas as pd
import MeCab
import matplotlib.pyplot as plt
from matplotlib import rcParams
plt.rcParams["font.family"] = "MS Gothic"

def count_words(text_list):
    mecab = MeCab.Tagger()
    result = pd.Series([])
    for text in text_list:
        word_list = extract_words(text, mecab)
        add_series = list2series(word_list)
        result = sum_series(result, add_series)

    return result


def extract_words(text, mecab):
    parses = mecab.parse(text).split("\n")
    word_list = []
    for p in parses[:-2]:
        p_split = re.split(r"[\t,]", p)
        parts = p_split[1]
        base = p_split[7]
        if parts in ["名詞", "動詞", "形容詞", "副詞"] and base != "*" and p_split[2] != "非自立":
            word_list.append(base)
    return word_list


def list2series(word_list):
    return pd.Series(collections.Counter(word_list))


def sum_series(base, add_data):
    return base.add(add_data, fill_value=int(0))

if __name__ == "__main__":
    data = pd.read_csv("./result/teaching_data.csv")
    true_data = data[data["favorite"]]
    false_data = data[~data["favorite"]]

    result_true = count_words(true_data["text"])
    result_false = count_words(false_data["text"])
    a = result_true.sort_values().iloc[-10:]
    plt.bar([i for i in range(len(a))], a)
    plt.xticks([i for i in range(len(a))], a.index)
    plt.show()
    print(result_true.sort_values())
    print(result_false.sort_values())

