import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from streamlit_option_menu import option_menu
from  PIL import Image



st.set_page_config(page_title="Delitos en México",page_icon="🛑",layout="wide")

@st.cache_data
def load_data(file,geojson):
#Creamos un dataframe para leer la base de datos
  df=pd.read_csv(file)
  mex = requests.get(geojson).json()
  return df,geojson

df,mex=load_data("/content/IDEFC_NM_sep23.csv","https://raw.githubusercontent.com/jeaggo/datasets/master/states_mexico.geojson")

familia = Image.open(r'/content/familia.jpg')
violencia_familiar = Image.open(r'/content/violencia-familiar.jpg')
logo=Image.open(r'/content/Yosu logo png.png')

#Sustituimos los valores nulos por 0
df.fillna(0, inplace=True)

#Creamos un conteo del total de delitos por mes para asi tener un conteo anual
df["anual"]=df["Enero"]+df["Febrero"]+df["Marzo"]+df["Abril"]+df["Mayo"]+df["Junio"]+df["Julio"]+df["Agosto"]+df["Septiembre"]+df["Octubre"]+df["Noviembre"]+df["Diciembre"]

#Eliminamos las columnas que no seran de utilidad para nuestro analisis
df.drop(columns=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre","Bien jurídico afectado","Subtipo de delito","Modalidad"],inplace=True)

delitos=df["Tipo de delito"].unique()
anos=df["Año"].unique()

dfcrimenesporano=df.groupby("Año")["anual"].sum()
dfcrimenesporano=dfcrimenesporano.reset_index()
dfcrimenesporano["pais"]="México"

dfdel=pd.DataFrame(df.groupby(["Clave_Ent","Entidad"])["anual"].sum())
dfdel=dfdel.reset_index()
dfdel.sort_values(by="anual",inplace=True)

dfcdmx=pd.DataFrame(df.loc[(df["Entidad"]=="Ciudad de México")].groupby(["Clave_Ent","Entidad","Tipo de delito"])["anual"].sum())
dfcdmx=dfcdmx.reset_index()
dfcdmx=dfcdmx.loc[dfcdmx["anual"]!=0]

figlinea = px.line(dfcrimenesporano, x="Año", y="anual",
                   title="Delitos en México",
                   text="anual",
                   color="pais",
                   color_discrete_sequence=px.colors.sequential.YlOrRd_r,
                   labels={'anual':"Delitos","pais":"País"}
                   )
figlinea.update_traces(textposition="bottom right")
figlinea.update_layout(
  title="Delitos en México a traves del tiempo",
  xaxis_title="Año",
  yaxis_title="Delitos",
)

figdel = px.bar(dfdel, x='Entidad', y='anual',
             title="Delitos en México por estados",
             color="anual",
             color_continuous_scale="YlOrRd",
             labels={"anual":"Delitos"}
             )

figcdmx = px.treemap(dfcdmx, path=["Entidad","Tipo de delito"],
                 values="anual",
                 color="anual",
                 color_continuous_scale="YlOrRd",
                 labels={"anual":"Delitos"}
                 )
figcdmx.update_traces(root_color="lightgrey")
figcdmx.update_layout(margin = dict(t=50, l=25, r=25, b=25))

with st.sidebar:
  menu = option_menu(None, ["Inicio", "Storytelling",  "KPI's", "Mapa de México"],
      icons=['house', 'book', "bar-chart-steps", 'globe-americas'],
      menu_icon="cast", default_index=1,
      styles={
          "container": {"padding": "0!important", "background-color": "#262730"},
          "icon": {"color": "#feac49", "font-size": "25px"},
          "nav-link": {"font-size": "25px", "text-align": "left", "margin":"5px", "--hover-color": "#9ea3c8"},
          "nav-link-selected": {"background-color": "#62657c"},
      }
  )

if menu == "Inicio":
  logoizq,logoenmedio,logoder=st.columns([0.3,0.4,0.3])
  with logoenmedio:
    st.image(logo,  width=600)
  st.write("""
  Somos una consultoría especializada en el análisis de datos para ayudar a las organizaciones a tomar mejores decisiones.
  Ofrecemos soluciones a medida para cada cliente, utilizando las últimas tecnologías y metodologías de análisis de datos.
  Nos adaptamos a las necesidades de nuestros clientes con el fin de ofrecer el mejor servicio ajustandonos a los presupuestos
  de cada empresa, ya sea pequeña, mediana o una franquicia. Estamos preparados para brindar soluciones a cualquier
  problema de analisis de datos que se presente.
  """)

elif menu == "Storytelling":

  izq, enmedio ,der = st.columns([0.1,0.35,0.1])
  with enmedio:
    st.header('**El caso de Sofia**')
    st.divider()

    izq1, der1 = st.columns([0.55,0.45])
    with izq1:
      st.write("""
      Sofia era una joven de 25 años que vivía con su esposo Luis, de 28 años, y su hijo mateo, de 5 años. Sofía trabajaba como enfermera en un hospital cercano, mientras que
      Luis era mecánico en un taller. Aunque al principio de su relación Luis era cariñoso y atento con Sofía, con el tiempo se volvió celoso, controlador y violento. Le revisaba
      el celular, le prohibía salir con sus amigas y le exigía que le entregara todo su sueldo. Si Sofía se negaba o le reclamaba algo, Luis la golpeaba, la insultaba y la amenazaba con quitarle a su hijo.
      """)

    with der1:
      st.image(familia,  use_column_width=True)

    izq2, der2 = st.columns([0.40,0.60])
    with der2:
      st.write("""
      Un día, Luis llegó borracho y drogado al departamento, y empezó a discutir con Sofía. Le acusó de haberlo
      engañado con un compañero de trabajo, y le dio una cachetada que la tiró al suelo. Sofía se levantó y trató
      de defenderse, pero Luis la agarró del pelo y la arrastró hasta el baño. Allí, la encerró y le prendió
      fuego a la puerta, mientras le gritaba que se iba a morir. Sofía se desesperó y empezó a toser por el humo.
      Intentó romper la ventana, pero estaba demasiado alta y no tenía nada con qué romperla. Luis se burlaba de ella desde afuera, y le decía que se despidiera de su hijo.
       """)
    with izq2:
      st.image(violencia_familiar,  use_column_width=True)

    st.write("""
    Mateo estaba en su cuarto y escuchó los gritos de su madre asi que salió a ver qué pasaba. Al ver el fuego y a su padre riéndose,
    se asustó y corrió a la cocina. Allí, vio un teléfono y recordó que su madre le había enseñado a marcar el 911 en caso de emergencia.
    Mateo tomó el teléfono y marcó el número. Una voz le contestó y le preguntó qué necesitaba. Mateo, con voz temblorosa, dijo: “Mi papá
    le pegó a mi mamá y le prendió fuego al baño. Ayúdenme, por favor”. Llegaron patrullas, bomberos y una ambulancia.

    Sofía y Mateo fueron trasladados al hospital, donde recibieron atención médica. Sofía se recuperó de sus heridas físicas, pero quedó con secuelas
    psicológicas. Mateo también sufrió un trauma por lo que vivió, y tuvo que recibir terapia. Luis fue procesado por el delito de violencia familiar
    agravada, y fue condenado a 15 años de prisión.
    """)

    st.empty().text("")

    st.write("""
    La situación en la que se encuentra México es alarmante, la cantidad de delitos ocurridos durante los últimos años ha ido prácticamente en aumento, tomando
    en cuenta factores como la pandemia o que los datos de 2023 solamente llegan a septiembre.
    """)

    st.plotly_chart(figlinea,use_container_width=True, theme="streamlit")

    st.write("""
    Sofia es de la Ciudad de México, el estado con la segunda mayor cantidad de delitos cometidos, esto se puede deber a que en este estado se encuentra entre los
    estados con mayor densidad de población o algunos otros factores relacionados con la seguridad.

    """)

    st.plotly_chart(figdel,use_container_width=True, theme="streamlit")

    st.write("""
    Sofia vivió un caso de violencia familiar, la violencia familiar es el segundo delito más común en la Ciudad de México, donde solamente se encuentra el robo por encima.
    Los casos de violencia familiar son muy preocupantes, ya que son casos que se viven durante muchos años, y muchas veces este tipo de casos no suelen salir a la luz hasta que hay una muerte.
    """)

    st.plotly_chart(figcdmx,use_container_width=True, theme="streamlit")

elif menu == "KPI's":

  tab1,tab2,tab3,tab4=st.tabs(["Delitos por año en México","Delitos por estado en México","Tipos de delitos más cometidos en México","Tipos de delitos cometidos por estado en México"])

  with tab1:
    coltab1,coltab11,coltab111=st.columns([0.2,0.6,0.4])
    with coltab1:
      st.empty().text("")
      anuales = st.selectbox(
      'Año',
      anos,
      placeholder="Escoge un año",
      index=None,
      )


    if anuales==None:
      dfcrimenesporano=df.groupby("Año")["anual"].sum()
      dfcrimenesporano=dfcrimenesporano.reset_index()
      dfcrimenesporano["pais"]="México"
      delitosporanovalor=dfcrimenesporano["anual"].sum()
      nombredelitosporano="Delitos en total"
    else:
      dfcrimenesporano=pd.DataFrame(df.loc[df["Año"]==anuales].groupby("Año")["anual"].sum())
      dfcrimenesporano=dfcrimenesporano.reset_index()
      dfcrimenesporano["pais"]="México"
      delitosporanovalor=dfcrimenesporano["anual"]
      nombredelitosporano="Delitos/año"

    figlineanos = px.line(dfcrimenesporano, x="Año", y="anual",
                      title="Delitos en México",
                      text="anual",
                      color="pais",
                      color_discrete_sequence=px.colors.sequential.YlOrRd_r,
                      labels={'anual':"Delitos","pais":"País"}
                      )
    figlineanos.update_traces(textposition="bottom right")
    figlineanos.update_layout(
      title="Delitos en México a traves del tiempo",
      xaxis_title="Año",
      yaxis_title="Delitos",
    )

    with coltab111:
      roundelito=round(delitosporanovalor/1000000,2)
      st.empty().text("")
      st.metric(label=nombredelitosporano, value= "%2.2f M" %roundelito)

    st.plotly_chart(figlineanos,use_container_width=True, theme="streamlit")

  with tab2:
    coltab2,coltab22,coltab222=st.columns([0.45,0.6,0.4])
    with coltab2:
      st.empty().text("")
      estadoselect=st.selectbox(
      "Estado",
      df["Entidad"].unique(),
      placeholder="Escoge un estado",
      index=None,
      key="hola"
      )

    if estadoselect==None:
      dfdel=pd.DataFrame(df.groupby(["Clave_Ent","Entidad"])["anual"].sum())
      dfdel=dfdel.reset_index()
      dfdel.sort_values(by="anual",inplace=True)
      delitosporanovalor=dfdel["anual"].sum()
      nombredelitosporano="Delitos en total"

    else:
      dfdel=pd.DataFrame(df.loc[df["Entidad"]==estadoselect].groupby(["Clave_Ent","Entidad"])["anual"].sum())
      dfdel=dfdel.reset_index()
      delitosporanovalor=dfdel["anual"].sum()
      nombredelitosporano="Delitos en el estado"

    figdeltab = px.bar(dfdel, x='Entidad', y='anual',
             title="Delitos en México por estados",
             color="anual",
             color_continuous_scale="YlOrRd",
             labels={"anual":"Delitos"}
             )


    with coltab222:
      if (delitosporanovalor>=1000000):
        roundelito="%2.2f M" %round(delitosporanovalor/1000000,2)
      else:
        roundelito="%2.2f K" %round(delitosporanovalor/1000,2)
      st.empty().text("")
      st.metric(label=nombredelitosporano, value=roundelito)

    st.plotly_chart(figdeltab,use_container_width=True, theme="streamlit")

  with tab3:

    dftipodedelito=pd.DataFrame(df.groupby("Tipo de delito")["anual"].sum())
    dftipodedelito=dftipodedelito.reset_index()
    dftipodedelito.sort_values(by="anual",ascending=False,inplace=True)
    dftipodedelito=dftipodedelito.head(5)

    figtipodelitobola=px.pie(dftipodedelito,values="anual",names=dftipodedelito["Tipo de delito"],
                      title="Los 5 tipos de delitos más comunes en México",
                      color_discrete_sequence=px.colors.sequential.YlOrRd_r
    )

    coltab3,coltab33,coltab333=st.columns([0.4,0.4,0.4])
    with coltab3:
      st.empty().text("")
      st.metric(label="Tipo de delito más cometido", value=str(dftipodedelito["Tipo de delito"].iloc[0]))

    with coltab333:
      st.empty().text("")
      st.metric(label="No. de delitos del tipo de delito mas común", value="%2.2f M" %round((dftipodedelito["anual"].iloc[0])/1000000,2))

    st.plotly_chart(figtipodelitobola,use_container_width=True, theme="streamlit")

  with tab4:
    coltab4,coltab44,coltab444=st.columns([0.4,0.5,0.3], gap="large")
    with coltab4:
      estadoselect=st.selectbox(
      "Estado",
      df["Entidad"].unique(),
      placeholder="Escoge un estado",
      key="adios"
      )

    dftipodedelitoestado=pd.DataFrame(df.loc[df["Entidad"]==estadoselect].groupby(["Entidad","Tipo de delito"])["anual"].sum())
    dftipodedelitoestado=dftipodedelitoestado.reset_index()
    dftipodedelitoestado.sort_values(by="anual",ascending=False,inplace=True)
    dftipodedelitoestado=dftipodedelitoestado.loc[dftipodedelitoestado["anual"]!=0]

    with coltab44:
      st.metric(label="Tipo de delito más común" , value=str(dftipodedelitoestado["Tipo de delito"].iloc[0]))

    with coltab444:
      if dftipodedelitoestado["anual"].iloc[0]>=1000000:
        valortipoporestado= "%2.2f M" %round(dftipodedelitoestado["anual"].iloc[0]/1000000,2)
      elif dftipodedelitoestado["anual"].iloc[0]>=1000:
        valortipoporestado= "%2.2f K" %round(dftipodedelitoestado["anual"].iloc[0]/1000,2)

      st.metric(label="No. de delitos del delito mas común" , value=valortipoporestado)

    figtipoestado = px.treemap(dftipodedelitoestado, path=["Entidad","Tipo de delito"],
                 values="anual",
                 color="anual",
                 color_continuous_scale="YlOrRd",
                 labels={"anual":"Delitos"}
                 )
    figtipoestado.update_traces(root_color="lightgrey")
    figtipoestado.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    st.plotly_chart(figtipoestado,use_container_width=True, theme="streamlit")




elif menu == "Mapa de México":

  st.header('Delincuencia en México')

  colestadoselect, coldelito, colano = st.columns([0.3,0.4,0.3],gap="large")

  with colestadoselect:
    estadoselect=st.selectbox(
    'Estado',
    df["Entidad"].unique(),
    placeholder="Escoge un estado",
    index=None
    )

  with coldelito:
    scale = st.selectbox(
        'Tipo de delito',
        delitos)

  with colano:
    anuales = st.selectbox(
        'Año',
        anos,
        placeholder="Escoge un año",
        index=None,
        )


  if (anuales==None)&(estadoselect==None):
    dfdelitos=pd.DataFrame(df.loc[(df["Tipo de delito"]==scale)].groupby(["Clave_Ent","Entidad"])["anual"].sum())
    dfdelitos=dfdelitos.reset_index()

  elif estadoselect==None:
    dfdelitos=pd.DataFrame(df.loc[(df["Tipo de delito"]==scale)&(df["Año"]==anuales)].groupby(["Año","Clave_Ent","Entidad"])["anual"].sum())
    dfdelitos=dfdelitos.reset_index()

  elif anuales==None:
    dfdelitos=pd.DataFrame(df.loc[(df["Tipo de delito"]==scale)&(df["Entidad"]==estadoselect)].groupby(["Clave_Ent","Entidad"])["anual"].sum())
    dfdelitos=dfdelitos.reset_index()

  else:
    dfdelitos=pd.DataFrame(df.loc[(df["Tipo de delito"]==scale)&(df["Entidad"]==estadoselect)&(df["Año"]==anuales)].groupby(["Año","Clave_Ent","Entidad"])["anual"].sum())
    dfdelitos=dfdelitos.reset_index()


  fig = px.choropleth(dfdelitos, geojson=mex, featureidkey='properties.state_code',
                      locations='Clave_Ent', color='anual',
                      hover_name='Entidad',
                      color_continuous_scale="YlOrRd",
                      title='Numero de delitos en México por año',
                      labels={'anual':scale}
  )

  fig.update_geos(fitbounds="locations", visible=False)

  fig.update_layout(
      autosize=False,
      width=1000,
      height=700,
  )

  st.plotly_chart(fig,use_container_width=True, theme="streamlit")
