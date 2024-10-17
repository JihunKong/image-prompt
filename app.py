from openai import OpenAI
import streamlit as st

# OpenAI 클라이언트 초기화
try:
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
except KeyError:
    st.error("OpenAI API 키를 찾을 수 없습니다. .streamlit/secrets.toml 파일에 [openai] api_key = 'your-key-here' 형식으로 API 키를 설정해주세요.")
    st.stop()

# 스트림릿 앱 설정
st.title('불편한 편의점 숏폼 과제 지원 프로그램')
st.write('학생들이 <불편한 편의점>을 읽고 자신만의 생각을 담은 숏폼 컨텐츠를 만들 수 있도록 돕기 위한 프로그램입니다.')

# GPT-4 모델을 통해 프롬프트 생성 지원
def generate_prompt_details(base_prompt):
    prompt_details = (
        f"시간 및 공간에 대한 설명을 포함합니다.\n"
        f"배경에 대한 설명을 포함합니다.\n"
        f"피사체에 대한 자세한 설명을 포함합니다.\n"
        f"만약 피사체가 인물이라면, 연령, 얼굴 생김새, 헤어스타일, 복장, 표정 등을 세밀하게 묘사합니다.\n"
        f"언어는 이미지에 포함되지 않으므로 언어 표현은 제외합니다.\n"
        f"기본 프롬프트: {base_prompt}"
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "학생들이 이미지를 구체적으로 묘사할 수 있도록 도움을 주는 역할입니다."},
                {"role": "user", "content": prompt_details}
            ],
            max_tokens=200
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"OpenAI API 오류: {str(e)}")
        return None

# 사용자로부터 입력받기
st.write("프롬프트를 작성할 때 다음 요소를 포함하세요: 시간, 공간, 배경, 피사체(인물인 경우 세부 묘사)")
student_prompt = st.text_input('숏폼 컨텐츠에 사용할 이미지를 설명하는 기본 아이디어를 입력하세요:', '')

if student_prompt:
    if len(student_prompt) < 20:
        st.warning("아이디어가 너무 짧습니다. 더 구체적으로 작성해 주세요.")
    else:
        st.write('프롬프트 상세 설명:')
        detailed_prompt = generate_prompt_details(student_prompt)
        if detailed_prompt:
            st.write(detailed_prompt)

# 예시 프롬프트 제공
st.write("예시 프롬프트: '햇살이 가득한 여름 오후, 공원에서 책을 읽는 20대 여성. 그녀는 짧은 갈색 머리를 하고 있으며, 노란색 드레스를 입고 편안한 미소를 짓고 있다.'")
