import streamlit as st
import requests as rq
import json as js


if 'target' not in st.session_state:
    st.session_state['target'] = []

if 'name' not in st.session_state:
    st.session_state['name'] = ''

if 'flag' not in st.session_state:
    st.session_state['flag'] = ''

if 'languages' not in st.session_state:
    st.session_state['languages'] = []

if 'targetCont' not in st.session_state:
    st.session_state['targetCont'] = ''

if 'contInfo' not in st.session_state:
    st.session_state['contInfo'] = []

if 'contLangs' not in st.session_state:
    st.session_state['contLangs'] = []

if 'langDict' not in st.session_state:
    st.session_state['langDict'] = {}


def titleSection():
    st.title('Languages Around the World')
    st.header('What Languages are spoken near you?')
    st.write('---')
titleSection()

def selectCountry():
    st.subheader('What Languages are Spoken in a Country?')
    st.text('Enter your country below.')
    target = st.text_input("Country")
    if target:
        st.session_state['target'] = target
selectCountry()

def langOut():
    country = st.session_state['target']
    info = rq.get(f'https://restcountries.com/v3.1/name/{country}', verify=False)
    countryInfo = info.json()
    langList = []
    try:
        name = countryInfo[0]["name"]['common']
        if name:
            st.session_state['name'] = name

        flag = countryInfo[0]["flags"]['png']
        if flag:
            st.session_state['flag'] = flag
        
        languages = countryInfo[0]['languages']
        if languages:
            st.session_state['languages'] = languages

        st.image(flag)
        st.subheader(f'Languages spoken in {name}.')
        for key, term in st.session_state['languages'].items():
            st.write(f'- {term}')

    except:
        st.error("Country not found, please try again.")
if st.session_state['target'] != []:
    langOut()
    st.session_state['target'] = []

st.write('---')

def selectContinent():
    st.subheader('Languages Spoken by Continent')

    targetCont = st.selectbox(
        'Choose your Continent',
        ('Africa', 'Asia', 'Europe', 'North America', 'South America', "Oceania")
    )

    if targetCont:
        st.session_state['targetCont'] = targetCont
selectContinent()

def contGraph():
    targetCont = st.session_state['targetCont']
    info = rq.get(f'https://restcountries.com/v3.1/region/{targetCont}', verify=False)
    contInfo = info.json()
    if contInfo:
        st.session_state['contInfo'] = contInfo

    contLangs = []
    langDict = {}
    for continent in st.session_state['contInfo']:
        languages = continent['languages']
        for key, term in languages.items():
            if term in contLangs:
                langDict[(term)] += 1
            else:
                contLangs += (term,)
                langDict[(term)] = 1
    if langDict != {}:
        st.session_state['langDict'] = langDict
    st.bar_chart(data=st.session_state['langDict'], x_label='Languages', y_label='Number of Countries')
if st.session_state['targetCont'] != []:
    contGraph()
    st.session_state['targetCont'] = []
            





    

