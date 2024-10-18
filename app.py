import streamlit as st
import json
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 스트림릿 앱 설정
st.title('불편한 편의점 숏폼 과제 지원 프로그램')
st.write('학생들이 <불편한 편의점>을 읽고 자신만의 생각을 담은 숏폼 컨텐츠를 만들 수 있도록 돕기 위한 프로그램입니다.')

# 번역 함수
def translate_to_english(text):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate the given Korean text to English."},
                {"role": "user", "content": f"Translate the following Korean text to English: {text}"}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"번역 중 오류 발생: {str(e)}")
        return None

# GPT-4 모델을 통해 프롬프트 생성 지원
def generate_prompt_details(base_prompt, language):
    prompt_details = (
        f"다음 지시사항에 따라 프롬프트를 상세화해주세요:\n"
        f"1. 시간 및 공간에 대한 설명을 포함합니다.\n"
        f"2. 배경에 대한 설명을 포함합니다.\n"
        f"3. 피사체에 대한 자세한 설명을 포함합니다.\n"
        f"4. 만약 피사체가 인물이라면, 연령, 얼굴 생김새, 헤어스타일, 복장, 표정 등을 세밀하게 묘사합니다.\n"
        f"5. 언어는 이미지에 포함되지 않으므로 언어 표현은 제외합니다.\n"
        f"기본 프롬프트: {base_prompt}\n"
        f"응답은 {language}로 작성해주세요."
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "학생들이 이미지를 구체적으로 묘사할 수 있도록 도움을 주는 역할입니다."},
                {"role": "user", "content": prompt_details}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"프롬프트 생성 중 오류 발생: {str(e)}")
        return None

# 예시 프롬프트 제공 (사용자 입력 전에만 표시)
st.write("예시 프롬프트: '햇살이 가득한 여름 오후, 공원에서 책을 읽는 20대 여성. 그녀는 짧은 갈색 머리를 하고 있으며, 노란색 드레스를 입고 편안한 미소를 짓고 있다.'")

# 사용자로부터 입력받기
st.write("프롬프트를 작성할 때 다음 요소를 포함하세요: 시간, 공간, 배경, 피사체(인물인 경우 세부 묘사)")
student_prompt = st.text_input('숏폼 컨텐츠에 사용할 이미지를 설명하는 기본 아이디어를 입력하세요:', '')

if student_prompt:
    if len(student_prompt) < 20:
        st.warning("아이디어가 너무 짧습니다. 더 구체적으로 작성해 주세요.")
    else:
        st.write('프롬프트 상세 설명:')

        # 한국어 프롬프트 생성
        korean_prompt = generate_prompt_details(student_prompt, "한국어")
        if korean_prompt:
            st.subheader("한국어 프롬프트")
            st.write(korean_prompt)

            # 한국어 프롬프트 복사 버튼
            korean_prompt_json = json.dumps(korean_prompt)
            copy_korean_button = f"""
            <button onclick="navigator.clipboard.writeText({korean_prompt_json}); alert('한국어 프롬프트가 복사되었습니다.');">한국어 프롬프트 복사하기</button>
            """
            st.markdown(copy_korean_button, unsafe_allow_html=True)

            # 영어 번역
            english_prompt = translate_to_english(korean_prompt)
            if english_prompt:
                st.subheader("English Prompt")
                st.write(english_prompt)

                # 영어 프롬프트 복사 버튼
                english_prompt_json = json.dumps(english_prompt)
                copy_english_button = f"""
                <button onclick="navigator.clipboard.writeText({english_prompt_json}); alert('English prompt copied to clipboard.');">Copy English Prompt</button>
                """
                st.markdown(copy_english_button, unsafe_allow_html=True)
