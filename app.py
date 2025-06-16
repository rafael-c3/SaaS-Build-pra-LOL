import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gerador de Builds - LoL com Gemini", page_icon=":game_die:")
st.title("BUILD GAP")

genai.configure(api_key="AIzaSyDmlAswr06Fnw7YgulArivaF7vHIA5AnCk")
model = genai.GenerativeModel('gemini-1.5-flash')

campeao = st.text_input("Qual campeão você está usando?")

forma_kayn = ""
if campeao.strip().lower() == "kayn":
    forma_kayn = st.selectbox("Qual forma do Kayn você está usando?", ["Kayn Azul (Assassino das Sombras)", "Kayn Vermelho (Rhaast)"])

modo_jogo = st.selectbox("Qual modo de jogo?", ["Normal", "Ranked", "ARAM"])

rota = st.selectbox("Qual rota você está jogando?", ["Top", "Jungle", "Mid", "ADC", "Suporte"])

adversario = st.text_input("Qual campeão adversário?")

ameaça_adversario = st.radio("O campeão adversário é uma ameaça para você?", ["Sim", "Não"])

preferencia_build = st.radio("Preferência de Build? (Opcional)", ["", "AP", "AD"])

st.subheader("Seu time (opcional):")
time_aliado = []
for i in range(4):
    champ = st.text_input(f"Campeão aliado {i+1} (opcional):")
    time_aliado.append(champ)

st.subheader("Time inimigo (opcional):")
time_inimigo = []
for i in range(4):
    champ = st.text_input(f"Campeão inimigo {i+1} (opcional):")
    time_inimigo.append(champ)

if st.button("Gerar Recomendação com Gemini"):
    prompt = f"Estou jogando League of Legends com o campeão {campeao} no modo {modo_jogo}, na rota {rota}.\n"

    if forma_kayn:
        prompt += f"Estou usando a forma: {forma_kayn}.\n"

    prompt += f"Meu oponente na lane é {adversario}.\n"
    if ameaça_adversario == 'Sim':
        prompt += f"Considero o {adversario} uma ameaça para mim.\n"

    aliados = [c for c in time_aliado if c]
    inimigos = [c for c in time_inimigo if c]

    if aliados:
        prompt += f"Meus aliados são: {', '.join(aliados)}.\n"
    if inimigos:
        prompt += f"Os inimigos além do meu oponente são: {', '.join(inimigos)}.\n"

    if preferencia_build:
        prompt += f"Prefiro builds focadas em {preferencia_build}.\n"

    prompt += "Qual build você recomenda para essa situação? Desde Itens iniciais até o EndGame"

    st.subheader("📝 Prompt Gerado:")
    st.text_area("Prompt para Gemini:", value=prompt, height=250)

    with st.spinner("Consultando o Gemini..."):
        response = model.generate_content(prompt)
        resposta = response.text

    st.subheader("🔍 Resposta do Gemini:")
    st.write(resposta)
