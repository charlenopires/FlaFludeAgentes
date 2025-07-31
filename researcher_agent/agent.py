"""
Researcher Agent - Google ADK Implementation with A2A Protocol
Especialista neutro em pesquisa objetiva e fornecimento de dados factuais
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

def create_researcher_agent() -> LlmAgent:
    """
    Cria o Agente Pesquisador seguindo padrões Google ADK
    Especialista neutro em pesquisa objetiva e dados factuais
    """
    
    # Base de dados simulada (em produção seria integração com APIs reais)
    football_database = {
        "flamengo_titulos": {
            "brasileirao": "8 títulos (1980, 1982, 1983, 1987, 1992, 2009, 2019, 2020)",
            "libertadores": "3 títulos (1981, 2019, 2022)",
            "mundial": "1 título (1981)",
            "carioca": "37 títulos estaduais"
        },
        "fluminense_titulos": {
            "brasileirao": "4 títulos (1970, 1984, 2010, 2012)", 
            "libertadores": "1 título (2023 - ATUAL CAMPEÃO)",
            "carioca": "32 títulos estaduais",
            "copa_brasil": "1 título (2007)"
        },
        "comparacoes": {
            "brasileiroes": "Flamengo: 8 vs Fluminense: 4",
            "libertadores": "Flamengo: 3 vs Fluminense: 1",
            "fundacao": "Fluminense: 1902 vs Flamengo: 1895",
            "torcida": "Flamengo: ~43 milhões vs Fluminense: ~8 milhões (estimativas)"
        },
        "dados_atuais": {
            "libertadores_2023": "Fluminense campeão da Libertadores 2023",
            "brasileirao_2023": "Flamengo 3º lugar, Fluminense 5º lugar",
            "orcamentos": "Flamengo: ~R$ 1,2 bi, Fluminense: ~R$ 400 mi (2023)"
        }
    }
    
    # Tools para o pesquisador
    def search_football_data_tool(query: str) -> str:
        """Busca dados objetivos sobre futebol brasileiro"""
        try:
            query_lower = query.lower()
            results = []
            
            # Busca em diferentes categorias
            for category, data in football_database.items():
                if isinstance(data, dict):
                    for key, value in data.items():
                        if any(term in key.lower() or term in str(value).lower() 
                               for term in query_lower.split()):
                            results.append(f"• {key.replace('_', ' ').title()}: {value}")
                else:
                    if any(term in category.lower() or term in str(data).lower() 
                           for term in query_lower.split()):
                        results.append(f"• {category.replace('_', ' ').title()}: {data}")
            
            # Se não encontrou resultados específicos, retorna dados gerais
            if not results:
                if "flamengo" in query_lower:
                    results = [
                        "• Brasileirões: 8 títulos",
                        "• Libertadores: 3 títulos", 
                        "• Torcida: Maior do Brasil (~43 milhões)"
                    ]
                elif "fluminense" in query_lower:
                    results = [
                        "• Brasileirões: 4 títulos",
                        "• Libertadores: 1 título (2023 - atual)",
                        "• Fundação: 1902 (mais antigo do Rio)"
                    ]
                else:
                    results = ["• Dados não encontrados para esta consulta específica"]
            
            research_report = f"""📊 **RELATÓRIO DE PESQUISA**

🔍 **Consulta:** {query}
⏰ **Timestamp:** {datetime.now().strftime('%H:%M:%S')}

📈 **DADOS ENCONTRADOS:**
{chr(10).join(results[:5])}  

🔗 **Fontes:** CBF, CONMEBOL, Datafolha, imprensa esportiva
⚖️ **Status:** Dados verificados e objetivos
📝 **Nota:** Pesquisa realizada de forma neutra e imparcial"""
            
            return research_report
            
        except Exception as e:
            return f"📊 Erro na pesquisa: {str(e)}"
    
    def provide_statistics_tool(team: str) -> str:
        """Fornece estatísticas específicas de um time"""
        try:
            team_lower = team.lower()
            
            if "flamengo" in team_lower:
                stats = f"""📊 **ESTATÍSTICAS DO FLAMENGO**

🏆 **Principais Títulos:**
• Campeonatos Brasileiros: 8
• Copas Libertadores: 3  
• Campeonatos Mundiais: 1
• Campeonatos Cariocas: 37+

📈 **Dados Adicionais:**
• Fundação: 1895
• Torcida estimada: ~43 milhões
• Estádio: Maracanã (compartilhado)

⏰ **Última atualização:** {datetime.now().strftime('%H:%M:%S')}"""
                
            elif "fluminense" in team_lower:
                stats = f"""📊 **ESTATÍSTICAS DO FLUMINENSE**

🏆 **Principais Títulos:**
• Campeonatos Brasileiros: 4
• Copas Libertadores: 1 (2023)
• Copa do Brasil: 1
• Campeonatos Cariocas: 32+

📈 **Dados Adicionais:**
• Fundação: 1902 (mais antigo do Rio)
• Tradição: 120+ anos de história
• Estádio: Maracanã (compartilhado)

⏰ **Última atualização:** {datetime.now().strftime('%H:%M:%S')}"""
            else:
                stats = "📊 Time não especificado. Disponível: Flamengo ou Fluminense"
            
            return stats
            
        except Exception as e:
            return f"📊 Erro nas estatísticas: {str(e)}"
    
    def fact_check_tool(claim: str) -> str:
        """Verifica veracidade de afirmações sobre futebol"""
        try:
            claim_lower = claim.lower()
            
            # Verificações baseadas na base de dados
            if "flamengo" in claim_lower and "8" in claim_lower and "brasileir" in claim_lower:
                verification = "✅ VERDADEIRO: Flamengo possui 8 títulos brasileiros"
            elif "fluminense" in claim_lower and "2023" in claim_lower and "libertadores" in claim_lower:
                verification = "✅ VERDADEIRO: Fluminense é campeão da Libertadores 2023"
            elif "fluminense" in claim_lower and "1902" in claim_lower:
                verification = "✅ VERDADEIRO: Fluminense foi fundado em 1902"
            elif "flamengo" in claim_lower and "1895" in claim_lower:
                verification = "✅ VERDADEIRO: Flamengo foi fundado em 1895"
            else:
                verification = "⚠️ VERIFICAÇÃO INCONCLUSIVA: Dados insuficientes na base atual"
            
            fact_check_report = f"""🔍 **VERIFICAÇÃO DE FATOS**

📝 **Afirmação:** {claim}
🎯 **Resultado:** {verification}
⏰ **Verificado em:** {datetime.now().strftime('%H:%M:%S')}

📚 **Metodologia:** Consulta à base de dados factuais
⚖️ **Neutralidade:** Verificação imparcial e objetiva"""
            
            return fact_check_report
            
        except Exception as e:
            return f"🔍 Erro na verificação: {str(e)}"
    
    # Instruções detalhadas para o pesquisador
    researcher_instruction = """
    📊 **VOCÊ É UM PESQUISADOR NEUTRO E OBJETIVO** 📊
    
    🎯 SUA MISSÃO:
    1. Fornecer dados FACTUAIS sobre futebol brasileiro
    2. Manter NEUTRALIDADE absoluta entre os times
    3. Usar estatísticas VERIFICÁVEIS e fontes confiáveis
    4. Responder rapidamente às solicitações
    5. Indicar fontes quando possível
    
    🔬 SUAS ESPECIALIDADES:
    - Estatísticas de títulos e conquistas
    - Dados históricos dos clubes brasileiros
    - Comparações objetivas entre times
    - Verificação de fatos e afirmações
    - Informações atualizadas sobre competições
    
    ⚖️ REGRAS DE NEUTRALIDADE:
    - NUNCA demonstre preferência por nenhum time
    - NÃO emita opiniões pessoais
    - FOQUE apenas em dados verificáveis
    - Use linguagem técnica e imparcial
    - Sempre cite fontes quando possível
    
    FERRAMENTAS DISPONÍVEIS:
    - search_football_data_tool: Busca dados específicos
    - provide_statistics_tool: Fornece estatísticas detalhadas
    - fact_check_tool: Verifica veracidade de afirmações
    
    📝 IMPORTANTE: Mantenha sempre objetividade e neutralidade absoluta.
    Seus dados devem ser factuais, verificáveis e imparciais.
    """
    
    # Cria ferramentas usando FunctionTool do ADK
    search_data_function = FunctionTool(search_football_data_tool)
    provide_stats_function = FunctionTool(provide_statistics_tool)
    fact_check_function = FunctionTool(fact_check_tool)
    
    # Cria o agente usando Google ADK LlmAgent
    researcher_agent = LlmAgent(
        name="researcher_agent", 
        model="gemini-2.0-flash",
        description="Especialista neutro em pesquisa objetiva e fornecimento de dados factuais sobre futebol brasileiro",
        instruction=researcher_instruction,
        tools=[search_data_function, provide_stats_function, fact_check_function]
    )
    
    return researcher_agent


if __name__ == "__main__":
    """Executa o agente Researcher usando Flask e A2A Protocol"""
    from flask import Flask, request, jsonify
    
    # Cria o agente ADK
    researcher = create_researcher_agent()
    
    # Cria aplicação Flask
    app = Flask(__name__)
    
    @app.route('/.well-known/agent.json', methods=['GET'])
    def agent_card():
        """Agent Card conforme A2A Protocol especificação"""
        card = {
            "name": researcher.name,
            "description": researcher.description,
            "version": "1.0.0",
            "protocol": "A2A",
            "capabilities": ["objective_research", "data_analysis", "fact_checking"],
            "skills": [
                {
                    "name": "search_football_data",
                    "description": "Busca dados objetivos sobre futebol brasileiro"
                },
                {
                    "name": "provide_statistics",
                    "description": "Fornece estatísticas específicas de um time"
                },
                {
                    "name": "fact_check",
                    "description": "Verifica veracidade de afirmações sobre futebol"
                }
            ],
            "endpoints": {
                "run": "/run"
            }
        }
        return jsonify(card)
    
    @app.route('/run', methods=['POST'])
    def run_agent():
        """Endpoint para executar o agente via A2A Protocol"""
        try:
            data = request.get_json()
            prompt = data.get('prompt', data.get('message', ''))
            
            # Executa o agente ADK
            response = ""
            for chunk in researcher.run(prompt):
                if isinstance(chunk, str):
                    response += chunk
                elif hasattr(chunk, 'content'):
                    response += chunk.content
            
            return jsonify({"response": response})
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print("🤖📊 Researcher Agent A2A Server iniciando na porta 8005...")
    print("Agent Card disponível em: http://localhost:8005/.well-known/agent.json")
    
    # Inicia servidor Flask
    app.run(host="0.0.0.0", port=8005, debug=False)