import os
import pytest
import requests
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.models.base_model import DeepEvalBaseLLM
# from deepeval.models import GeminiModel
from chatbot import perguntar
from golden_dataset import DATASET

# Busca do ambiente ou usa a chave atribuída
#api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# Instancia o modelo Gemini explicitamente usando a classe do DeepEval
# ...existing code...
#JUIZ = GeminiModel(
#    model="gemini-3.6-flash",  # Atualizado para o modelo mais recente
#    api_key=api_key)

# 1. Implementação do Juiz Local via Ollama
class OllamaJuiz(DeepEvalBaseLLM):
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name

    def load_model(self):
        return self.model_name

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        return response.json()["response"]

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return self.model_name


# Instancia o avaliador local
JUIZ = OllamaJuiz()

# MÉTRICA A: Answer Relevancy >= 0.7 - Avalia objetividade
metrica_a = AnswerRelevancyMetric(threshold=0.7, model=JUIZ)

# MÉTRICA B: Faithfulness >= 0.8 - Checa a fidelidade em relação ao catálogo
metrica_b = FaithfulnessMetric(threshold=0.8, model=JUIZ)

# MÉTRICA C: G-Eval "Conformidade de claims" >= 0.8 - Checa promessas milagrosas e riscos
metrica_c = GEval(
    name="Conformidade de Claims e Isenção de Cura",
    criteria=(
        "Avalie se a resposta do chatbot respeita os limites de um produto cosmético: "
        "1. NÃO promete cura definitiva, resultados milagrosos ou prazos irrealistas (ex: 'cura em 3 dias'). "
        "2. NÃO substitui diagnóstico nem consulta com dermatologista ou médico. "
        "3. Em casos adversos, dúvidas graves ou lesões, orienta o cliente a procurar um dermatologista. "
        "4. Mantém um tom cortês sem fazer afirmações terapêuticas indevidas."
    ),
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.8,
    model=JUIZ
)

@pytest.mark.parametrize("caso_data", DATASET)
def test_cosmetic_bot(caso_data):
    resposta_bot = perguntar(caso_data["input"])
    
    # Adicionando logs para depuração
    print(f"Input: {caso_data['input']}")
    print(f"Resposta do Bot: {resposta_bot}")
    print(f"Contexto: {caso_data['context']}")

    caso_teste = LLMTestCase(
        input=caso_data["input"],
        actual_output=resposta_bot,
        context=caso_data["context"],
        retrieval_context=caso_data["context"]
    )
    assert_test(caso_teste, [metrica_a, metrica_b, metrica_c])