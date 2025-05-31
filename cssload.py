import streamlit as st
import streamlit.components.v1 as components

# streamlit run cssload.py

if "css" not in st.session_state:
    with open("style.css", "r", encoding="utf-8") as css_file:
        st.session_state.css = css_file.read()


def hex_to_rgb(hex: str):
    hex = hex.lstrip("#")
    return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def calculate_middle_color(hex_colors: list[str]):
    # 轉換 HEX 為 RGB 顏色
    rgb_colors = [hex_to_rgb(color) for color in hex_colors]

    # 計算每個顏色通道的平均值
    avg_r = sum(color[0] for color in rgb_colors) // len(rgb_colors)
    avg_g = sum(color[1] for color in rgb_colors) // len(rgb_colors)
    avg_b = sum(color[2] for color in rgb_colors) // len(rgb_colors)

    # 轉換回 HEX
    return rgb_to_hex(avg_r, avg_g, avg_b)


def UpdateCss(css: str, colors: list[str], time: int):
    middle_color = calculate_middle_color(colors)
    css = css.replace("MEANCOLOR", middle_color)

    for i, change_txt in enumerate(
        ["1st_COLOR_", "2nd_COLOR_", "3rd_COLOR_", "4th_COLOR_", "5th_COLOR_"]
    ):
        css = css.replace(change_txt + "ff", colors[i] + "ff")
        css = css.replace(change_txt + "00", colors[i] + "00")

    css = css.replace("ANIMETIME", str(time) + "s")

    return f"<style>{css}</style>"


st.title("CSS load")

css = st.session_state.css

colors = ["#eb694e", "#f30ba4", "#feea83", "#aa8ef5", "#f8c093"]
colors = [st.color_picker(f"選擇顏色 {i + 1}", v) for i, v in enumerate(colors)]

loop_time = st.number_input("循環週期 : ", value=20)

components.html(f"<style>{UpdateCss(css, colors, loop_time)}</style>", height=400)
