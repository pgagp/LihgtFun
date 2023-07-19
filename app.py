import streamlit as st
import pickle

import pandas as pd
import numpy as np
from lightfm import LightFM

from PIL import Image
import time


image = Image.open('words.png')
st.image(image)


df = pd.read_csv('df.csv', index_col=0)

model_file = 'model_warp.pkl'
with open(model_file, 'rb') as f:
    model_warp = pickle.load(f)

model_file1 = 'model_bpr.pkl'
with open(model_file1, 'rb') as f:
    model_bpr = pickle.load(f)


def recommend_similar_item(model, item_id, num_items=10):
    item_embeddings = model.item_embeddings
    item_embedding = item_embeddings[item_id]
    similarities = np.dot(item_embeddings, item_embedding)
    similar_indices = np.argsort(-similarities)
    similar_indices = similar_indices[similar_indices != item_id]
    top_similar_indices = similar_indices[:num_items]

    return top_similar_indices

def recommend_items(model, user_id):
    num_users, num_features = model.user_embeddings.shape
    num_items, _ = model.item_embeddings.shape
    user_ids = np.array([user_id] * num_items)
    item_ids = np.array(range(num_items))
    ratings = np.ones(num_items)
    scores = model.predict(user_ids, item_ids, num_threads=2)
    recommendations = item_ids[np.argsort(-scores)]

    return recommendations[:10].tolist()


def item_to_rec(model, game_choose):
    ids = df[df['title']==game_choose].item_id.unique().item()
    recs = recommend_similar_item(model, ids)
    filtered_df = df[df['item_id'].isin(recs)]

    return filtered_df

st.markdown("<h1 style='text-align: center; '>LightFun ваш помощник для </h1>", unsafe_allow_html=True)

colT1,colT2 = st.columns([1,9])
with colT2:
    st.title('выбора настольных игр :game_die:')

st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.caption('*LightFun создан на данных с [tesera.ru](https://tesera.ru/) и библиотеки [LightFM](https://making.lyst.com/lightfm/docs/index.html)')
st.markdown(' ')
st.write('Пожалуйста, пройдите небольшой опрос, чтобы LightFun предоставил наилучшие рекомендации для вас :heart_decoration:')
st.markdown(' ')

a = 'выберите ответ' 
first = st.radio(
    'КАКОЙ У ВАС ОПЫТ В НАСТОЛЬНЫХ ИГРАХ?',
    ('выберите ответ', 'небольшой, знаю мафию, монополию, алиас', 'я гик!'))

if first == 'небольшой, знаю мафию, монополию, алиас':
    first_two = st.radio('Хотели бы получить рекомендации по определенной игре?', 
                         (a, 'да!', 'хочу посмотреть топ 20 популярных настольных игр'))
    if first_two == 'да!':
        game_choose = st.selectbox('введите название игры', (df['title'].unique()), index=123)
        st.write('вы выбрали:', game_choose)
        st.table(item_to_rec(model_warp, game_choose).drop_duplicates(subset='item_id')['title'])
        time.sleep(3)
        st.balloons()

    elif first_two == 'хочу посмотреть топ 20 популярных настольных игр':
        st.table(df.groupby('title')['rating'].count().sort_values(ascending=False).head(20))

elif first == 'я гик!':
    geek_first = st.radio('У вас есть акканут на tesera.ru?',
                          (a, 'да, конечно!', 'нет'))
    if geek_first == 'да, конечно!':
        userid = st.selectbox('введите свой username', (df['author_username'].unique()), index=0)
        st.write('вы выбрали:', userid)
        
        ids = df[df['author_username']==userid].id.unique().item()
        recs = recommend_items(model_warp, ids)
        filtered_df = df[df['item_id'].isin(recs)]
        st.table(filtered_df.drop_duplicates(subset='item_id')['title'])

        time.sleep(3)
        st.balloons()
    elif geek_first == 'нет':
        st.write('игры которые могу вас заинтересовать')
        game_choose = st.selectbox('введите название игры', (df['title'].unique()), index=345)
        
        st.table(item_to_rec(model_bpr, game_choose).drop_duplicates(subset='item_id')['title'])
        
        time.sleep(3)
        st.balloons()