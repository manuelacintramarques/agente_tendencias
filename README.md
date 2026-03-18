# Agentes de Tendências

Dois agentes de IA para coleta e análise de tendências de conteúdo no Brasil, com geração de insights estratégicos via GPT-4.

## Agentes

### `agente_1_tendencias.py`
Coleta as 10 pesquisas mais relevantes da semana no Brasil usando **Google Trends** (via `pytrends`) e gera um resumo estratégico de marketing com GPT-4, incluindo temas recomendados, tom, estilo visual, palavras-chave e sugestão de título viral. O resultado é salvo em um arquivo `.txt` com a data do dia.

### `agente_tendencias.py`
Coleta tendências diretamente da aba "Para Você" do **TikTok** usando Selenium, detectando vídeos com alto engajamento. Analisa até 50 trends com GPT-4o, descrevendo o nome da trend, estilo visual e como marcas podem aproveitá-la. Possui interface interativa via **Streamlit**.

## Requisitos

```
openai
streamlit
pytrends
selenium
undetected-chromedriver
schedule
```

## Configuração

Defina a variável de ambiente com sua chave da OpenAI:

```bash
export OPENAI_API_KEY="sua_chave_aqui"
```

## Uso

**Agente Google Trends:**
```bash
python agente_1_tendencias.py
```

**Agente TikTok (Streamlit):**
```bash
streamlit run agente_tendencias.py
```
