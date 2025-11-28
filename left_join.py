from itertools import product
import pandas as pd
from unicodedata import category

if __name__ == "__main__":
    sales = pd.read_excel("data/Sales.xlsx", sheet_name="Sheet1")
    details = pd.read_excel("data/Details.xlsx", sheet_name=None)

    promotion = details['프로모션']
    channel = details['채널']
    region = details['지역']
    category = details['분류']
    product_category = details['제품분류']
    product = details['제품']
    date = details["날짜"]
    customer = details['2018년도~2022년도 주문고객']   

    # 날짜 문자열에서 변환
    date["날짜"] = pd.to_datetime(date["날짜"])

    #  merge 대상 리스트
    merge_targets = [
        (date, "날짜"),
        (product, "제품코드"),
        (customer, "고객코드"),
        (promotion, "프로모션코드"),
        (channel, "채널코드"),
        (product_category, "제품분류코드"),
        (category, "분류코드"),
        (region, "지역코드")
    ]

    #  Left Join 자동화 함수
    def left_merge(df, merge_list):
        for right, key in merge_list:
            df = df.merge(right, on=key, how="left")
        return df

    #  모든 테이블 조인 수행
    merge_df = left_merge(sales, merge_targets)

    #  필요한 컬럼만 선택
    merge_df = merge_df[[
        '날짜', '고객명', 'Quantity', '단가', '원가',
        '지역_x', '색상', '프로모션', '할인율', '채널명',
        '제품명', '제품분류명', '분류명', '시도', '구군시'
    ]]

    #  rename
    merge_df.rename({"Quantity": "수량", "지역_x": "지역"}, axis=1, inplace=True)

    #  판매량 계산
    merge_df["판매량"] = merge_df['수량'] * merge_df["단가"] * (1 - merge_df['할인율'])

    #  groupby 분석
    product_group_revenue = merge_df.groupby("제품명")['판매량'].mean().sort_values(ascending=False)

    print(product_group_revenue)
