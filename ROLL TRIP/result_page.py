import streamlit as st




# Customize Streamlit theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f5f5;  /* Light grey background */
    }
    .recommend-button {
        background-color: #008CBA; /* Blue background */
        color: white; /* White text */
        padding: 10px 20px; /* Padding inside the button */
        font-size: 18px; /* Button text size */
        border-radius: 5px; /* Rounded corners */
        border: none; /* No border */
        cursor: pointer; /* Pointer cursor */
    }
    .recommend-button:hover {
        background-color: #005F6B; /* Darker blue on hover */
    }
    .share-header {
        text-align: center;
        font-family: 'Pacifico', cursive;
        font-size: 28px;
        font-weight: bold;
        margin-top: 20px;
        padding: 10px;
        background-color: #F5F5DC;
        border-radius: 10px;
        display: inline-block;
    }
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def get_images():
    
    return ["image1.jpg", "image2.jpg", "image3.jpg"]



def result_page():                                      #main 부분을 여기로 
    st.title("Right Now ~ ! 여행지 추천")
    

    if 'selected_destination' in st.session_state:
        st.write(f"선택된 여행지는~: {st.session_state.selected_destination}")

    if 'random_spots' in st.session_state:
        st.write("랜덤으로 선택된 관광지는:")
        for i, spot in enumerate(st.session_state.selected_famous_spots):
            st.write(f"{i+1}. {spot}")
    
    
    # 열을 생성
    cols = st.columns(3)

    # 각 열에 이미지를 배치
    for i, img_path in enumerate(get_images()):
        cols[i].image(img_path, caption=f"관광지 {i+1}", use_column_width=True)
    
    st.markdown("""
    <div class="share-header" style="font-family: 'Arial', sans-serif;">
            여행 정보 공유하기
    </div>
    """, unsafe_allow_html=True)

    current_url = "http://localhost:8501/"
    st.markdown(f"""
    <div class="social-icons">
        <a href="https://www.facebook.com/sharer/sharer.php?u={current_url}" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@3/icons/facebook.svg" width="50" height="50" alt="Facebook">
        </a>
        <a href="https://twitter.com/intent/tweet?text=Check+out+this+app!+{current_url}" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@3/icons/twitter.svg" width="50" height="50" alt="Twitter">
        </a>
        <a href="https://www.instagram.com/" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@3/icons/instagram.svg" width="50" height="50" alt="Instagram">
        </a>
        <a href="{current_url}" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@3/icons/link.svg" width="50" height="50" alt="URL">
        </a>
    </div>
    """, unsafe_allow_html=True)

def main():
    result_page()


if __name__ == "__main__":
    main()


    