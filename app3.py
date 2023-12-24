import re
from collections import Counter

import jieba
import requests
import streamlit as st
from bs4 import BeautifulSoup
from pyecharts import options as opts
from pyecharts.charts import WordCloud, Bar, Line, TreeMap, Pie, Funnel, Radar
from streamlit.components.v1 import html

st.title('python实训')
url = st.text_input('')

sidebar_options = ["词云", "柱形图", "折线图", "饼图", "矩形树图", "漏斗图", "瀑布图"]
chart_type = st.sidebar.selectbox('选择图表类型', sidebar_options)

if url:
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    # 使用BeautifulSoup解析响应文本
    soup = BeautifulSoup(response.content, 'html.parser')
    # 获取文本内容
    text = soup.text
    # 1. 移除 HTML 标签（如果存在）
    cleaned_text = re.sub(r'<.*?>', '', text)
    # 2. 去除空白字符
    cleaned_text = " ".join(cleaned_text.split())
    # 3. 去除标点和特殊字符
    punctuation = '''！ ；（ ） —— |  ：“”，、。( )-[ ]{ };:'"\,<>./?@#$%^&*_~'''
    cleaned_text = cleaned_text.translate(str.maketrans('', '', punctuation))
    # 4. 转换为小写
    cleaned_text = cleaned_text.lower()
    # 5. 去除数字
    cleaned_text = re.sub(r'\d+', '', cleaned_text)
    # 6. 去除停用词
    stop_words = {"的", "是", "在", "有", "和", "也", "了", "不", "我", "我们", ...}
    # 6. 分词并去除停用词
    words = jieba.cut(cleaned_text)
    cleaned_text = ''.join([word for word in words if word not in stop_words])  # 不使用空格连接

    # 7. 再次去除多余的空格（如果需要）
    cleaned_text = re.sub(r'\s+', '', cleaned_text)

    words = jieba.lcut(cleaned_text)
    word_counts = Counter(words)

    # 不再使用滑块，直接设定最小词频为5
    min_freq = 5
    freq_words = {k: v for k, v in word_counts.items() if v >= min_freq}

    top20_words = dict(Counter(freq_words).most_common(20))
    st.write('词频排名前20的词汇:')
    for word, count in Counter(freq_words).most_common(20):
        st.write(f'{word}: {count}')

    # 根据选定的图表类型绘制图表
    if chart_type == '词云':
        wc = WordCloud()
        wc.add("", list(top20_words.items()), word_size_range=[20, 100])
        wc.set_global_opts(
            title_opts=opts.TitleOpts(title="词云图"),
        )
        wc_html = wc.render_embed()
        st.components.v1.html(wc_html, width=900, height=600)

    elif chart_type == '柱形图':
        bar = Bar()
        bar.add_xaxis(list(top20_words.keys()))
        bar.add_yaxis("", list(top20_words.values()))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="柱状图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30))
        )
        bar_html = bar.render_embed()
        st.components.v1.html(bar_html, width=900, height=600)

    elif chart_type == '折线图':
        line = Line()
        line.add_xaxis(list(top20_words.keys()))
        line.add_yaxis("", list(top20_words.values()))
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="折线图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30))
        )
        line_html = line.render_embed()
        st.components.v1.html(line_html, width=900, height=600)

    elif chart_type == '饼图':
        pie = Pie()
        pie.add(
            series_name="",
            data_pair=list(top20_words.items()),
            radius=["20%", "75%"],
            label_opts=opts.LabelOpts(formatter="{b}: {d}%")
        )
        pie.set_global_opts(
            title_opts=opts.TitleOpts(title="饼图"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="1%")
        )
        pie_html = pie.render_embed()
        st.components.v1.html(pie_html, width=900, height=600)

    elif chart_type == '矩形树图':
        tree = TreeMap()
        tree_data = [{"value": v, "name": k} for k, v in top20_words.items()]
        tree.add(
            series_name="",
            data=tree_data,
            visual_min=5,
            leaf_depth=2,
            label_opts=opts.LabelOpts(position="inside"),
        )
        tree.set_global_opts(title_opts=opts.TitleOpts(title="矩形树图"))
        tree_html = tree.render_embed()
        st.components.v1.html(tree_html, width=900, height=600)

    elif chart_type == '漏斗图':
        funnel = Funnel()
        funnel.add("", list(top20_words.items()))
        funnel.set_global_opts(
            title_opts=opts.TitleOpts(title="漏斗图", pos_top="20%"),
        )
        funnel_html = funnel.render_embed()
        st.components.v1.html(funnel_html, width=900, height=600)

    elif chart_type == '瀑布图':
        bar = Bar(init_opts=opts.InitOpts(renderer='canvas'))
        bar.add_xaxis(list(top20_words.keys()))
        bar.add_yaxis("", list(top20_words.values()))
        # 不显示柱状图颜色标签
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        # 设置图表标题、坐标轴信息
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="瀑布图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),

            # 设置tooltip提示信息
            tooltip_opts=opts.TooltipOpts(is_show=True),

            # 设置视觉映射组件控制颜色渐变
            visualmap_opts=opts.VisualMapOpts(
                is_show=True, pos_left="10%", pos_top="30%",
                min_=min(top20_words.values()), max_=max(top20_words.values())
            )
        )
        bar_html = bar.render_embed()
        st.components.v1.html(bar_html, width=900, height=600)
