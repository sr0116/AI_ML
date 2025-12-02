from operator import index

import numpy as np
import pandas as pd
import pickle
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error


def extract_data(df, minRating=4.0, custCount=100):
    users = df['user_id'].value_counts().reset_index().iloc[:custCount, :]  # 인덱스 , 컬럼
    movies = df['movie_id'].value_counts().reset_index().iloc[:, :]  # movie는 다 가져와야 함
    data = df[(df['user_id'].isin(users['user_id'])) & (df['rating'] >= minRating)]
    return data


def svd_predict_model(users, degree =50):
    # unique
    index = users['user_id'].unique()
    columns = users['movie_id'].unique()
    pivot_df = users.pivot_table(
        index='user_id',
        columns='movie_id',
        values='rating',
        fill_value=None
    )
    means = pivot_df.mean(axis=0)
    pivot_df.fillna(means, inplace=True)

    svd = TruncatedSVD(n_components=degree, random_state=42)
    user_svd =   svd.fit_transform(pivot_df)
    matrix = svd.components_
    rations_predict = user_svd@matrix
    df = pd.DataFrame(data=rations_predict, index=index, columns=columns)
    print(df.head())
    #  피벗 테이블 푸는 방법 stack
    # exit()
    unpivot_df = df.stack().reset_index()
    unpivot_df.columns = ['user_id', 'movie_id', 'rating']
    return unpivot_df

#  성능 지표
def performance_metrics(data):
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    predict_df = svd_predict_model(train_data) # train 데이터만 학습

    comparison_df = pd.merge(predict_df, test_data, on=['movie_id', 'user_id'], how='inner')

    actual_ratings = comparison_df['rating_y']
    predicted_ratings = comparison_df['rating_x']
    # error 찾기 오차찾기
    rmse = np.sqrt(mean_squared_error(actual_ratings, predicted_ratings))
    mae = mean_absolute_error(actual_ratings, predicted_ratings)
    return  rmse, mae
    print(rmse)


if __name__ == '__main__':
    df = pd.read_pickle('data/ratings.pkl')
    data = extract_data(df, 3.5, 300)
    rmse, mae = performance_metrics(data)
    print(rmse, mae)
    # performance_metrics(data)
    # predicts = svd_predict_model(data)
    # print(predicts.head())