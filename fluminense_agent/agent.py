"""
Fluminense Agent - Google ADK Implementation with A2A Protocol
Torcedor orgulhoso do Fluminense com argumentação elegante e tradicional
"""

import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv

# Sistema de log aprimorado
from utils.enhanced_logger import (
    enhanced_logger, log_agent_start, log_agent_response, 
    log_tool_execution, log_error, LogLevel, LogCategory
)

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
    fluminense_llm_agent = LlmAgent(
        name="fluminense_agent",
        model="gemini-2.0-flash",
        description="Torcedor orgulhoso do Fluminense especializado em argumentação elegante com tradição e classe",
        instruction=fluminense_instruction,
        tools=[initial_argument_function, counter_argument_function, request_research_function]
    )
    
    # Configura Runner para execução
    session_service = InMemorySessionService()
    runner = Runner(
        agent=fluminense_llm_agent,
        app_name="fluminense_agent",
        session_service=session_service
    )
    
    # Cria classe wrapper para adicionar método run
    class FluminenseWrapper:
        def __init__(self, agent, runner, session_service):
            self.agent = agent
            self.runner = runner
            self.session_service = session_service
            self.name = agent.name
            self.description = agent.description
            self.tools = agent.tools
        
        def run(self, prompt: str):
            """Executa o fluminense usando Runner ADK com logging aprimorado"""
            import uuid
            import asyncio
            
            session_id = f"session_{uuid.uuid4().hex[:8]}"
            user_id = f"user_{uuid.uuid4().hex[:8]}"
            start_time = time.time()
            
            # Log início da execução
            correlation_id = log_agent_start(
                agent_name="fluminense",
                session_id=session_id,
                user_id=user_id,
                prompt=prompt
            )
            
            try:
                async def run_with_session():
                    # Log criação de sessão
                    enhanced_logger.log(
                        LogLevel.INFO,
                        LogCategory.SESSION,
                        f"Criando sessão para torcedor Fluminense",
                        agent_name="fluminense",
                        session_id=session_id,
                        user_id=user_id,
                        event_type="session_create",
                        correlation_id=correlation_id
                    )
                    
                    # Cria sessão de forma assíncrona
                    await self.session_service.create_session(
                        app_name="fluminense_agent",
                        user_id=user_id,
                        session_id=session_id
                    )
                    
                    content = types.Content(role="user", parts=[types.Part(text=prompt)])
                    response_text = ""
                    
                    # Log início do processamento ADK
                    enhanced_logger.log(
                        LogLevel.INFO,
                        LogCategory.AGENT,
                        f"Torcedor Fluminense processando com classe: {prompt[:50]}...",
                        agent_name="fluminense",
                        session_id=session_id,
                        event_type="adk_processing_start",
                        details={"prompt_type": "elegant_argument", "content_length": len(prompt)},
                        correlation_id=correlation_id
                    )
                    
                    async for event in self.runner.run_async(
                        user_id=user_id,
                        session_id=session_id,
                        new_message=content
                    ):
                        if event.is_final_response():
                            response_text = event.content.parts[0].text
                            break
                            
                    return response_text or "Sem resposta do agente"
                
                # Executa de forma assíncrona
                response = asyncio.run(run_with_session())
                
                # Calcula duração e log de sucesso
                duration_ms = (time.time() - start_time) * 1000
                log_agent_response(
                    agent_name="fluminense",
                    session_id=session_id,
                    response=response,
                    duration_ms=duration_ms,
                    correlation_id=correlation_id
                )
                
                # Log para pesquisa se houver tags [PESQUISA]
                if "[PESQUISA]" in response.upper():
                    enhanced_logger.log(
                        LogLevel.INFO,
                        LogCategory.AGENT,
                        "Torcedor Fluminense solicitou pesquisa com elegância",
                        agent_name="fluminense",
                        session_id=session_id,
                        event_type="research_request",
                        details={"research_detected": True},
                        correlation_id=correlation_id
                    )
                
                return response
                
            except Exception as e:
                # Log detalhado do erro
                duration_ms = (time.time() - start_time) * 1000
                log_error(
                    error=e,
                    context="fluminense_agent_execution",
                    agent_name="fluminense",
                    session_id=session_id,
                    correlation_id=correlation_id
                )
                
                return f"🟢 Erro no Fluminense: {str(e)}"
    
    return FluminenseWrapper(fluminense_llm_agent, runner, session_service)


if __name__ == "__main__":
    """Executa o agente Fluminense usando Flask e A2A Protocol"""
    from flask import Flask, request, jsonify
    import asyncio
    
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
            
            # Implementação simplificada usando as tools diretamente
            if 'argumento inicial' in prompt.lower() or 'inicial' in prompt.lower():
                response = fluminense.tools[0].func()  # create_initial_argument_tool
            elif 'contra' in prompt.lower() or 'rebater' in prompt.lower():
                response = fluminense.tools[1].func(prompt)  # create_counter_argument_tool  
            elif 'pesquisa' in prompt.lower():
                response = fluminense.tools[2].func(prompt)  # request_research_tool
            else:
                response = f"""🟢 **TORCEDOR FLUMINENSE ATIVO**

📨 **Mensagem:** {prompt[:100]}{'...' if len(prompt) > 100 else ''}

✨ **Argumentos principais:**
• Atual campeão da Libertadores (2023)
• Clube mais antigo do Rio (1902)
• 4 Brasileirões com qualidade técnica
• Tradição centenaria em revelar craques

🏆 **Somos CLASSE! Somos TRADIÇÃO! Somos ATUAIS CAMPEÕES!**

Use: `argumento inicial`, `contra [rival]`, `pesquisa [tema]`"""
                
            return jsonify({"response": response})
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print("🤖🟢 Fluminense Agent A2A Server iniciando na porta 8004...")
    print("Agent Card disponível em: http://localhost:8004/.well-known/agent.json")
    
    # Inicia servidor Flask
    app.run(host="0.0.0.0", port=8004, debug=False)