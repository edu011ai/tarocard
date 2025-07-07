import streamlit as st
import openai
import base64
import requests

# OpenAI API 키 입력
import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI API KEY ---
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("오늘의 운세 타로카드 🔮")

# 프로필 사진만 상단에 배치
st.image("타로사진.png", width=400)

# 소개글을 사진 아래에 배치
st.markdown(
    """
    오늘, 타로가 당신에게 건네는 작은 힌트!\n
    마음속에 궁금한 일이 있다면 살짝 떠올려보세요.\n
    그 마음을 담아 버튼을 눌러주세요.\n
    타로가 오늘의 답을 건넵니다.
    """
)

if st.button("오늘 운세 뽑기 🃏"):
    prompt = "A fortune tarot card illustration for today's luck, beautiful, mystical, high detail"
    with st.spinner("타로카드를 뽑는 중입니다...⌛"):
        try:
            # 이미지 생성
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url

            # 두 컬럼으로 배치 (왼쪽: 이미지, 오른쪽: 해석)
            col1, col2 = st.columns([1, 1.2])
            with col1:
                st.image(
                    image_url,
                    caption="오늘의 운세 타로카드",
                    width=220 # 실제 카드 느낌의 적당한 크기(px)
                )
            with col2:
                # 카드 해석 문구 생성
                interpretation_prompt = (
                    "오늘의 운세 타로카드가 나타내는 의미를 간단하고 긍정적으로 2~3문장으로 한국어로 설명해줘. 물론입니다와 같은 대답은 할 필요없어."
                )
                interpretation_response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "당신은 친절한 타로카드 해설가입니다."},
                        {"role": "user", "content": interpretation_prompt}
                    ],
                    max_tokens=100,
                    temperature=0.7
                )
                interpretation = interpretation_response.choices[0].message.content.strip()
                st.markdown(f"{interpretation}")
        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")