import streamlit as st
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize
from collections import Counter
from wordcloud import WordCloud
from pyecharts import options as opts
from pyecharts.charts import WordCloud as PyechartsWordCloud, Bar, Line, Pie, TreeMap, Funnel, Radar

# 获取静态网页的文本内容
def get_webpage_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    return text

# 统计重复关键词并显示词语和次数
def count_and_display_keywords(text):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha() and len(word) > 1]
    word_freq = Counter(tokens)

    st.subheader("关键词统计:")

    # 只显示重复出现次数最多的前20个词语
    sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20])

    for word, freq in sorted_word_freq.items():
        st.write(f"{word}: {freq} 次")

    return sorted_word_freq

# 使用 pyecharts 绘制词云
def plot_word_cloud(word_freq):
    words = list(word_freq.keys())
    values = list(word_freq.values())

    c = (
        PyechartsWordCloud()
        .add("", list(zip(words, values)), word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="词云"))
        .render("wordcloud.html")
    )

    st.components.v1.html(open("wordcloud.html", "r", encoding="utf-8").read(), height=1000)

# 使用 pyecharts 绘制柱形图
def plot_bar_chart(word_freq):
    words = list(word_freq.keys())
    values = list(word_freq.values())

    c = (
        Bar()
        .add_xaxis(words)
        .add_yaxis("词频", values)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="词频柱形图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45, font_size=12)),
        )
        .render("bar_chart.html")
    )

    st.components.v1.html(open("bar_chart.html", "r", encoding="utf-8").read(), height=1000)

# 使用 pyecharts 绘制折线图
def plot_line_chart(word_freq):
    words = list(word_freq.keys())
    values = list(word_freq.values())

    c = (
        Line()
        .add_xaxis(words)
        .add_yaxis("词频", values, markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="词频折线图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45, font_size=12)),
        )
        .render("line_chart.html")
    )

    st.components.v1.html(open("line_chart.html", "r", encoding="utf-8").read(), height=1000)
# 使用 pyecharts 绘制饼图
def plot_pie_chart(word_freq):
    words = list(word_freq.keys())
    values = list(word_freq.values())

    c = (
        Pie()
        .add("", list(zip(words, values)))
        .set_global_opts(title_opts=opts.TitleOpts(title="词频饼图"), legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("pie_chart.html")
    )

    st.components.v1.html(open("pie_chart.html", "r", encoding="utf-8").read(), height=1000)
# 使用 pyecharts 绘制矩形树图
def plot_tree_map(word_freq):
    words = list(word_freq.keys())
    values = list(word_freq.values())

    data = []
    for word, freq in zip(words, values):
        data.append({"value": freq, "name": word})

    c = (
        TreeMap()
        .add("矩形树图", data)
        .set_global_opts(title_opts=opts.TitleOpts(title="矩形树图"))
        .render("tree_map.html")
    )

    st.components.v1.html(open("tree_map.html", "r", encoding="utf-8").read(), height=1000)

# 使用 pyecharts 绘制漏斗图
def plot_funnel_chart(word_freq):
    words = list(word_freq.keys())
    values = list(word_freq.values())

    data = []
    for i in range(len(words)):
        data.append((words[i], values[i]))

    c = (
        Funnel()
        .add("漏斗图", data, label_opts=opts.LabelOpts(position="inside"))
        .set_global_opts(title_opts=opts.TitleOpts(title="漏斗图"))
        .render("funnel_chart.html")
    )

    st.components.v1.html(open("funnel_chart.html", "r", encoding="utf-8").read(), height=1000)
# 使用 pyecharts 绘制雷达图
def plot_radar_chart(word_freq):
    words = list(word_freq.keys())
    values = list(word_freq.values())

    c = (
        Radar()
        .add_schema(schema=[opts.RadarIndicatorItem(name=word, max_=max(values)) for word in words])
        .add("词频", [values], areastyle_opts=opts.AreaStyleOpts(opacity=0.1))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="词频雷达图"))
        .render("radar_chart.html")
    )

    st.components.v1.html(open("radar_chart.html", "r", encoding="utf-8").read(), height=500)

# Streamlit应用程序
def main():
    st.title('python实训')

    # 用户输入网址
    url = st.text_input('输入网址:')

    # 选择图形类型
    chart_type = st.sidebar.selectbox("选择图形类型", ["词云", "柱形图", "折线图", "饼图","矩形树图","漏斗图","雷达图"])

    # 当用户选择图形类型时，获取正文、进行关键词统计并显示对应图形
    if st.button('生成图形'):
        try:
            webpage_text = get_webpage_text(url)
            st.text_area("网页正文", webpage_text)

            word_freq = count_and_display_keywords(webpage_text)

            if chart_type == "词云":
                plot_word_cloud(word_freq)
            elif chart_type == "柱形图":
                plot_bar_chart(word_freq)
            elif chart_type == "折线图":
                plot_line_chart(word_freq)
            elif chart_type == "饼图":
                plot_pie_chart(word_freq)
            elif chart_type == "矩形树图":
                plot_tree_map(word_freq)
            elif chart_type == "漏斗图":
                plot_funnel_chart(word_freq)
            elif chart_type == "雷达图":
                plot_radar_chart(word_freq)
        except:
            st.write("错误: 无法检索网页内容。请查看网址.")

if __name__ == '__main__':
    main()
