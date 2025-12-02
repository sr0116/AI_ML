import requests
import pandas as pd

def fetch_sales_view_all(limit: int = 20000) -> pd.DataFrame:
    url = "http://127.0.0.1:8000/app_graphql"
    query = """
        query ($limit: Int!) {
          salesViewAll(limit: $limit) {
            # --- 공통: 요약/연도/권역/트리맵 등에서 쓰는 필드들 ---
            year
            monthNo          #  월 번호 추가 (1~12)
            monthName        # (선택) "1월", "2월" 같은 이름도 쓰고 싶으면
            salesAmount
            netProfit
            customerName
            quantity

            # 권역별 막대그래프에서 필요한 컬럼
            region
            sigungu         #  하위 시군구 필드 추가!

            #  트리맵용 3단계 계층 컬럼
            productName
            productCategoryName
            categoryName
          }
        }
        """

    resp = requests.post(url, json={'query': query, 'variables': {'limit': limit}})
    data = resp.json()
    # sales_view_json = data.get("data").get("salesViewAll") // 여러 방식으로 사용 가능
    sales_view_json = data["data"]["salesViewAll"]
    df = pd.DataFrame(sales_view_json)
    print(df)
    return df

# tolist()[0]
if __name__ == '__main__':
    df = fetch_sales_view_all()
    # df.info, duplicated
    # regions = df["region"].drop().duplicated().tolist()
    # print(regions)

    data  = df[df["reason"] == "서울"]
    print(data.shape)