import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 페이지 설정
st.set_page_config(page_title="불편한 편의점 숏폼 과제 지원", layout="wide")

# 사이드바에 앱 설명 추가
with st.sidebar:
    st.title("앱 사용 가이드")
    st.write("1. 기본 아이디어를 입력하세요.")
    st.write("2. '프롬프트 생성' 버튼을 클릭하세요.")
    st.write("3. 생성된 한국어와 영어 프롬프트를 확인하세요.")
    st.write("4. '클립보드에 복사' 버튼을 눌러 프롬프트를 복사하세요.")

# 메인 페이지 콘텐츠
st.title('📚 불편한 편의점 숏폼 과제 지원 프로그램')
st.write('학생들이 <불편한 편의점>을 읽고 자신만의 생각을 담은 숏폼 컨텐츠를 만들 수 있도록 돕기 위한 프로그램입니다.')

# 번역 함수
def translate_to_english(text):
    try:
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
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
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "학생들이 이미지를 구체적으로 묘사할 수 있도록 도움을 주는 역할입니다."},
                {"role": "user", "content": prompt_details}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"프롬프트 생성 중 오류 발생: {str(e)}")
        return None

# 클립보드에 복사하는 함수
def copy_to_clipboard(text, button_key):
    if st.button('클립보드에 복사', key=button_key):
        js = f"navigator.clipboard.writeText('{text.replace("'", "\\'")}');"
        streamlit_js_eval(js)
        st.success('클립보드에 복사되었습니다!')

# 예시 프롬프트 제공
st.info("💡 예시 프롬프트: '햇살이 가득한 여름 오후, 공원에서 책을 읽는 20대 여성. 그녀는 짧은 갈색 머리를 하고 있으며, 노란색 드레스를 입고 편안한 미소를 짓고 있다.'")

# 사용자로부터 입력받기
st.subheader("🖋 프롬프트 작성")
st.write("프롬프트를 작성할 때 다음 요소를 포함하세요: 시간, 공간, 배경, 피사체(인물인 경우 세부 묘사)")
student_prompt = st.text_area('숏폼 컨텐츠에 사용할 이미지를 설명하는 기본 아이디어를 입력하세요:', height=100)

if st.button('프롬프트 생성', key='generate'):
    if not student_prompt or len(student_prompt) < 20:
        st.warning("⚠️ 아이디어가 너무 짧습니다. 더 구체적으로 작성해 주세요.")
    else:
        with st.spinner('프롬프트 생성 중...'):
            # 한국어 프롬프트 생성
            korean_prompt = generate_prompt_details(student_prompt, "한국어")
            if korean_prompt:
                st.subheader("🇰🇷 한국어 프롬프트")
                st.text_area("생성된 한국어 프롬프트:", value=korean_prompt, height=200, key='korean_prompt')
                copy_to_clipboard(korean_prompt, 'korean_copy_btn')

                # 영어 번역
                english_prompt = translate_to_english(korean_prompt)
                if english_prompt:
                    st.subheader("🇺🇸 English Prompt")
                    st.text_area("Generated English Prompt:", value=english_prompt, height=200, key='english_prompt')
                    copy_to_clipboard(english_prompt, 'english_copy_btn')

# 푸터 추가
st.markdown("---")
st.markdown("© 2024 불편한 편의점 숏폼 과제 지원 프로그램. All rights reserved.")
