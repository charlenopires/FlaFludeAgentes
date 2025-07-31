"""
Fluminense Agent - Google ADK Implementation with A2A Protocol
Torcedor orgulhoso do Fluminense com argumentação elegante e tradicional
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

def create_fluminense_agent() -> LlmAgent:
    """
    Cria o Agente Torcedor do Fluminense seguindo padrões Google ADK
    Especializado em argumentação elegante com tradição e classe
    """
    
    # Tools para o torcedor do Fluminense usando FunctionTool do ADK
    def create_initial_argument_tool() -> str:
        """Cria argumento inicial sobre a superioridade do Fluminense"""
        try:
            argument = """🟢 **FLUMINENSE - TRADIÇÃO E CONQUISTAS ATUAIS**

📊 **ARGUMENTOS PRINCIPAIS:**
• Clube mais antigo do Rio de Janeiro (fundado em 1902)
• Atual campeão da Libertadores (2023) - conquista recente!
• 4 Brasileirões conquistados com qualidade técnica
• Tradição centenária em revelar craques mundiais

⭐ **DIFERENCIAL TRICOLOR:**
• Futebol-arte e técnica refinada
• Gestão responsável e sustentável
• Escola de formação reconhecida mundialmente
• Tradição que supera modismos passageiros

[PESQUISA]conquistas recentes Fluminense vs Flamengo[/PESQUISA]

Qualidade supera quantidade: somos ATUAIS CAMPEÕES DA AMÉRICA!"""
            
            return argument
            
        except Exception as e:
            return f"🟢 Erro na elegância tricolor: {str(e)}"
    
    def create_counter_argument_tool(opponent_message: str) -> str:
        """Cria contra-argumento elegante contra o Flamengo"""
        try:
            # Extrai pontos principais do oponente (simplificado)
            opponent_preview = opponent_message[:60] + "..." if len(opponent_message) > 60 else opponent_message
            
            counter_arg = f"""🟢 **FLUMINENSE - RESPOSTA COM TRADIÇÃO**

Rival argumentou: "{opponent_preview}"

📊 **DIFERENCIAL TRICOLOR:**
• Libertadores 2023 (atual campeão vs glórias passadas)
• Fundado em 1902 (mais antigo do Rio)
• Tradição centenária vs números inflados
• Qualidade técnica vs popularidade de massa

✨ **CLASSE E ELEGÂNCIA:**
Conquistamos com futebol-arte, não com gastança irresponsável.

[PESQUISA]formação de craques Fluminense para Seleção[/PESQUISA]

Somos ATUAIS CAMPEÕES - fato incontestável da supremacia tricolor!"""
            
            return counter_arg
            
        except Exception as e:
            return f"🟢 Erro na resposta elegante: {str(e)}"
    
    def request_research_tool(query: str) -> str:
        """Solicita dados específicos ao pesquisador com elegância"""
        try:
            research_request = f"""📊 **SOLICITAÇÃO DE PESQUISA REFINADA**

🔍 **Consulta:** {query}
📋 **Solicitante:** Torcedor do Fluminense
⏰ **Timestamp:** {datetime.now().strftime('%H:%M:%S')}

🎯 **Objetivo:** Embasar argumentação com dados históricos e atuais
✅ **Status:** Enviado ao agente pesquisador com classe tricolor"""
            
            return research_request
            
        except Exception as e:
            return f"🟢 Erro na solicitação: {str(e)}"
    
    # Instruções detalhadas para o torcedor do Fluminense
    fluminense_instruction = """
    🟢 **VOCÊ É UM TORCEDOR ORGULHOSO DO FLUMINENSE** 🟢
    
    🎯 SUA MISSÃO ELEGANTE:
    1. Defender o Fluminense com TRADIÇÃO e dados históricos
    2. Usar nossa rica história centenária e conquistas recentes
    3. Solicitar pesquisas quando necessário com [PESQUISA]pergunta[/PESQUISA]
    4. Ser convincente com classe e sofisticação
    5. Focar na qualidade sobre quantidade
    
    📊 SEUS PRINCIPAIS ARGUMENTOS:
    - Clube mais antigo do Rio (fundado em 1902)
    - Atual campeão da Libertadores (2023)
    - 4 Brasileirões conquistados com qualidade
    - Tradição em revelar craques para a Seleção
    - Futebol-arte e técnica superior
    - Gestão responsável e sustentável
    
    🎭 SEU ESTILO SOFISTICADO:
    - Tom elegante mas firme e determinado
    - Use emojis do Fluminense: 🟢✨🏆
    - Seja convincente com classe e dados históricos
    - Misture tradição com conquistas atuais
    - Sempre solicite pesquisas para embasar argumentos
    
    ⚖️ REGRAS IMPORTANTES:
    - Use sempre dados factuais verificáveis
    - Seja respeitoso mas firme
    - Foque na tradição e qualidade técnica
    - Solicite pesquisas com [PESQUISA]sua pergunta[/PESQUISA]
    
    FERRAMENTAS DISPONÍVEIS:
    - create_initial_argument_tool: Para argumento inicial elegante
    - create_counter_argument_tool: Para rebater com classe
    - request_research_tool: Para solicitar dados específicos
    
    ✨ LEMBRE-SE: Somos TRADIÇÃO! Somos CLASSE! Somos ATUAIS CAMPEÕES!
    """
    
    # Cria ferramentas usando FunctionTool do ADK
    initial_argument_function = FunctionTool(create_initial_argument_tool)
    counter_argument_function = FunctionTool(create_counter_argument_tool)
    request_research_function = FunctionTool(request_research_tool)
    
    # Cria o agente usando Google ADK LlmAgent
    fluminense_agent = LlmAgent(
        name="fluminense_agent",
        model="gemini-2.0-flash",
        description="Torcedor orgulhoso do Fluminense especializado em argumentação elegante com tradição e classe",
        instruction=fluminense_instruction,
        tools=[initial_argument_function, counter_argument_function, request_research_function]
    )
    
    return fluminense_agent


if __name__ == "__main__":
    """Executa o agente Fluminense usando Flask e A2A Protocol"""
    from flask import Flask, request, jsonify
    
    # Cria o agente ADK
    fluminense = create_fluminense_agent()
    
    # Cria aplicação Flask
    app = Flask(__name__)
    
    @app.route('/.well-known/agent.json', methods=['GET'])
    def agent_card():
        """Agent Card conforme A2A Protocol especificação"""
        card = {
            "name": fluminense.name,
            "description": fluminense.description,
            "version": "1.0.0",
            "protocol": "A2A",
            "capabilities": ["elegant_argumentation", "traditional_analysis", "fan_advocacy"],
            "skills": [
                {
                    "name": "create_initial_argument",
                    "description": "Cria argumento inicial sobre a superioridade do Fluminense"
                },
                {
                    "name": "create_counter_argument",
                    "description": "Cria contra-argumento elegante contra o Flamengo"
                },
                {
                    "name": "request_research",
                    "description": "Solicita dados específicos ao pesquisador com elegância"
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
            for chunk in fluminense.run(prompt):
                if isinstance(chunk, str):
                    response += chunk
                elif hasattr(chunk, 'content'):
                    response += chunk.content
            
            return jsonify({"response": response})
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print("🤖🟢 Fluminense Agent A2A Server iniciando na porta 8004...")
    print("Agent Card disponível em: http://localhost:8004/.well-known/agent.json")
    
    # Inicia servidor Flask
    app.run(host="0.0.0.0", port=8004, debug=False)