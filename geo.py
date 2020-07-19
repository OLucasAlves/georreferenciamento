# Importação das biliotecas
import streamlit as st
import pandas as pd
import base64
import geopy
import folium

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False,float_format='%.10f')
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dados.csv">Download csv file</a>'
    return href


def main():
    st.title('Georreferenciamento')
    st.subheader('Carregue seu arquivo com os endereços')
    file = st.file_uploader(
        'Escolha a base de dados que deseja analisar (.csv)', type='csv')
    if file is not None:
        st.subheader('Analisando os dados')
        df = pd.read_csv(file)
        st.write("**Número de endereços:** " +str(df.shape[0]))
        st.markdown('**Visualizando o dataframe**')
        number = st.slider(
            'Escolha o numero de linhas que deseja ver', min_value=1, max_value=20)
        st.table(df.head(number))
        botao = st.button('Executar')
        if botao:
            georeferenciamento(df)


def georeferenciamento(df):
    dir(geopy)

    from geopy.geocoders import Nominatim
    nom = Nominatim(user_agent="test", timeout=3)

    df["endereco"] = df["Rua"]+", " + \
        df["Bairro"]+", "+df["cidade"]+" "+"CE"

    df["Coodernadas"] = df["endereco"].apply(nom.geocode)

    df["lat"] = df["Coodernadas"].apply(
        lambda x: x.latitude if x != None else None)
    df["lon"] = df["Coodernadas"].apply(
        lambda x: x.longitude if x != None else None)

    dados = df.copy()
    nulos = dados['lat'].isnull().sum()
    st.write("Não conseguimos georreferenciar " + str(nulos) + " endereços")
    
    dados.dropna(axis=0, how='any',inplace=True)
    mapa = folium.Map(location=[-15.788497,-47.879873], zoom_start=4)


    lat = dados["lat"]
    long = dados["lon"] 
    for la, lo in zip(lat, long):
        folium.Marker([la, lo]).add_to(mapa)
    st.markdown(mapa._repr_html_(), unsafe_allow_html =True)

    st.subheader('faça download abaixo : ')
    df['lat'] = df['lat'].apply(str)
    df['lon'] = df['lon'].apply(str)
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)

    st.markdown("**Desenvolvido por:**")
    st.write("Lucas Ribeiro")
if __name__ == '__main__':
    main()
