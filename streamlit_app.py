import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SUPER-SON 사이드프로젝트",
    page_icon="😃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Google Analytics tracking code
GA_TRACKING_CODE = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-24TZHQ6Y49"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-24TZHQ6Y49');
</script>
"""

# Google Search Console verification meta tag
GSC_VERIFICATION_META_TAG = """
<meta name="google-site-verification" content="hA5Z8T9H4JpXgiH69j3LkKS5wtCLdUtT72R7oZekObc">
"""

# Insert GA tracking code in the app
components.html(GA_TRACKING_CODE + GSC_VERIFICATION_META_TAG, height=0, width=0)

with st.sidebar:
    st.write(
        """
    ### 연락처
    📞 Tel. 010-4430-2279  
    📩 E-mail. [gnsu0705@gmail.com](gnsu0705@gmail.com)  
    💻 Blog. [Super-Son](https://super-son.tistory.com)
    😎 Resume. [Super-Son](https://super-son.streamlit.app)
    """
    )

st.write(
    """
## 사이드프로젝트 by SUPER-SON
안녕하세요. 👋  
저의 사이드프로젝트에 관심가져주셔서 감사합니다.  
사이드 프로젝트는 대부분 제가 생활하면서 불편하다고 느낀 것들을 통해 얻은 아이디어로 진행하였습니다.  

하단에 각 프로젝트를 정리하였으며, 좌측 사이드바를 활용해 각 사이드 프로젝트를 사용해보실 수 있습니다.  
오늘도 방문해주셔서 감사합니다. 😃
"""
)

st.divider()

### streamlit-elements를 활용한 dashboard로 제작
### link : https://github.com/okld/streamlit-elements