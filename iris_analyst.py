import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

# 함수 및 클래스 , 전역 변수 생성

# 'data', 'target','target_names, 'feature_names'
#  실행문이라고 보면 됨
if __name__ == '__main__':
    # iris 꽃
    iris = load_iris()
    X = iris.data
    Coc = X.T @ X
    print(Coc) # 피버팅 된 테이블이 보이는 것이라 보면 됨(4차원 (필드))

    # 피버팅 (평점이 제일 중요함 -> 고객 성경, 상품 성격)
    # 자연어 처리 (차원을 만들어서 백터화 : Embedding 법칙)
    # print(iris)
    # print(iris.keys())
    # print(iris.data.shape) # 4차원 ->  데이터 150개 정규화 필요성
    print(iris.feature_names)
    print(iris.target_names)
    # print(iris.data)
    # print(iris.target)
#      target 이 곧 라벨링 feature -> 차원 (dimension) , 속성 (attributes), properties, key, filed 다 같은 말
