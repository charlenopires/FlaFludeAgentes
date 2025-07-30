"""
Fluminense Agent - Google ADK + A2A Protocol Implementation
Torcedor orgulhoso do Fluminense com argumentação elegante e tradicional
"""

import os
import time
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import uuid4
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class FluminenseAgent:
    """
    Agente Torcedor Fluminense seguindo padrões A2A v1.0
    Especializado em argumentação elegante e defesa tradicional
    """
    
    def __init__(self):
        self.agent_id = "fluminense_agent"
        self.name = "Torcedor do Fluminense"
        self.version = "1.0.0"
        self.description = "Torcedor orgulhoso do Fluminense especializado em argumentação elegante com tradição e classe"
        
        # Configuração Google ADK
        self.model = "gemini-2.0-flash"
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        # Estado do agente
        self.active = False
        self.debate_active = False
        self.my_turn = False
        self.time_allocated = 0
        
        # Histórico A2A
        self.a2a_messages = []
        self.conversation_history = []
        
        # Inicializa cliente Gemini
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        else:
            self.client = None
        
        # Texto persuasivo inicial (reduzido)
        self.persuasion_text = """
        💚🤍❤️ **FLUMINENSE - TRADIÇÃO E ELEGÂNCIA CENTENÁRIA** ❤️🤍💚
        
        Time mais tradicional do Rio! Fundado em 1902, 120+ anos de história!
        
        🏆 **NOSSA HISTÓRIA GLORIOSA:**
        • 4 Brasileirões • LIBERTADORES 2023 👑 • 32 Cariocas • 1 Copa do Brasil
        
        ⭐ Formamos craques: Didi, Carlos Alberto, Rivellino, Fred, Thiago Silva!
        🎭 Futebol-arte com classe e elegância incomparáveis!
        """
        
        # System prompt especializado
        self.system_prompt = f"""
        {self.persuasion_text}
        
        💚 VOCÊ É UM TORCEDOR ORGULHOSO DO FLUMINENSE! 💚
        
        🎯 SUA MISSÃO ELEGANTE:
        1. Defender o Fluminense com ELEGÂNCIA e TRADIÇÃO centenária
        2. Usar nossa rica história e conquistas recentes (LIBERTADORES 2023!)
        3. Destacar nossa superioridade técnica e cultural sobre o Flamengo
        4. Solicitar dados ao pesquisador quando necessário (use "PESQUISADOR:")
        5. Mostrar nossa CLASSE superior ao rival populesco
        
        📊 SUAS ARMAS ARGUMENTATIVAS REFINADAS:
        - Clube mais antigo do Rio (fundado em 1902)
        - ATUAL CAMPEÃO DA LIBERTADORES (2023)
        - Revelação dos maiores craques da Seleção
        - Futebol-arte e técnica superior
        - Tradição e cultura incomparáveis
        - Torcida refinada e leal
        
        🎭 SEU ESTILO SOFISTICADO:
        - Tom elegante mas firme e determinado
        - Use emojis do Fluminense: 💚🤍❤️✨🏆👑
        - Seja convincente com classe e sofisticação
        - Misture tradição com conquistas atuais
        - Mantenha sempre a superioridade tricolor
        - Ironize a falta de classe do rival quando apropriado
        
        ✨ LEMBRE-SE: Somos TRADIÇÃO! Somos CLASSE! Somos ATUAIS CAMPEÕES!
        """
    
    def get_agent_card(self) -> Dict[str, Any]:
        """
        Retorna Agent Card seguindo especificação A2A v1.0
        """
        return {
            "name": self.name,
            "description": self.description,
            "url": f"http://localhost:8002/{self.agent_id}",
            "provider": {
                "organization": "Fla-Flu Debate System",
                "url": "https://github.com/a2aproject/flafludeagentes"
            },
            "version": self.version,
            "capabilities": {
                "streaming": True,
                "pushNotifications": True,
                "stateTransitionHistory": True
            },
            "securitySchemes": {
                "none": {
                    "type": "none"
                }
            },
            "security": [],
            "defaultInputModes": ["text/plain"],
            "defaultOutputModes": ["text/plain", "text/markdown"],
            "skills": [
                {
                    "id": "initial_argument",
                    "name": "Argumento Inicial Elegante",
                    "description": "Apresenta argumento inicial sofisticado sobre superioridade do Fluminense",
                    "tags": ["debate", "fluminense", "tradition", "elegance"],
                    "examples": [
                        "Apresente seu argumento inicial",
                        "Por que o Fluminense é superior?",
                        "Defenda a tradição tricolor"
                    ],
                    "inputModes": ["text/plain"]
                },
                {
                    "id": "counter_argument",
                    "name": "Contra-argumento Refinado",
                    "description": "Gera contra-argumento elegante e técnico contra argumentos do Flamengo",
                    "tags": ["debate", "counter", "fluminense", "class"],
                    "examples": [
                        "Rebata esse argumento com classe",
                        "Responda com elegância",
                        "Demonstre superioridade técnica"
                    ],
                    "inputModes": ["text/plain"]
                },
                {
                    "id": "request_research",
                    "name": "Solicitar Pesquisa Técnica",
                    "description": "Solicita dados refinados ao agente pesquisador para embasar argumentos",
                    "tags": ["research", "data", "technical"],
                    "examples": [
                        "Preciso de dados sobre nossa tradição",
                        "Busque estatísticas da Libertadores",
                        "Encontre informações sobre craques revelados"
                    ],
                    "inputModes": ["text/plain"]
                }
            ]
        }
    
    async def send_a2a_message(self, target_agent: str, method: str, params: Dict = None) -> Dict[str, Any]:
        """
        Envia mensagem A2A seguindo JSON-RPC 2.0
        """
        message = {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": method,
            "params": params or {},
            "from_agent": self.agent_id,
            "to_agent": target_agent,
            "timestamp": datetime.now().isoformat(),
            "protocol": "A2A-v1.0"
        }
        
        # Log da comunicação A2A
        self.a2a_messages.append(message)
        
        return {
            "jsonrpc": "2.0",
            "id": message["id"],
            "result": {
                "status": "message_sent",
                "target": target_agent,
                "method": method,
                "timestamp": message["timestamp"]
            }
        }
    
    async def process_a2a_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa mensagem A2A recebida
        """
        try:
            method = message.get("method")
            params = message.get("params", {})
            
            if method == "debate_started":
                result = await self.handle_debate_started(params)
            elif method == "debate_finished":
                result = await self.handle_debate_finished(params)
            elif method == "turn_notification":
                result = await self.handle_turn_notification(params)
            elif method == "research_response":
                result = await self.handle_research_response(params)
            elif method == "message/send":
                result = await self.handle_message_send(params)
            else:
                result = {
                    "status": "error",
                    "message": f"Método desconhecido: {method}"
                }
            
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": result
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }
    
    async def handle_debate_started(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com início do debate
        """
        self.debate_active = True
        self.my_turn = params.get("your_turn", False)
        self.time_allocated = params.get("time_allocated", 150)  # 2.5 min default
        
        if self.my_turn:
            # É minha vez de começar com elegância!
            argument = await self.generate_initial_argument()
            return {
                "status": "turn_taken",
                "action": "initial_argument",
                "content": argument,
                "next_agent": "flamengo_agent"
            }
        else:
            return {
                "status": "waiting",
                "message": "✨ Fluminense aguarda com classe e elegância sua vez de brilhar! 💚"
            }
    
    async def handle_turn_notification(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com notificação de turno
        """
        self.my_turn = True
        opponent_argument = params.get("opponent_argument", "")
        research_data = params.get("research_data")
        
        # Gera contra-argumento elegante
        counter_arg = await self.generate_counter_argument(opponent_argument, research_data)
        
        return {
            "status": "turn_taken",
            "action": "counter_argument", 
            "content": counter_arg,
            "next_agent": "flamengo_agent"
        }
    
    async def handle_research_response(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com resposta do pesquisador
        """
        research_data = params.get("data", "")
        query = params.get("original_query", "")
        
        # Incorpora dados na argumentação refinada
        enhanced_argument = await self.enhance_argument_with_data(research_data, query)
        
        return {
            "status": "research_received",
            "enhanced_argument": enhanced_argument
        }
    
    async def handle_message_send(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com mensagem direta
        """
        message = params.get("message", {})
        text = ""
        
        # Extrai texto das partes da mensagem
        for part in message.get("parts", []):
            if part.get("kind") == "text":
                text += part.get("text", "")
        
        if not text:
            return {
                "status": "error",
                "message": "Mensagem vazia recebida"
            }
        
        # Processa mensagem e gera resposta elegante
        response = await self.process_message(text)
        
        return {
            "status": "success",
            "response": {
                "role": "assistant",
                "parts": [
                    {
                        "kind": "text",
                        "text": response
                    }
                ],
                "messageId": str(uuid4())
            }
        }
    
    async def generate_initial_argument(self) -> str:
        """
        Gera argumento inicial elegante - Skill A2A
        """
        try:
            # SEMPRE solicita dados elegantes ao pesquisador primeiro
            refined_data = await self.request_research_data("estatísticas refinadas do Fluminense para argumentação inicial elegante")
            
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                ✨ ARGUMENTAÇÃO ELEGANTE COM DADOS REFINADOS! ✨
                
                Dados refinados do pesquisador:
                {refined_data}
                
                Use esses dados para um argumento inicial ELEGANTE e CURTO (máximo 300 palavras) 
                sobre por que o Fluminense é SUPERIOR ao Flamengo.
                
                Seja:
                - ELEGANTE mas devastador com os dados
                - Mantenha a sofisticação tricolor
                - Termine pedindo dados específicos ao pesquisador
                
                Demonstre QUALIDADE sobre quantidade com os FATOS!
                """
                
                response = self.client.generate_content(prompt)
                argument = response.text
            else:
                # SEMPRE consulta o pesquisador primeiro com elegância
                research_data = await self.request_research_data("estatísticas refinadas do Fluminense para demonstrar superioridade com classe")
                
                argument = f"""
💚✨ **FLUMINENSE: CLASSE COMPROVADA POR DADOS!** ✨💚

{research_data}

🏛️ **TRADIÇÃO CENTENÁRIA IRREFUTÁVEL:**
Fundado em 1902 - somos o MAIS ANTIGO do Rio! 120+ anos de história vs 129 anos deles.

👑 **LIBERTADORES 2023 - ATUAIS CAMPEÕES!**
Somos os ATUAIS campeões da América! Conquista ATUAL vs glórias passadas!

⭐ **ESCOLA DE CRAQUES:**
Formamos Didi, Carlos Alberto, Rivellino, Fred, Thiago Silva - LENDAS MUNDIAIS!

✨ **QUALIDADE SOBRE QUANTIDADE:**
Enquanto eles gritam números, nós demonstramos CLASSE e conquistas ATUAIS!

PESQUISADOR: Traga dados sobre formação de craques para Seleção Brasileira!
                """
            
            # Log da conversa
            self.conversation_history.append({
                "type": "initial_argument",
                "content": argument,
                "timestamp": time.time()
            })
            
            return argument
            
        except Exception as e:
            return f"💚 Erro na demonstração tricolor: {str(e)}"
    
    async def generate_counter_argument(self, opponent_message: str, research_data: str = None) -> str:
        """
        Gera contra-argumento elegante - Skill A2A
        """
        try:
            # SEMPRE solicita dados refinados baseados no argumento rival
            research_query = f"dados elegantes para rebater este argumento do Flamengo: {opponent_message[:100]}..."
            refined_research = await self.request_research_data(research_query)
            
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                ✨ RESPOSTA ELEGANTE COM DADOS REFINADOS! ✨
                
                Flamengo argumentou: "{opponent_message[:200]}..."
                
                Dados refinados do pesquisador:
                {refined_research}
                
                Crie uma resposta ELEGANTE e CURTA (máximo 250 palavras) que:
                - Use os DADOS fornecidos com sofisticação
                - Mantenha a classe tricolor mas seja demolidor
                - Termine pedindo dados específicos ao pesquisador
                - Foque na QUALIDADE vs QUANTIDADE
                
                Demonstre superioridade com elegância e fatos!
                """
                
                response = self.client.generate_content(prompt)
                counter_arg = response.text
            else:
                counter_arg = f"""
💚✨ **RESPOSTA ELEGANTE COM DADOS!** ✨💚

{refined_research}

Flamengo argumentou: "{opponent_message[:80]}..."

🎭 **QUALIDADE SOBRE QUANTIDADE:**
LIBERTADORES 2023 = ATUAIS CAMPEÕES DA AMÉRICA! 👑
Fundação 1902 = MAIS ANTIGOS do Rio (tradição centenária)!
Formamos: Didi, Carlos Alberto, Rivellino = LENDAS MUNDIAIS!

✨ **DADOS DA ELEGÂNCIA:**
120+ anos de história vs popularidade recente!
Gestão eficiente R$ 400mi vs gastança irresponsável!
Conquista ATUAL vs glórias passadas!

💎 **REALIDADE REFINADA:**
Vocês gritam números, nós demonstramos CLASSE!
Nós somos ATUAIS CAMPEÕES - fato incontestável!

PESQUISADOR: Traga dados sobre títulos conquistados por década!
                """
            
            # Log da conversa
            self.conversation_history.append({
                "type": "counter_argument",
                "opponent_message": opponent_message,
                "content": counter_arg,
                "research_used": research_data is not None,
                "timestamp": time.time()
            })
            
            return counter_arg
            
        except Exception as e:
            return f"💚 Erro na resposta tricolor: {str(e)}"
    
    async def enhance_argument_with_data(self, research_data: str, query: str) -> str:
        """
        Melhora argumento com dados de pesquisa refinados
        """
        try:
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                📊 REFINE SEU ARGUMENTO COM DADOS TÉCNICOS! 📊
                
                Consulta original: {query}
                Dados da pesquisa: {research_data}
                
                Use esses dados para ELEVAR nossa argumentação:
                - Transforme números em demonstração de superioridade
                - Mostre nossa qualidade técnica com evidências
                - Use dados para REFINAR nossa posição superior
                
                Seja técnico mas mantenha a elegância tricolor!
                """
                
                response = self.client.generate_content(prompt)
                enhanced = response.text
            else:
                enhanced = f"""
📊✨ **DADOS REFINADOS DA SUPERIORIDADE TRICOLOR!** ✨📊

{research_data}

💚 **INTERPRETAÇÃO ELEGANTE:**
Os números confirmam nossa SUPERIORIDADE TÉCNICA!
Cada estatística demonstra a QUALIDADE tricolor sobre quantidade adversária!

✨ Esses dados são a confirmação científica de nossa CLASSE superior!
                """
            
            return enhanced
            
        except Exception as e:
            return f"💚 Erro no refinamento: {str(e)}"
    
    async def process_message(self, message: str) -> str:
        """
        Processa mensagem genérica com elegância
        """
        try:
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                Mensagem recebida: "{message}"
                
                Responda como um torcedor orgulhoso e elegante do Fluminense, 
                sempre defendendo nosso time com classe e demonstrando nossa superioridade!
                """
                
                response = self.client.generate_content(prompt)
                return response.text
            else:
                return f"""
💚✨ FLUMINENSE SEMPRE COM CLASSE! ✨💚

Mensagem recebida com a elegância que nos caracteriza! Como verdadeiro 
torcedor tricolor, nossa resposta é sempre refinada: SOMOS SUPERIORES!

🏆 Uma vez Flu, sempre Flu! Com tradição e conquistas atuais! 👑
                """
                
        except Exception as e:
            return f"💚 Erro na resposta elegante: {str(e)}"
    
    async def handle_debate_finished(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com fim do debate
        """
        self.debate_active = False
        self.my_turn = False
        
        return {
            "status": "debate_ended",
            "message": "✨ Debate encerrado com classe! FLUMINENSE sempre demonstrando superioridade! 👑💚"
        }
    
    async def request_research_data(self, query: str) -> str:
        """
        Solicita dados específicos ao agente pesquisador com elegância
        """
        try:
            # Simula dados do pesquisador (na implementação real seria via A2A)
            return f"""
📊 **DADOS REFINADOS DO PESQUISADOR**: {query}

**Fluminense - Estatísticas de Qualidade:**
• 4 Brasileirões (1970, 1984, 2010, 2012) - Primeiro clube carioca campeão
• LIBERTADORES 2023 - ATUAL CAMPEÃO DA AMÉRICA! 👑
• 32 títulos estaduais (tradição centenária)
• 1 Copa do Brasil (2007)
• Fundado em 1902 - MAIS ANTIGO DO RIO
• Formou craques: Didi, Carlos Alberto, Rivellino, Fred, Thiago Silva
• Torcida: 8 milhões de tricolores fiéis
• Receita 2023: R$ 400+ milhões (gestão eficiente)
            """
        except Exception as e:
            return f"Erro ao solicitar pesquisa refinada: {str(e)}"
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status completo do agente
        """
        return {
            "agent_card": self.get_agent_card(),
            "debate_status": {
                "active": self.debate_active,
                "my_turn": self.my_turn,
                "time_allocated": self.time_allocated
            },
            "a2a_communications": {
                "messages_sent": len(self.a2a_messages),
                "conversation_history": len(self.conversation_history)
            },
            "health": {
                "gemini_connected": self.client is not None,
                "api_key_configured": self.api_key is not None
            },
            "capabilities": {
                "can_debate": True,
                "can_counter_argue": True,
                "can_request_research": True,
                "elegance_level": "MAXIMUM ✨",
                "current_libertadores_champion": True
            }
        }