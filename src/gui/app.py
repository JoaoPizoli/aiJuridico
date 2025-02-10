import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

#__import__('pysqlite3')
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

#from streamlit import logger
#import sqlite3

#app_logger = logger.get_logger('SMI_APP')
#app_logger.info(f"sqlite version: {sqlite3.sqlite_version}")

# Add the project root to PYTHONPATH



import streamlit as st
from src.jurisCrew.crews import JusaiCrew
import json

def object_to_text(obj):
    attributes = {key: getattr(obj, key) for key in dir(obj) if not key.startswith('_')}
    return str(attributes)

class jurisCrewUI:

    def generate_jusai(self, topic, description):
        inputs = {
            "topic"      : topic,
            "description": description,
            "num_keys"   : 3
        }

        #output = JusaiCrew().crew().kickoff(inputs=inputs)
        with st.spinner('Gerando saída, aguarde...'):
            return JusaiCrew(input=inputs)

    def jusai_generation(self):

        if st.session_state.generating:
            st.session_state.jusai = self.generate_jusai(st.session_state.topic, st.session_state.description)

        st.write(st.session_state.jusai)
        st.markdown("***Proposta de Defesa para o Caso Descrito:***")
        st.markdown(object_to_text(st.session_state.jusai))
        #st.markdown("#***Consolidação da Pesquisa de Jurisprudências***")
        #st.markdown(object_to_text(st.session_state.jusai.Sout.raw))
        #st.write(st.session_state.jusai.Wcrew.__annotations__)
        #st.write(st.session_state.jusai.__repr__)
        #st.write(st.session_state.jusai.__doc__)
        #st.write(st.session_state.jusai.__dict__)
        #st.text(st.session_state.jusai)

    def sidebar(self):
        with st.sidebar:
            st.title("JUSAI")
            st.write("""
                    To generate ... write,
                    crew will work
                    """)
            
            st.text_input("Tópico", key="topic", 
                        placeholder="ex: Planos de Saúde, Estatuto do Idoso, Código de Desesa do Consumidor ...")
            
            st.text_area("Entre com o seu caso aqui, que vamos procurar as jurisprudências mais aderentes e auxiliá-lo na escrita:", 
                         key="description", 
                        placeholder="Disserte aqui sobre o seu caso. Inclua o máximo de detalhes possível. Se preferir escreva em frases curtas...")
            
            if st.button("Executar"):
                st.session_state.generating = True

    def render(self):
        st.set_page_config(page_title="jurisCrew", page_icon="🤖⚖🤖")
        #st.title(os.listdir())
        st.title("JusAI - Sua IA assistente jurídica")
        

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "description" not in st.session_state:
            st.session_state.description = ""

        if "jusai" not in st.session_state:
            st.session_state.jusai = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()
        self.jusai_generation()

if __name__ == "__main__":

    jurisCrewUI().render()