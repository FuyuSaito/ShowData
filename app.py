import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# データの表示（ピボットテーブル）
def show_data(selected_sheet, selected_regions, data):
    filtered_data = data[(data['地域'].isin(selected_regions)) & (data['地域'] != '全国')]
    filtered_data = filtered_data.drop(columns=['注記', '地域コード'])
    pivot_table = filtered_data.pivot(index='時点', columns='地域').droplevel(level=0, axis=1)
    pivot_table.columns.name = None
    pivot_table.index = pivot_table.index.astype('str')
    st.write(pivot_table)

# グラフの表示
def show_graph(selected_sheet, selected_regions, data):
    fig, ax = plt.subplots(figsize=(10, 5))
    for region in selected_regions:
        region_data = data[(data['地域'] == region) & (data['地域'] != '全国')]
        ax.plot(region_data['時点'], region_data[selected_sheet], label=region)
    ax.set_xlabel('年月')
    ax.set_ylabel('人口')
    ax.set_title(f'{selected_sheet}の人口推移')
    ax.tick_params(axis='x', rotation=90)
    ax.legend(loc='upper left')
    st.pyplot(fig)

# メインのStreamlitアプリ
# メインのStreamlitアプリ
def main():
    st.title('エクセルファイルのデータ表示')
    st.sidebar.header('選択欄')

    uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=["xlsx", "xls"])
    if uploaded_file is not None:
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)  # すべてのシートを読み込む
        sheet_names = list(excel_data.keys())

        for i in sheet_names:
            excel_data[i].時点 = excel_data[i].時点.str.extract(r'(\d+)').astype('int')

        selected_sheet = st.sidebar.selectbox('シート', sheet_names)

        if selected_sheet:
            selected_regions = st.sidebar.multiselect('地域', excel_data[selected_sheet]['地域'].unique())
            
            # 年のスライダーで開始年と終了年を選択
            start_year, end_year = st.sidebar.slider("年の範囲を選択", 
                                         min_value=int(excel_data[selected_sheet]['時点'].min()), 
                                         max_value=int(excel_data[selected_sheet]['時点'].max()), 
                                         value=(int(excel_data[selected_sheet]['時点'].min()), int(excel_data[selected_sheet]['時点'].max())))


            if selected_regions:
                filtered_data = excel_data[selected_sheet][(excel_data[selected_sheet]['地域'].isin(selected_regions))]
                filtered_data = filtered_data[(filtered_data['時点'] >= start_year) & (filtered_data['時点'] <= end_year)]

                if not filtered_data.empty:
                    show_graph(selected_sheet, selected_regions, filtered_data)
                    show_data(selected_sheet, selected_regions, filtered_data)
                else:
                    st.write("選択された期間にデータがありません。")


if __name__ == "__main__":
    st.set_option('deprecation.showPyplotGlobalUse', False)
    main()
