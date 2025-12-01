import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



if __name__ == "__main__":
    iris = load_iris()
    X = iris.data
    y = iris.target
    # 정규화(통계적 거리, 마할라로비스 거리) -> 실생활에서 유클리드는 잘 사용하지 않음
    X_normalized  = StandardScaler().fit_transform(X)
    # print(X_normalized)
    pca = PCA(n_components=2)
    # 새로운 행렬 만들기?? - 좌표 만들기 ??
    X_pca = pca.fit_transform(X_normalized)
    # print(X_pca)
    plt.figure(figsize=(5, 5))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolors='k', s = 100)
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.title('PCA on Isis')
    plt.show()