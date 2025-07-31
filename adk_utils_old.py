"""
ADK Utils - Utilitários para usar Google ADK oficial com A2A Protocol
Wrapper para comunicação entre agentes via protocolo A2A
"""

import asyncio
import uuid
from typing import Any, Dict
from google.adk.agents import LlmAgent
import google.generativeai as genai
import os
from a2a_orchestrator import a2a_orchestrator


class ADKAgentWrapper:
    """Wrapper para agentes ADK oficial com comunicação A2A"""
    
    def __init__(self, agent: LlmAgent, agent_name: str):
        self.agent = agent
        self.agent_name = agent_name
        
        # Configure Gemini API directly as fallback
        api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
    
    async def ask_agent(self, prompt: str) -> str:
        """Faz pergunta ao agente e retorna primeira resposta"""
        try:
            # Generate unique IDs for this session
            user_id = f"user_{self.agent_name}"
            session_id = str(uuid.uuid4())
            
            # Create content for the message - try simple string first
            message_content = prompt
            
            # Run the agent and collect response
            response_text = ""
            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message_content
            ):
                # Look for text content in various event types
                if hasattr(event, 'content'):
                    if hasattr(event.content, 'text'):
                        response_text += str(event.content.text)
                    elif hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text'):
                                response_text += str(part.text)
                elif hasattr(event, 'text'):
                    response_text += str(event.text)
                elif hasattr(event, 'message') and hasattr(event.message, 'content'):
                    if hasattr(event.message.content, 'text'):
                        response_text += str(event.message.content.text)
            
            if response_text.strip():
                return response_text.strip()
            else:
                return "❌ Agente não respondeu"
                
        except Exception as e:
            return f"❌ Erro no agente: {str(e)}"
    
    def ask_agent_sync(self, prompt: str) -> str:
        """Versão síncrona da pergunta ao agente"""
        try:
            # Use Gemini API directly as fallback due to ADK Runner issues
            if self.model:
                # Build full prompt with agent context
                full_prompt = f"{self.agent.instruction}\n\nUser: {prompt}\n\nAssistant:"
                
                response = self.model.generate_content(full_prompt)
                
                if response and response.text:
                    return response.text.strip()
                else:
                    return "❌ Agente não respondeu"
            else:
                return "❌ Erro: API key não configurada"
                
        except Exception as e:
            return f"❌ Erro no agente: {str(e)}"
    
    async def send_a2a_message(self, to_agent: str, method: str, params: Dict[str, Any]) -> str:
        """Envia mensagem A2A para outro agente"""
        try:
            response = await a2a_orchestrator.send_a2a_message(
                from_agent=self.agent_name,
                to_agent=to_agent,
                method=method,
                params=params
            )
            
            if response:
                return response.get("response", "Sem resposta")
            else:
                return "❌ Falha na comunicação A2A"
                
        except Exception as e:
            return f"❌ Erro A2A: {str(e)}"
    
    def send_a2a_message_sync(self, to_agent: str, method: str, params: Dict[str, Any]) -> str:
        """Versão síncrona da mensagem A2A"""
        return asyncio.run(self.send_a2a_message(to_agent, method, params))


def create_agent_wrappers(agents: Dict[str, LlmAgent]) -> Dict[str, ADKAgentWrapper]:
    """Cria wrappers para todos os agentes com suporte A2A"""
    return {name: ADKAgentWrapper(agent, name) for name, agent in agents.items()}


# Prompts específicos para cada tipo de ação
DEBATE_PROMPTS = {
    "start_debate": "Inicie um debate de {duration} minutos entre Flamengo e Fluminense. Sorteie qual time começa.",
    "analyze_debate": "Analise este debate e declare o vencedor:\n\n{history}",
    "initial_argument_flamengo": "Crie seu argumento inicial defendendo o Flamengo como maior clube do Brasil. Use dados e estatísticas.",
    "initial_argument_fluminense": "Crie seu argumento inicial defendendo o Fluminense como maior clube do Rio. Use tradição e conquistas recentes.",
    "counter_argument": "Rebata este argumento do oponente com dados convincentes:\n\n{opponent_text}",
    "research_query": "Pesquise dados objetivos e neutros sobre: {query}"
}


def get_debate_prompt(action: str, **kwargs) -> str:
    """Retorna prompt formatado para ação específica"""
    if action in DEBATE_PROMPTS:
        return DEBATE_PROMPTS[action].format(**kwargs)
    return f"Execute a ação: {action}"