import streamlit as st
import pandas as pd

st.set_page_config(page_title="더벨 리그테이블 챗봇", layout="wide")

st.markdown("## 📊 더벨 리그테이블 챗봇")

# 상품군 선택
product = st.selectbox("상품군 선택", ["국내채권", "ABS", "FB", "ECM"])

# 연도 선택 (다중 선택 가능)
selected_years = st.multiselect("연도 선택", [f"{year}년" for year in range(2020, 2025)], default=["2024년"])

# 증권사 입력 (쉼표로 구분 가능)
company_input = st.text_input("증권사 이름 입력 (예: KB증권,한화투자증권)")
company_names = [name.strip() for name in company_input.split(',')] if company_input else []

# 파일명 및 시트명 매핑
file_mapping = {
    "국내채권": "더벨 DCM 리그테이블 국내채권 대표주관 순위.xlsx",
    "ABS": "더벨 DCM 리그테이블 유동화증권(ABS) 대표주관 순위.xlsx",
    "FB": "더벨 DCM 리그테이블 여신전문금융회사채권(FB) 대표주관 순위.xlsx",
    "ECM": "더벨 ECM 리그테이블 대표주관 순위.xlsx"
}

sheet_mapping = {
    "국내채권": "전체 국내채권 대표주관 순위",
    "ABS": "유동화증권(ABS) 대표주관 순위",
    "FB": "FB 대표주관순위",
    "ECM": "ECM 대표주관 순위"
}

if st.button("조회하기"):
    file_path = file_mapping[product]
    sheet_name = sheet_mapping[product]

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # 데이터 전처리
        df['연도'] = df['연도'].astype(str).str.replace('년', '').astype(int)
        df['주관사'] = df['주관사'].astype(str).str.strip()

        for year in selected_years:
            year_int = int(year.replace("년", ""))
            df_year = df[df['연도'] == year_int]

            if not df_year.empty:
                if company_names:
                    found = False
                    for name in company_names:
                        df_company = df_year[df_year['주관사'] == name]
                        if not df_company.empty:
                            found = True
                            st.success(f"{year} ({product}) - {name} 검색 결과")
                            st.dataframe(
                                df_company.style.set_properties(
                                    subset=['연도', df.columns[1]],
                                    **{'text-align': 'center'}
                                ),
                                use_container_width=True
                            )
                    if not found:
                        st.warning(f"{year} ({product}) 결과값을 찾을 수 없습니다.")
                else:
                    st.success(f"{year} ({product}) 전체 결과")
                    st.dataframe(
                        df_year.style.set_properties(
                            subset=['연도', df.columns[1]],
                            **{'text-align': 'center'}
                        ),
                        use_container_width=True
                    )
            else:
                st.warning(f"{year}년 ({product}) 시트에 데이터가 없습니다.")

    except Exception as e:
        st.error(f"파일 또는 시트를 불러오는 중 오류 발생: {e}")
