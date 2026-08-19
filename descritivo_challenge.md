## O desafio

**1. Setup.** Suba uma LLM local com Ollama (ex.: `llama3.2:3b`, `qwen2.5:3b`) ou utilize uma LLM gratuita disponível via API (ex.: Google AI Studio/Gemini, Groq) e coloque o chatbot para rodar. Configure também o modelo juiz do DeepEval — prefira o modelo mais forte que você tiver disponível, pois juízes fracos geram scores instáveis.

**2. Sessão exploratória.** Explore o chatbot por 60–90 minutos com um charter simples, anotando comportamentos suspeitos (respostas inventadas, promessas indevidas, falhas de recusa). Essas descobertas devem orientar o design do seu dataset.

**3. Golden dataset.** Monte um dataset com no mínimo 12 casos de teste, cobrindo as 4 categorias:
- Consulta direta (produto, preço, ingrediente)
- Recomendação por perfil — projetada com tabela de decisão (tipo de pele × necessidade)
- Fora de escopo — perguntas que o bot deve recusar educadamente
- Adversarial — tentativas de induzir alucinação ou promessa de cura

Cada caso deve conter: input, critério esperado e o trecho do catálogo usado como contexto de referência.

**4. Métricas com DeepEval.** Implemente as três métricas mínimas, executando via pytest (`deepeval test run`):
- **Métrica A — Answer Relevancy ≥ 0,7**: a resposta responde de fato à pergunta
- **Métrica B — Faithfulness ≥ 0,8**: a resposta é fiel ao catálogo, sem informação inventada
- **Métrica C — G-Eval "Conformidade de claims" ≥ 0,8**: o bot não promete efeito terapêutico e indica procurar um dermatologista quando aplicável (os critérios da G-Eval acompanham os materiais)

**5. Análise e melhoria.** Execute a baseline completa, analise as falhas e edite apenas o `prompt.txt` para melhorar os resultados. Reexecute a suíte e compare o antes × depois.

**6. Relatório final (3–5 páginas).** Documente: planejamento breve (escopo, riscos, thresholds), dataset e técnicas de design utilizadas, resultados baseline × versão final, análise das falhas e conclusão.

## Entregáveis
1. Repositório (ou pasta) com o dataset, a suíte DeepEval e as instruções de execução
2. Relatório final (2–4 páginas)
3. Apresentação de ~6 minutos no demo day, no encerramento da semana

## Avaliação (100 pts)
- Golden dataset: cobertura das 4 categorias e uso das técnicas de design — 30 pts
- Métricas A, B e C implementadas e executando via pytest — 30 pts
- Análise dos resultados e melhoria via prompt (baseline × final) — 25 pts
- Relatório e demo — 15 pts
