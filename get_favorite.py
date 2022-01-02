import numpy as np
import pandas as pd
import get_tweet


data = pd.read_csv("./result/my_favorite.csv")
before_length = len(data)
out = pd.DataFrame(get_tweet.get_tweet_by_favorite(), columns=["name", "text", "id"])
out = out.astype({"id": np.int64})
merge_data = pd.concat([out, data])

result = merge_data[~merge_data.duplicated()]
after_length = len(result)
print(f"before:{before_length}, after:{after_length}")
result.to_csv("./result/my_favorite.csv", index=False)

