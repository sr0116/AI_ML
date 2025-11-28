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
    # 날짜 문자열에서 변환
    date["날짜"] = pd.to_datetime(date["날짜"])
    customer = details['2018년도~2022년도 주문고객']
    merge_df = pd.merge(sales, date, on="날짜", how="left")
    merge_df = pd.merge(merge_df, product, on="제품코드", how="left")
    merge_df = pd.merge(merge_df, customer, on="고객코드", how="left")
    merge_df = pd.merge(merge_df, promotion, on="프로모션코드", how="left")
    merge_df = pd.merge(merge_df, channel, on="채널코드", how="left")
    merge_df = pd.merge(merge_df, product_category, on="제품분류코드", how="left")
    merge_df = pd.merge(merge_df, category, on="분류코드", how="left")
    merge_df = pd.merge(merge_df, region, on="지역코드", how="left")
    # print(merge_df.keys())
    # print(date.keys())
    merge_df = merge_df[[
        '날짜', '고객명', 'Quantity', '단가', '원가',
        '지역_x', '색상', '프로모션', '할인율', '채널명',
        '제품명', '제품분류명', '분류명', '시도', '구군시'
    ]]
    merge_df.rename({"Quantity" : "수량", "지역_x" : "지역"}, axis=1, inplace=True)
    merge_df["판매량"] = merge_df['수량'] * merge_df["단가"] * (1 - merge_df['할인율'])
    product_group_revenue = merge_df.groupby("제품명")['판매량'].sum().sort_values(ascending=False)
    # print(merge_df)
    print(product_group_revenue)
