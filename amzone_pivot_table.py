
import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv("data/amazon.csv")
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    print(df['rating'])
    df["user_name"] = df["user_name"].astype(str).str.split(",")
    df_explode = df.explode("user_name")
    df_explode = df_explode.dropna(subset=["rating", "user_name"])

    # print(df.loc[0, "user_name"])
    # df.info() # type 볼 수 있음 , null 값이 있는지 없는지 볼 수 있음
    # describe() 평균, 분산, 표준 편차, 보통 통계는 이상치는 잘라내서 4분위로 잘라서 보여줌 위아래

    # exit()
    pivot_table = pd.pivot_table(
        df_explode,
        values="rating",
        columns="product_name",
        index="user_name",
        aggfunc="mean"
    #     fill_value = np.nan
    )

    means = df_explode.mean(axis=0)
    pivot_table.fillna(means, inplace=True)
    # print(means)
    print(pivot_table.iloc[:, 3].tolist())
    # print(pivot_table)

