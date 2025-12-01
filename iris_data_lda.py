import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
# 선형 분해
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler



if __name__ == "__main__":
    iris = load_iris()
    X = iris.data
    y = iris.target
    # 정규화(통계적 거리, 마할라로비스 거리) -> 실생활에서 유클리드는 잘 사용하지 않음
    X_normalized  = StandardScaler().fit_transform(X)
    # print(X_normalized)
    lda = LDA(n_components=2)
    # 새로운 행렬 만들기?? - 좌표 만들기 ??
    X_lda = lda.fit_transform(X_normalized, y)


    plt.figure(figsize=(5, 5))
    plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y, cmap='viridis', edgecolors='k', s = 100)
    plt.xlabel('First Linear Discriminant Component')
    plt.ylabel('Second Linear Discriminant Component')
    plt.title('LDA on Iris dataset')
    plt.show()