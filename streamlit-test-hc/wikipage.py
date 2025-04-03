import streamlit as st 
import databases.controllers as db

def return_all_infos():
    return db.get_plague_database('databases/plague.db')
    

def wiki_page_file():
    data_from_db = return_all_infos()  

    list_tuple_name = ()
    for i in range(len(data_from_db)):
        list_tuple_name += (data_from_db[i][1],)


    st.title('Wiki Life', anchor=False)

    option = st.selectbox(
        "Qual bactéria deseja pesquisar?",
        list_tuple_name
    )

    get_info_plague = db.get_single_plague_database('databases/plague.db', option)


    st.subheader("Bactéria: ", anchor=False)
    st.title(get_info_plague[0][1], anchor=False)
    fake_col1, fake_col2, fake_col3 = st.columns(3)
    
    with fake_col1:
        pass
    with fake_col2:
        st.image(get_info_plague[0][9], use_container_width=True, caption=get_info_plague[0][1], width=10)
    with fake_col3:
        pass    
    st.markdown('------')


    col1, col2, col3 = st.columns(3, border=True)

    with col1:
        st.header("Tipo: ", anchor=False)
        st.subheader(get_info_plague[0][2], anchor=False)

    with col2:
        st.header("Sintomas: " , anchor=False)
        st.subheader(get_info_plague[0][5],  anchor=False)
        
    with col3:
        st.header("Localização: ", anchor=False)
        st.subheader(get_info_plague[0][3],  anchor=False)


    st.markdown('------')
    colb1, colb2, colb3 = st.columns(3, border=True)

    with colb1:
        st.header("Prevenção: ", anchor=False)
        st.subheader(get_info_plague[0][8], anchor=False)   

    with colb2:
        st.header("Medicamentos: ", anchor=False)
        st.subheader(get_info_plague[0][6], anchor=False)

    with colb3:
        st.header("Dicas: ", anchor=False)
        st.subheader(get_info_plague[0][7], anchor=False)

