# Demos da Masterclass — Semana 3

Quatro exemplos progressivos de DeepEval, com respostas fixas no código
(sem chamar chatbot nenhum): a demo fica rápida e previsível ao vivo.

## Setup (antes da aula)

```bash
pip install deepeval ollama
```

O juiz padrão é o **Ollama local** — basta ele estar rodando e o modelo baixado:

```bash
ollama pull llama3.2:3b
```

Para um juiz mais estável (se a máquina aguentar), use um modelo maior:

```bash
ollama pull qwen2.5:7b               # e rode com:
JUIZ_MODEL=qwen2.5:7b python demo_01_relevancia.py   # Windows: $env:JUIZ_MODEL="qwen2.5:7b"
```

Alternativa via API: `pip install google-genai`, defina `GEMINI_API_KEY` e rode com `JUIZ_PROVIDER=gemini`.

## Ordem de apresentação

```bash
python demo_01_relevancia.py    # Answer Relevancy: boa vs fora do assunto
python demo_02_fidelidade.py    # Faithfulness: fiel vs preço/produto inventado
python demo_03_geval.py         # G-Eval: critérios de claims (cosméticos)
deepeval test run demo_04_pytest.py   # tudo como suíte pytest
```

Na demo 4, descomente o teste final para mostrar uma falha ao vivo.

## Dicas
- Rode tudo uma vez antes da aula (valida o juiz e aquece a apresentação).
- Leia o `reason` do juiz em voz alta — é onde está o aprendizado.
- Free tiers têm limite de requisições por minuto; se aparecer erro 429,
  aguarde alguns segundos e rode de novo.
- Material validado com DeepEval 4.x.
