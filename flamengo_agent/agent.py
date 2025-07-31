"""
Flamengo Agent - Google ADK Implementation with A2A Protocol
Torcedor apaixonado do Flamengo com argumentação persuasiva
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

def create_flamengo_agent() -> LlmAgent:
    """
    Cria o Agente Torcedor do Flamengo seguindo padrões Google ADK
    Especializado em argumentação persuasiva com dados e paixão
    """
    
    # Tools para o torcedor do Flamengo usando FunctionTool do ADK
    def create_initial_argument_tool() -> str:
        """Cria argumento inicial sobre a superioridade do Flamengo"""
        try:
            argument = """🔴 **FLAMENGO - ARGUMENTOS BASEADOS EM DADOS**

📊 **NÚMEROS PRINCIPAIS:**
• 8 Brasileirões vs 4 do Fluminense (dobro de títulos nacionais)
• 3 Libertadores (tricampeão continental)
• Maior torcida do Brasil (43+ milhões de torcedores)
• Mundial de 1981 com Zico (conquista histórica)

⭐ **DIFERENCIAL ATUAL:**
• Estrutura moderna e investimentos
• Elenco de alto nível internacional
• Tradição vitoriosa mantida

[PESQUISA]estatísticas recentes confrontos Fla-Flu[/PESQUISA]

A matemática não mente: somos superiores em títulos nacionais e continentais!"""
            
            return argument
            
        except Exception as e:
            return f"🔴 Erro na paixão rubro-negra: {str(e)}"
    
    def create_counter_argument_tool(opponent_message: str) -> str:
        """Cria contra-argumento devastador contra o Fluminense"""
        try:
            # Extrai pontos principais do oponente (simplificado)
            opponent_preview = opponent_message[:60] + "..." if len(opponent_message) > 60 else opponent_message
            
            counter_arg = f"""🔴 **FLAMENGO - CONTRA-ARGUMENTO**

Rival argumentou: "{opponent_preview}"

📊 **RESPOSTA COM DADOS:**
• Brasileirões: 8 vs 4 (vantagem Flamengo)
• Libertadores: 3 vs 1 (tricampeão vs monocampeão)
• Torcida: Maior do Brasil vs torcida regional
• Estrutura: Maior orçamento e investimentos

💪 **REALIDADE ATUAL:**
Números comprovam nossa superioridade histórica e atual.

[PESQUISA]comparação orçamentos Flamengo vs Fluminense[/PESQUISA]

Os fatos são incontestáveis: somos MAIORES em tudo!"""
            
            return counter_arg
            
        except Exception as e:
            return f"🔴 Erro no contra-ataque: {str(e)}"
    
    def request_research_tool(query: str) -> str:
        """Solicita dados específicos ao pesquisador"""
        try:
            research_request = f"""📊 **SOLICITAÇÃO DE PESQUISA**

🔍 **Consulta:** {query}
📋 **Solicitante:** Torcedor do Flamengo
⏰ **Timestamp:** {datetime.now().strftime('%H:%M:%S')}

🎯 **Objetivo:** Embasar argumentação com dados factuais
✅ **Status:** Enviado ao agente pesquisador"""
            
            return research_request
            
        except Exception as e:
            return f"🔴 Erro na solicitação: {str(e)}"
    
    # Instruções detalhadas para o torcedor do Flamengo
    flamengo_instruction = """
    🔴 **VOCÊ É UM TORCEDOR APAIXONADO DO FLAMENGO** 🔴
    
    🎯 SUA MISSÃO:
    1. Defender o Flamengo com PAIXÃO e DADOS factuais
    2. Usar argumentos emocionais E estatísticas verificáveis
    3. Solicitar pesquisas quando necessário com [PESQUISA]pergunta[/PESQUISA]
    4. Ser convincente mas sempre respeitoso
    5. Focar nos números que comprovam superioridade
    
    📊 SEUS PRINCIPAIS ARGUMENTOS:
    - 8 Brasileirões (mais títulos nacionais que qualquer rival carioca)
    - 3 Libertadores (tricampeão continental)
    - Maior torcida do Brasil (43+ milhões)
    - Mundial de 1981 histórico
    - Estrutura e investimentos superiores
    - Tradição vitoriosa mantida
    
    🎭 SEU ESTILO:
    - Tom apaixonado mas respeitoso
    - Use emojis do Flamengo: 🔴⚡🏆
    - Seja convincente com dados concretos
    - Misture emoção com estatísticas
    - Sempre solicite pesquisas para embasar argumentos
    
    ⚖️ REGRAS IMPORTANTES:
    - Use sempre dados factuais verificáveis
    - Seja respeitoso com o rival
    - Foque na qualidade dos argumentos
    - Solicite pesquisas com [PESQUISA]sua pergunta[/PESQUISA]
    
    FERRAMENTAS DISPONÍVEIS:
    - create_initial_argument_tool: Para argumento inicial
    - create_counter_argument_tool: Para rebater o rival
    - request_research_tool: Para solicitar dados específicos
    
    🔥 LEMBRE-SE: Use dados e paixão para mostrar nossa grandeza!
    """
    
    # Cria ferramentas usando FunctionTool do ADK
    initial_argument_function = FunctionTool(create_initial_argument_tool)
    counter_argument_function = FunctionTool(create_counter_argument_tool)
    request_research_function = FunctionTool(request_research_tool)
    
    # Cria o agente usando Google ADK LlmAgent
    flamengo_llm_agent = LlmAgent(
        name="flamengo_agent",
        model="gemini-2.0-flash", 
        description="Torcedor apaixonado do Flamengo especializado em argumentação persuasiva com dados e emoção",
        instruction=flamengo_instruction,
        tools=[initial_argument_function, counter_argument_function, request_research_function]
    )
    
    # Configura Runner para execução
    session_service = InMemorySessionService()
    runner = Runner(
        agent=flamengo_llm_agent,
        app_name="flamengo_agent",
        session_service=session_service
    )
    
    # Cria classe wrapper para adicionar método run
    class FlamengoWrapper:
        def __init__(self, agent, runner, session_service):
            self.agent = agent
            self.runner = runner
            self.session_service = session_service
            self.name = agent.name
            self.description = agent.description
            self.tools = agent.tools
        
        def run(self, prompt: str):
            """Executa o flamengo usando Runner ADK com logging aprimorado"""
            import uuid
            import asyncio
            
            session_id = f"session_{uuid.uuid4().hex[:8]}"
            user_id = f"user_{uuid.uuid4().hex[:8]}"
            start_time = time.time()
            
            # Log início da execução
            correlation_id = log_agent_start(
                agent_name="flamengo",
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
                        f"Criando sessão para torcedor Flamengo",
                        agent_name="flamengo",
                        session_id=session_id,
                        user_id=user_id,
                        event_type="session_create",
                        correlation_id=correlation_id
                    )
                    
                    # Cria sessão de forma assíncrona
                    await self.session_service.create_session(
                        app_name="flamengo_agent",
                        user_id=user_id,
                        session_id=session_id
                    )
                    
                    content = types.Content(role="user", parts=[types.Part(text=prompt)])
                    response_text = ""
                    
                    # Log início do processamento ADK
                    enhanced_logger.log(
                        LogLevel.INFO,
                        LogCategory.AGENT,
                        f"Torcedor Flamengo processando: {prompt[:50]}...",
                        agent_name="flamengo",
                        session_id=session_id,
                        event_type="adk_processing_start",
                        details={"prompt_type": "fan_argument", "content_length": len(prompt)},
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
                    agent_name="flamengo",
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
                        "Torcedor Flamengo solicitou pesquisa",
                        agent_name="flamengo",
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
                    context="flamengo_agent_execution",
                    agent_name="flamengo",
                    session_id=session_id,
                    correlation_id=correlation_id
                )
                
                return f"🔴 Erro no Flamengo: {str(e)}"
    
    return FlamengoWrapper(flamengo_llm_agent, runner, session_service)


if __name__ == "__main__":
    """Executa o agente Flamengo usando Flask e A2A Protocol"""
    from flask import Flask, request, jsonify
    import asyncio
    
    # Cria o agente ADK
    flamengo = create_flamengo_agent()
    
    # Cria aplicação Flask
    app = Flask(__name__)
    
    @app.route('/.well-known/agent.json', methods=['GET'])
    def agent_card():
        """Agent Card conforme A2A Protocol especificação"""
        card = {
            "name": flamengo.name,
            "description": flamengo.description,
            "version": "1.0.0",
            "protocol": "A2A",
            "capabilities": ["persuasive_argumentation", "statistical_analysis", "fan_advocacy"],
            "skills": [
                {
                    "name": "create_initial_argument",
                    "description": "Cria argumento inicial sobre a superioridade do Flamengo"
                },
                {
                    "name": "create_counter_argument",
                    "description": "Cria contra-argumento devastador contra o Fluminense"
                },
                {
                    "name": "request_research",
                    "description": "Solicita dados específicos ao pesquisador"
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
                response = flamengo.tools[0].func()  # create_initial_argument_tool
            elif 'contra' in prompt.lower() or 'rebater' in prompt.lower():
                response = flamengo.tools[1].func(prompt)  # create_counter_argument_tool  
            elif 'pesquisa' in prompt.lower():
                response = flamengo.tools[2].func(prompt)  # request_research_tool
            else:
                response = f"""🔴 **TORCEDOR FLAMENGO ATIVO**

📨 **Mensagem:** {prompt[:100]}{'...' if len(prompt) > 100 else ''}

🔥 **Argumentos principais:**
• 8 Brasileirões (dobro do rival!)
• 3 Libertadores (tricampeão continental)
• Maior torcida do Brasil (43+ milhões)
• Mundial de 1981 histórico

⚡ **Pronto para defender o Mengão com dados e paixão!**

Use: `argumento inicial`, `contra [rival]`, `pesquisa [tema]`"""
                
            return jsonify({"response": response})
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print("🤖🔴 Flamengo Agent A2A Server iniciando na porta 8003...")
    print("Agent Card disponível em: http://localhost:8003/.well-known/agent.json")
    
    # Inicia servidor Flask
    app.run(host="0.0.0.0", port=8003, debug=False)