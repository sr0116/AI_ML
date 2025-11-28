import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def visualize_height_weight(df):
    plt.figure(figsize=(7, 7))
    plt.scatter(df["Weight(Pounds)"], df["Height(Inches)"], alpha=0.7)
    plt.xlabel("Weight (Pounds)")
    plt.ylabel("Height (Inches)")
    plt.title("Height vs Weight")

    ax = plt.gca()

    # 데이터 범위 계산
    x_min, x_max = df["Weight(Pounds)"].min(), df["Weight(Pounds)"].max()
    y_min, y_max = df["Height(Inches)"].min(), df["Height(Inches)"].max()

    # 10% 여유 범위
    x_margin = (x_max - x_min) * 0.1
    y_margin = (y_max - y_min) * 0.1

    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)

    #  grid 간격을 크게 설정 (tick interval 크게設定)
    x_ticks = np.arange(int(x_min) - 20, int(x_max) + 20, 20)
    y_ticks = np.arange(int(y_min) - 5, int(y_max) + 5, 2)

    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # grid 표시
    ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

    # 축 단위 동일하게
    ax.set_aspect("equal", adjustable="box")

    plt.show()


def eigen_values_vectors(df):
    X = df[["Weight(Pounds)", "Height(Inches)"]].to_numpy()
    cov_pivot = np.cov(X.T)
    return np.linalg.eig(cov_pivot)


if __name__ == "__main__":
    filename = "data/SOCR-HeightWeight.csv"
    # df = pd.read_csv(filename)

    lists = [
        ["홍길동", 90, 85, 92, 88],
        ["이순신", 80, 95, 78, 85],
        ["신사임당", 100, 92, 89, 94],
        ["강감찬", 88, 76, 90, 82]
    ]

    df = pd.DataFrame(lists, columns=["이름", "국어", "영어", "수학", "과학"])
    print(df)

    # axis=0 : 각 열(column)별 합 (행을 따라 내려가면서 더함)
    print(df.sum(axis=0))

    # axis=1 : 각 행(row)별 합 (열을 따라 가로로 더함)
    # print(df.sum(axis=1))
    df.iloc[0, 0] = df.iloc[0, 0]
    print(df)
    # axis=0 : 행 삭제
    # print(df.drop("홍길동", axis=0))

    # axis=1 : 열 삭제
    # print(df.drop("영어", axis=1))

    # lists = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

    # print(df[df[lists]].isin([1]))
    # 조건문
    # table = df[df["Weight(Pounds)"] >= 150]
    # print(table.head())
    exit()

    visualize_height_weight(df)

    eigen_values, eigenvectors = eigen_values_vectors(df)
    print("Eigenvalues:\n", eigen_values)
    print("Eigenvectors:\n", eigenvectors)