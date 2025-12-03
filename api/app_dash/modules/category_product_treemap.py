import plotly.express as px

def category_product_treemap_graph(df, selected_category):
    if selected_category == "categoryName":
        treemap_option = "대분류"
        path = ["categoryName"]
        treemap_df = df.groupby(path, as_index=False)['salesAmount'].sum()

    elif selected_category == "productCategoryName":
        treemap_option = "제품분류"
        path = ["categoryName", "productCategoryName"]
        treemap_df = df.groupby(path, as_index=False)['salesAmount'].sum()
    else:
        treemap_option = "제품"
        path = ["categoryName", "productCategoryName", "productName"]
        treemap_df = df.groupby(path, as_index=False)['salesAmount'].sum()

    fig_treemap = px.treemap(
        treemap_df,
        path = path,
        values = "salesAmount",
        color = "salesAmount",
    )

    return treemap_option, fig_treemap