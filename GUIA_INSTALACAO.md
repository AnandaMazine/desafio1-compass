# Guia rápido — Cosmetic Bot + DeepEval

## 1. Pré-requisitos
- Python 3.10 ou superior e pip
- Instalar as dependências (de preferência em um ambiente virtual):

```bash
pip install requests deepeval
```

## 2. Colocando o chatbot para rodar

Os arquivos `chatbot.py`, `catalogo.json` e `prompt.txt` devem ficar na mesma pasta. Escolha **uma** das opções abaixo.

### Opção A — Ollama (LLM local)
1. Instale o Ollama: https://ollama.com/download
2. Baixe um modelo leve:

```bash
ollama pull llama3.2:3b
```

3. Rode o bot no modo interativo:

```bash
python chatbot.py
```

### Opção B — Gemini (API gratuita)
1. Gere uma chave em https://aistudio.google.com (menu *API Keys*)
2. Configure as variáveis de ambiente e rode:

```bash
# Linux/macOS
export GEMINI_API_KEY="sua-chave"
export LLM_PROVIDER=gemini
python chatbot.py
```

```powershell
# Windows (PowerShell)
$env:GEMINI_API_KEY = "sua-chave"
$env:LLM_PROVIDER = "gemini"
python chatbot.py
```

### Opção C — Groq (API gratuita)
1. Gere uma chave em https://console.groq.com (menu *API Keys*)
2. Mesmo esquema da opção B, usando `GROQ_API_KEY` e `LLM_PROVIDER=groq`

### Trocando o modelo
Use a variável `LLM_MODEL`. Padrões: `llama3.2:3b` (Ollama), `gemini-2.0-flash` (Gemini), `llama-3.3-70b-versatile` (Groq). Se algum nome de modelo tiver mudado, consulte a documentação do provedor e ajuste por essa variável.

## 3. Usando o bot na sua suíte de avaliação

```python
from chatbot import perguntar

resposta = perguntar("Qual protetor solar você indica para pele oleosa?")
print(resposta)
```

Teste de fumaça rápido, direto no terminal:

```bash
python -c "from chatbot import perguntar; print(perguntar('Quais protetores solares vocês têm?'))"
```

## 4. Configurando o modelo juiz do DeepEval

As métricas do DeepEval usam um LLM como **juiz** para dar as notas. Prefira o modelo mais forte que você tiver disponível — juízes pequenos geram scores instáveis.

### Juiz via Gemini (recomendado)

```python
from deepeval.models import GeminiModel
from deepeval.metrics import AnswerRelevancyMetric

JUIZ = GeminiModel(model="gemini-2.0-flash", api_key="sua-chave")

metrica_a = AnswerRelevancyMetric(threshold=0.7, model=JUIZ)
```

### Juiz via Ollama (100% local)

```bash
deepeval set-ollama llama3.2:3b
```

Atenção: com um juiz de 3B os scores podem oscilar entre execuções. Se optar por esse caminho, registre isso na análise do seu relatório.

Este material foi validado com o DeepEval 4.x. Em caso de erro, consulte a documentação oficial: https://github.com/confident-ai/deepeval

## 5. Exemplo mínimo de teste

Salve como `exemplo_teste.py` na mesma pasta do bot e execute com `deepeval test run exemplo_teste.py`:

```python
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from chatbot import perguntar

def test_exemplo_consulta_direta():
    pergunta = "Quanto custa o Sérum de Vitamina C 10% da Lume?"
    caso = LLMTestCase(
        input=pergunta,
        actual_output=perguntar(pergunta),
        retrieval_context=[
            "Sérum de Vitamina C 10% — Lume — R$ 119,90 — "
            "ingredientes: vitamina C, ácido ferúlico, vitamina E"
        ],
    )
    metrica_a = AnswerRelevancyMetric(threshold=0.7)  # passe model=JUIZ se configurou um juiz
    assert_test(caso, [metrica_a])
```

Esse exemplo cobre só a métrica A em um caso — as métricas B e C, as 4 categorias do dataset e a organização da suíte são o seu trabalho no desafio.

## 6. Limites das APIs gratuitas
- Os free tiers têm limite de requisições por minuto. Rode a suíte com calma, evite reexecuções desnecessárias e, se aparecer erro 429, aguarde um pouco e tente de novo.
- O desafio deve ter **custo zero**: não use chaves de contas pagas.
- Registre no relatório quais modelos (bot e juiz) e versões você utilizou.
