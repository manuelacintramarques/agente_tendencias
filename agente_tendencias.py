import os
import streamlit as st
import openai
import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# CONFIGURAÇÕES
openai.api_key = os.environ["OPENAI_API_KEY"]
TEMPO_COLETA = 180  # segundos coletando tendências

# --- COLETA DO TIKTOK ---
def coletar_tendencias_tiktok(duracao=180):
    options = uc.ChromeOptions()
    # options.add_argument("--headless=new")  ← comente isso
    driver = uc.Chrome(options=options)
    driver.get("https://www.tiktok.com/foryou")
    time.sleep(8)

    tendencias = []
    start = time.time()
    vistos = set()

    while time.time() - start < duracao:
        try:
            cards = driver.find_elements(By.XPATH, '//div[contains(@class,"video-feed-item")]')
            for card in cards:
                try:
                    texto = card.text
                    if 'mi visualizações' in texto.lower() or 'm views' in texto.lower():
                        audio = card.find_element(By.TAG_NAME, "strong").text
                        chave = (audio, texto)
                        if chave not in vistos:
                            tendencias.append({
                                "views": texto,
                                "audio": audio,
                                "raw_text": texto
                            })
                            vistos.add(chave)
                except:
                    continue
            ActionChains(driver).scroll_by_amount(0, 500).perform()
            time.sleep(3)
        except:
            break

    driver.quit()
    return tendencias

# --- ANÁLISE COM GPT ---
def descrever_trends(lista):
    descritas = []

    for t in lista[:50]:
        prompt = f"""
Você é um analista de tendências que trabalha com marketing no Brasil.

Crie uma descrição criativa de uma trend do TikTok com base no áudio e texto abaixo. Diga:

1. Nome da Trend (ex: Trend da Cleópatra, Trend do Zoom Cômico)
2. Descrição visual: como é o estilo, edição, estética ou piada?
3. Como marcas podem aproveitar essa trend

Texto do vídeo:
"{t['raw_text']}"

Áudio:
"{t['audio']}"
"""
        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            conteudo = resposta["choices"][0]["message"]["content"]
            partes = conteudo.strip().split("\n", 2)
            nome = partes[0].replace("Nome da Trend:", "").strip() if "Nome" in partes[0] else "Trend sem nome"
            desc = partes[1].strip() if len(partes) > 1 else ""
            uso = partes[2].strip() if len(partes) > 2 else ""

            descritas.append({
                "nome": nome,
                "descricao": desc,
                "como_usar": uso,
                "views": t["views"],
                "audio": t["audio"]
            })
        except Exception as e:
            print("Erro ao gerar descrição:", e)
            continue

    return descritas

# --- INTERFACE COM STREAMLIT ---
def mostrar_dashboard(tendencias):
    st.set_page_config(page_title="Agente de Tendências", layout="wide")
    st.title("🔥 Top 50 Tendências Atuais (TikTok Brasil)")
    st.markdown("Este agente coleta dados reais da aba 'Para Você' e analisa as trends com GPT-4o.")

    for t in tendencias:
        st.subheader(t["nome"])
        st.markdown(f"**Views:** {t['views']}")
        st.markdown(f"**Áudio:** {t['audio']}")
        st.markdown(f"**Descrição:** {t['descricao']}")
        st.markdown(f"**Como marcas podem usar:** {t['como_usar']}")
        st.markdown("---")

# --- EXECUÇÃO COMPLETA ---
def executar_agente():
    st.title("🤖 Agente de Inteligência de Tendências")
    st.write("Clique abaixo para iniciar a coleta de dados e geração de tendências reais do TikTok.")

    if st.button("📡 Rodar Agente"):
        with st.spinner("Coletando dados do TikTok..."):
            brutas = coletar_tendencias_tiktok(TEMPO_COLETA)

        st.success(f"{len(brutas)} vídeos detectados. Gerando análise...")

        with st.spinner("Analisando com GPT-4o..."):
            descritas = descrever_trends(brutas)

        with open("tendencias_atuais.json", "w", encoding="utf-8") as f:
            json.dump(descritas, f, ensure_ascii=False, indent=2)

        st.success("Tendências processadas com sucesso! 🎉")
        mostrar_dashboard(descritas)

    # Mostrar últimas tendências salvas
    elif st.button("📂 Ver Últimas Tendências Salvas"):
        try:
            with open("tendencias_atuais.json", "r", encoding="utf-8") as f:
                trends = json.load(f)
            mostrar_dashboard(trends)
        except:
            st.error("Nenhuma tendência salva ainda.")

# --- RODAR APP ---
if __name__ == "__main__":
    executar_agente()
