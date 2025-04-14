# -*- encoding: utf-8 -*-
'''
@File    :   web_chat.py
@Time    :   2025/04/11
@Author  :   Yansong Du 
@Contact :   dys24@mails.tsinghua.edu.cn
'''

import streamlit as st
import requests

st.set_page_config(page_title="无线光通信专家问答系统", layout="centered")

st.title("🔬 无线光通信专家问答系统")
st.markdown("👋 输入你关心的无线光通信问题，我会为你专业解答。")

# 设置 FastAPI 后端地址
API_URL = "http://localhost:8000/chat"

# 用户输入框
question = st.text_input("请输入您的问题：", placeholder="例如：什么是无线光通信？")

# 发送按钮
if st.button("发送"):
    if not question.strip():
        st.warning("⚠️ 问题不能为空，请重新输入。")
    else:
        with st.spinner("⏳ 正在生成回答，请稍候..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question}
                )
                if response.status_code == 200:
                    answer = response.json().get("response", "❌ 无法解析模型回答")
                    st.success("✅ 回答如下：")
                    st.write(answer)
                else:
                    st.error(f"❌ 请求失败：{response.status_code}")
            except Exception as e:
                st.error(f"❌ 连接失败，请确保后端正在运行。错误信息：{str(e)}")
