import streamlit as st
from langchain.memory import ConversationBufferMemory

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

TIPOS_DE_ARQUIVOS_VALIDOS = [
    'Site', 'Youtube', 'PDF', 'CSV', 'TXT'

]

CONFIG_MODELOS = {
    'Groq': {'modelos': ['llama3-70b-8192', 'gemma2-9b-it', 'whisper-large-v3'],
             'chat': ChatGroq},
    'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o'],
               'chat':ChatOpenAI}
}

MENSAGEM_EXEMPLO = [
    ('user','Olá!'),
    ('assistant','Olá! Tudo bem?'),
    ('user', 'Tudo ótimo'),

]


MEMORIA = ConversationBufferMemory()


def carrrga_modelo(provedor, modelo, api_key):
    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo,api_key=api_key)
    st.session_state['chat']= chat



def pagina_chat():
    st.header('Bem-vindo ao Oráculo', divider=True )


    chat_model= st.session_state.get('chat')
    memoria=st.session_state.get('memoria', MEMORIA) 
    for mensagem in memoria.buffer_as_messages:
        chat= st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario= st.chat_input('Fale com o oráculo:')
    if input_usuario:
        memoria.chat_memory.add_user_message(input_usuario)
        resposta = chat_model.invoke(input_usuario).content
        memoria.chat_memory.add_ai_message(resposta)
        

        st.session_state['memoria'] = memoria
        st.rerun()

def sidebar():
    tabs = st.tabs(['Upload de Arquivos', 'Seleção de Modelos'])   
    with tabs[0]:  
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo:', TIPOS_DE_ARQUIVOS_VALIDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a url do site:')
        if tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite a url do Youtube:')
        if tipo_arquivo == 'PDF':
            arquivo = st.file_uploader('Faça o upload do PDF:', type=['.pdf'])            
        if tipo_arquivo == 'CSV':
            arquivo = st.file_uploader('Faça o upload do CSV:', type=['.csv'])
        if tipo_arquivo == 'TXT':
            arquivo = st.file_uploader('Faça o upload do TXT:', type=['.txt'])


    with tabs[1]:
        provedor = st.selectbox('Selecione o provedor do modelo:', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Selecione um modelo:', CONFIG_MODELOS[provedor]['modelos'])
        api_key = st.text_input(
            f'Selecione a API Keys para o proverdor {provedor}:',
            value=st.session_state.get(f'api_keys_{provedor}'))

        st.session_state[f'api_keys_{provedor}'] = api_key

    if st.button('Inicializar Oráculo', use_container_width=True):
        carrrga_modelo(provedor, modelo, api_key)



def main():
    pagina_chat()
    with st.sidebar:
        sidebar()


if __name__ == '__main__':
    main()
