
# US Macro Dashboard 使用指南

## 文件说明
- fetch_fred_data.py：抓取美国宏观数据（需设置 API KEY）
- process_data.py：处理抓取到的数据为仪表盘格式
- streamlit_app.py：仪表盘界面展示，可通过 streamlit 启动
- data/：存放原始与处理后的 csv 数据（运行脚本后自动生成）

## 使用步骤（本地运行）
1. 安装依赖：
   pip install pandas plotly streamlit fredapi

2. 运行抓数脚本：
   python fetch_fred_data.py

3. 处理数据：
   python process_data.py

4. 启动仪表盘：
   streamlit run streamlit_app.py

## 注意事项
- 默认展示近五年数据，指标来自 FRED
- 可根据需要扩展指标（修改 MODULES / INDICATORS 字典）
- 支持 Notion 嵌入（通过部署生成公共访问链接）

作者：ChatGPT 宏观仪表盘模块
