import openai
import streamlit as st
import requests
from geopy.distance import geodesic
import random
import pandas as pd
import json  # json 모듈 추가
import os

# Ensure you have the API key set as an environment variable for security
openai.api_key = "open_api키입력"

def get_travel_recommendations(region):
    query = f"추천 여행지를 알려줘. 지역: {region}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error fetching travel recommendations: {e}")
        return ""

def get_famous_spots(region):
    prompt = f""""추천 여행지를 알려줘. 지역: {region} , 3개의 관광지 정보를 제공해줘:

    관광지 이름 
    관광지 설명
    날씨정보
    음식점 1개

    반드시 다음과 같은 유효한 JSON 형식으로 응답해주세요:
    [
      {{
        "location" : "관광지 이름",
        "description" : "관광지 설명",
        "weather": "날씨정보",
        "food" : "맛집"
      }},
      ...
    ]
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        spots = response.choices[0].message['content']
        spots_json = json.loads(spots)  # json 모듈을 사용하여 응답 파싱
        return spots_json
    except Exception as e:
        st.error(f"Error fetching famous spots: {e}")
        return []

# Load location data
location_data = pd.read_excel(r'C:\Users\이영락\Documents\GitHub\streamlit\korea_administrative_division_latitude_longitude.xlsx')

def find_nearest_locations(user_location, num_recommendations=6):
    distances = []
    for _, row in location_data.iterrows():
        distance_to_location = geodesic(user_location, (row['latitude'], row['longitude'])).km
        distances.append((row['city'], distance_to_location))

    distances.sort(key=lambda x: x[1])
    recommendations = distances[:num_recommendations]
    return recommendations

def get_user_location():
    ipinfo_token = "7e42d3944b33d1"
    response = requests.get(f"https://ipinfo.io?token={ipinfo_token}")
    data = response.json()
    loc = data['loc'].split(',')
    return float(loc[0]), float(loc[1])

def select_random_destination(destinations):
    return random.choice(destinations)

def recommend_by_location():
    try:
        user_location = get_user_location()
        if user_location == (None, None):
            return
        st.session_state.recommendations = find_nearest_locations(user_location)
        st.session_state.loc_flag = True
        response = "당일치기 추천 여행지 (순서: 도시, 거리(km)):<br><ul>"
        response += "".join([f"<li>{idx}. {location} - {dist:.2f} km</li>" for idx, (location, dist) in enumerate(st.session_state.recommendations, start=1)])
        response += "</ul>"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.step = 2
        
    except Exception as e:
        response = f"위치를 확인할 수 없습니다. 위치 정보를 수동으로 입력하세요. 오류: {e}"
        st.session_state.messages.append({"role": "assistant", "content": response})

def main_page():
    # Initialize session states
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'loc_flag' not in st.session_state:
        st.session_state.loc_flag = False
    if 'selected_destinations' not in st.session_state:
        st.session_state.selected_destinations = []
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'selected_famous_spots' not in st.session_state:
        st.session_state.selected_famous_spots = []
    if 'random_spots' not in st.session_state:
        st.session_state.random_spots = []
    if 'recommendations_generated' not in st.session_state:
        st.session_state.recommendations_generated = False

    # Custom CSS
    st.markdown(
        """
        <style>
        .assistant {
            background-color: #f1f1f1;
            border-radius: 10px;
            padding: 10px;
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            color: #333;
        }
        .user {
            background-color: #d1e7dd;
            border-radius: 10px;
            padding: 10px;
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            color: #333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 5px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(f"<div class='assistant'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            with st.chat_message("user"):
                st.markdown(f"<div class='user'>{message['content']}</div>", unsafe_allow_html=True)

    if st.session_state.step == 0:
        with st.chat_message("assistant"):
            st.markdown("<div class='assistant'>안녕하세요! 저는 여행지를 추천해주는 챗봇입니다.</div>", unsafe_allow_html=True)
        with st.chat_message("assistant"):
            st.markdown("<div class='assistant'>내 위치를 기반으로 여행지를 추천해드리겠습니다.</div>", unsafe_allow_html=True)
        if st.button("추천 받기"):
            recommend_by_location()

    if st.session_state.step == 2:
        if 'selected_destination' not in st.session_state:
            st.session_state.selected_destination = select_random_destination([loc for loc, _ in st.session_state.recommendations])
            st.session_state.selected_destinations.append(st.session_state.selected_destination)
            st.session_state.selected_famous_spots = get_famous_spots(st.session_state.selected_destination)

            with st.chat_message("assistant"):
                st.markdown(f"<div class='assistant'>랜덤으로 선택된 여행지는 {st.session_state.selected_destination}입니다.</div>", unsafe_allow_html=True)
            
            spots_text = "<ul>" + "".join([f"<li>{i+1}. {spot['location']} - {spot['description']} (날씨: {spot['weather']})</li>" for i, spot in enumerate(st.session_state.selected_famous_spots)]) + "</ul>"
            with st.chat_message("assistant"):
                st.markdown(f"<div class='assistant'>랜덤으로 선택된 관광지는\n{spots_text}</div>", unsafe_allow_html=True)

            if st.button("결과 공유하기"):
                st.session_state.page = 'Result Page'

def main():
    main_page()

if __name__ == "__main__":
    main()
