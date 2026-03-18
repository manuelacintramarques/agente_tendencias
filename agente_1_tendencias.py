from pytrends.request import TrendReq
import openai
import os
import schedule
import time
from datetime import date

openai.api_key = os.environ["OPENAI_API_KEY"]

def coletar_tendencias():
    pytrends = TrendReq(hl='pt-BR', tz=360)
    pytrends.build_payload(kw_list=["tiktok", "reels", "vídeo curto"], timeframe='now 7-d', geo='BR')
    dados = pytrends.related_queries()
    termos = []

    for palavra in dados:
        if dados[palavra]['top'] is not None:
            termos += dados[palavra]['top']['query'].tolist()

    return termos[:10]

def gerar_resumo(tendencias):
    prompt = f"""
Você é um analista de marketing especializado em vídeos curtos. Com base nas 10 pesquisas mais relevantes no Brasil esta semana, crie um resumo estratégico para criação de conteúdo viral.  
Pesquisas: {', '.join(tendencias)}

O resumo deve conter:
1. Temas recomendados
2. Tom do vídeo (ex: humor, emoção, mistério)
3. Estilo visual sugerido
4. Palavras-chave a serem usadas
5. Exemplo de título para um vídeo viral

Seja direto, profissional e estratégico.
    """
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return resposta['choices'][0]['message']['content']

def executar_agente():
    hoje = date.today().strftime("%d-%m-%Y")
    tendencias = coletar_tendencias()
    resumo = gerar_resumo(tendencias)

    with open(f"resumo_tendencias_{hoje}.txt", "w", encoding="utf-8") as f:
        f.write("Tendências capturadas:\n")
        for t in tendencias:
            f.write(f"- {t}\n")
        f.write("\nResumo estratégico:\n")
        f.write(resumo)

    print(f"[{hoje}] Agente executado com sucesso!")

# Executar imediatamente (sem esperar 08:00)
executar_agente()
