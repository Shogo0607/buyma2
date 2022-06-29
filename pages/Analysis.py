import streamlit as st
from datetime import datetime as dt
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
from st_aggrid.shared import GridUpdateMode
from st_aggrid import JsCode
import plotly_express as px
st.set_page_config(layout="wide")

st.title("BUYMA Search tool")
file = st.sidebar.file_uploader("出力したfileをアップロードしてください",type=("csv"))

if not file:
    st.warning("CSVファイルをアップロードしてください。")
    st.stop()

all_data = pd.read_csv(file)
st.subheader("全データ表示")

gb = GridOptionsBuilder.from_dataframe(all_data)

# ---
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True,enable_enterprise_modules=True)
cell_renderer=JsCode('''function(params) {return '<a href="' + params.value + '" target="_blank">'+ params.value+'</a>'}''')
gb.configure_column("問い合わせURL", cellRenderer=cell_renderer)
gb.configure_column("アイテムURL", cellRenderer=cell_renderer)
gridOptions = gb.build()
gridOptions["columnDefs"][0]["checkboxSelection"]=True
gridOptions["columnDefs"][0]["headerCheckboxSelection"]=True


data = AgGrid(all_data, 
              gridOptions=gridOptions, 
              enable_enterprise_modules=True, 
              allow_unsafe_jscode=True, 
              update_mode=GridUpdateMode.SELECTION_CHANGED)
col1,col2,col3 = st.columns(3)

selected_rows = data["selected_rows"]
selected_rows = pd.DataFrame(selected_rows)

with col1:
    st.subheader("問い合わせユーザーTop10")
    st.table(all_data['問い合わせユーザ名'].value_counts(sort=True).head(10))

with col2:
    st.subheader("問い合わせ商品Top10")
    st.table(all_data['アイテム名'].value_counts(sort=True).head(10))

with col3:
    st.subheader("回答者Top10")
    st.table(all_data['回答者'].value_counts(sort=True).head(10))

st.subheader("回答者別回答数")
if len(selected_rows) != 0:
    fig = px.bar(selected_rows, "回答者", color="アイテム名")
    fig.update_layout(height=400,width=1300)
    st.plotly_chart(fig)
else:
    st.warning("表中のチェックボックスを選択してください。")