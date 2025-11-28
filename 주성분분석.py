import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def visualize_height_weight(df):
    plt.figure(figsize=(12, 4))  # 🔥 가로로 넓게, 세로는 얇게

    plt.scatter(df["Weight(Pounds)"], df["Height(Inches)"], alpha=0.5)
    plt.xlabel("Weight (Pounds)")
    plt.ylabel("Height (Inches)")
    plt.title("Height vs Weight")

    ax = plt.gca()

    # 데이터 범위 계산
    x_min, x_max = df["Weight(Pounds)"].min(), df["Weight(Pounds)"].max()
    y_min, y_max = df["Height(Inches)"].min(), df["Height(Inches)"].max()

    # margin (여백)
    x_margin = (x_max - x_min) * 0.15
    y_margin = (y_max - y_min) * 0.10

    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)

    # 🔥 tick 범위 넓게 (너가 보낸 이미지 스타일)
    ax.set_xticks(np.arange(int(x_min) - 20, int(x_max) + 40, 20))
    ax.set_yticks(np.arange(int(y_min) - 5, int(y_max) + 10, 2))

    # grid 적용
    ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.7)

    # 🔥 세로보다 가로가 더 긴 형태 유지
    ax.set_aspect(0.25)  # 비율 낮게 => 눕혀진 형태

    plt.tight_layout()
    plt.show()


def eigen_values_vectors(df):
    X = df[["Height(Inches)", "Weight(Pounds)"]].to_numpy()
    cov_pivot = np.cov(X.T)
    eigen_values, eigen_vectors = np.linalg.eig(cov_pivot)

    # PC1, PC2 정렬
    idx = np.argsort(eigen_values)[::-1]
    eigen_values = eigen_values[idx]
    eigen_vectors = eigen_vectors[:, idx]

    print("\n=== 고유값 (Eigenvalues) ===")
    print(" PC      Value")
    print(f" PC1   {eigen_values[0]:.6f}")
    print(f" PC2   {eigen_values[1]:.6f}")

    print("\n=== 고유벡터 (Eigenvectors) ===")
    print("           PC1        PC2")
    print(f" Height  {eigen_vectors[0,0]:.6f}  {eigen_vectors[0,1]:.6f}")
    print(f" Weight  {eigen_vectors[1,0]:.6f}  {eigen_vectors[1,1]:.6f}")

    print("\n=== 고유값 상세 ===")
    print(f"PC1 고유값 (가장 큰 축): {eigen_values[0]:.6f}")
    print(f"PC2 고유값 (잔차 축):    {eigen_values[1]:.6f}")

    print("\n=== 고유벡터 상세(각 PC가 Height/Weight에 기여하는 비율) ===")
    print("행 = 변수(Height, Weight),  열 = PC1, PC2")

    print(f"\nPC1 벡터: Height={eigen_vectors[0,0]:.6f}, Weight={eigen_vectors[1,0]:.6f}")
    print(f"PC2 벡터: Height={eigen_vectors[0,1]:.6f}, Weight={eigen_vectors[1,1]:.6f}")

    return eigen_values, eigen_vectors


if __name__ == "__main__":
    filename = "data/SOCR-HeightWeight.csv"
    df = pd.read_csv(filename)

    print("=== 데이터 미리보기 ===")
    print(df.head())

    print("\n=== 컬럼 ===")
    print(df.columns)

    eigen_values, eigenvectors = eigen_values_vectors(df)

    visualize_height_weight(df)
