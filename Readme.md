# LightFun - сервис по рекомендации настольных игр

LightFun позволяет пользователю получать рекомендации по настольным играм, основываясь на его предпочтениях и прошлом опыте игр.

Получить рекомендации по играм [LightFun](https://lihgtfun.streamlit.app/)

# О проекте

Для создания этого проекта были использованы данные, полученные через API сайта о настольных играх tesera.ru и библиотеки для построения рекомендательных систем с помощью матричных разложений LightFM.

![этапы работы](https://i.imgur.com/eD0m6OO.png)


Для проекта рассматривались 3 метода построения рекомендательных систем:
- content-based
- collaborative filtering
- hybrid 

В данной версии проекта используется модель LightFM collaborative filtering


После всех этапов работ был реализован веб апп с помощью фреймворка  [Streamlit](https://streamlit.io/).


1. Парсинг данных(`requests, json`)  
Сайт tesera реализован с открытым API. В итоге получено 2 датасета: содержащий информацию об играх и с информацией о юзере и как он оценил игры (от 1 до 10) .

        
        
    
    
        "modificationDateUtc": "2023-06-18T19:37:56",
        "creationDateUtc": "2015-11-04T08:08:58",
        "photoUrl": "https://s.tesera.ru/images/items/635932,3/photo1.jpg",
        "photoUrl2": "https://s.tesera.ru/images/items/635932,3/photo2.png",
        "year": 2016,
        "ratingUser": 8.84,
        "n10Rating": 8.79,
        "n20Rating": 8.74,
        "bggRating": 8.42,
        "bggGeekRating": 8.166,
        "bggNumVotes": 29659,
        "numVotes": 752,
        "playersMin": 2,
        "playersMax": 4,
        "playersMinRecommend": 2,
        "playersMaxRecommend": 2,
        "playersAgeMin": 14,
        "timeToLearn": 20,
        "playtimeMin": 180,
        "playtimeMax": 240,
        "commentsTotal": 2573,
        "commentsTotalNew": 0,
        "teseraUrl": "https://tesera.ru/game/635932",
        "isAddition": false
    },

2.  EDA (`pandas, numpy, matplotlib, seaborn`)
 
Много пустых игр, дополнений к играм которые представляют из себя лишь одну карточку. Есть аномалии в год выпуска, нулевые рейтинги, дубликаты.

3. Feature engineering (`sklearn, nltk, wordcloud`)
   
Были сформированы новые признаки, удалены неинформативные признаки. Проведена подготовка данных к обучению.

4.  Обучение (`sklearn,  lightfm`)
    
- Рекомендации на основе контента. Текстовые признаки + косинусное расстояние.

- Коллаборативная фильтрация:
	-   lightfm с функцией потерь warp   
	-   lightfm с функцией потерь bgd

- Гибридная модель lightfm 
    

5.  Создание веб аппа (`streamlit`)
    
Импорт сохраненных моделей, скрипты функций для предоставления рекомендации для каждого случая + логика работы.


Логика работы
![enter image description here](https://i.imgur.com/gt54D1S.png)
