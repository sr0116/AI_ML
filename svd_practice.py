import numpy as np
import pandas as pd
import pickle as pkl
from sklearn.decomposition import TruncatedSVD  # 제일 많이 사용
from scipy.sparse.linalg import svds

# df = pd.read_csv('data/ratings.dat', sep='::', engine='python')
# print(df)
#   컬럼 만드는 법
#     df.columns = [ 'user_id', 'movie_id', 'rating', 'timestamp']
#     df.drop(columns=['timestamp'], inplace=True)
#     df.to_pickle('data/ratings.pkl')

# # pickle 파일 만드는 법 및 조회
# df = pd.read_pickle('data/ratings.pkl')
# #  많이 본 사람을 대상으로 200명
# users = df['user_id'].value_counts().reset_index().iloc[:200, :]  # 인덱스 , 컬럼
# movies = df['movie_id'].value_counts().reset_index().iloc[:, :]  # movie는 다 가져와야 함

# data = df[(df['user_id'].isin(users['user_id'])) & (df['rating'] >= 4)]
# # print(users.shape[0]) 두개 다 같음
# # print(len(data))
# # print(data)

# pivot_df = pd.pivot_table(df, index='user_id', columns='movie_id', values='rating', aggfunc="mean")
# pivot_df.to_pickle('data/rating_pivot.pkl')

# df = pd.read_pickle('data/rating_pivot.pkl')
# # print(df.shape)
# # exit()
# means = df.mean(axis=0)
# df.fillna(means, inplace=True)
# df.to_pickle('data/rating_pivot_means.pkl')

if __name__ == '__main__':
    # 행렬이니까 X
    X = pd.read_pickle('data/rating_pivot_means.pkl').values
    # np.linalg.svd(X, full_matrices=False)
    # U, S, VT = np.linalg.svd(df, full_matrices=False)
    # svd = TruncatedSVD(n_components=2)
    # A_reduced = svd.fit_transform(X)
    # print(A_reduced.shape)

    U, S, VT = svds(X, k=5)  # 5차원으로
    D = np.diag(S)
    print(D) # 대각 행렬로
    print(S.shape)

    #  새로운 x의 레이팅 (이게 새로운 피벗 테이블)
    X_new_ratings = U@D@VT
    print(X_new_ratings)


    #     (69878, 10677)
    # (69878, 5)
    # (5,) 이것만 1차원이라 대각 행렬로 바꿔야 함
    # (5, 10677)
