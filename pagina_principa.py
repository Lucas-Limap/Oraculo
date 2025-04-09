import streamlit as st

TIPOS_DE_ARQUIVOS_VALIDOS = [
    'Site', 'Youtube', 'PDF', 'CSV', 'TXT'

]

CONFIG_MODELOS = {
    'Groq': {'modelos': ['llama3-70b-8192', 'gemma2-9b-it', 'whisper-large-v3']},
    'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o']}
}

MENSAGEM_EXEMPLO = [
    ('user','Olá!'),
    ('assistant','Olá! Tudo bem?'),
    ('user', 'Tudo ótimo'),

]

def pagina_chat():
    st.header('Bem-vindo ao Oráculo', divider=True )

    mensagens=st.session_state.get('mensagens', []) 

    mensagens = st.session_state.get('mensagens', MENSAGEM_EXEMPLO)
    for mensagem in mensagens:
        chat= st.chat_message(mensagem[0])
        chat.markdown(mensagem[1])

    input_usuario= st.chat_input('Fale com o oráculo:')
    if input_usuario:
        mensagens.append(('user',input_usuario))

        st.session_state['mensagens'] = mensagens
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



def main():
    pagina_chat()
    with st.sidebar:
        sidebar()


if __name__ == '__main__':
    main()
