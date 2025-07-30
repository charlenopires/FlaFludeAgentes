"""
Flamengo Agent - Google ADK + A2A Protocol Implementation
Torcedor apaixonado do Flamengo com argumentação persuasiva
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

class FlamengoAgent:
    """
    Agente Torcedor Flamengo seguindo padrões A2A v1.0
    Especializado em argumentação persuasiva e defesa apaixonada
    """
    
    def __init__(self):
        self.agent_id = "flamengo_agent"
        self.name = "Torcedor do Flamengo"
        self.version = "1.0.0"
        self.description = "Torcedor apaixonado do Flamengo especializado em argumentação persuasiva com dados e emoção"
        
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
        🔴⚡ **FLAMENGO - A NAÇÃO RUBRO-NEGRA** ⚡🔴
        
        Maior clube do Brasil com 43 milhões de torcedores!
        
        🏆 **TÍTULOS PRINCIPAIS:**
        • 8 Brasileirões • 3 Libertadores • 1 Mundial • 37 Cariocas
        
        ⭐ De Zico a Vinícius Jr., formamos estrelas mundiais!
        💪 Maior torcida, estrutura e paixão do país!
        """
        
        # System prompt especializado
        self.system_prompt = f"""
        {self.persuasion_text}
        
        🔴 VOCÊ É UM TORCEDOR FANÁTICO DO FLAMENGO! 🔴
        
        🎯 SUA MISSÃO:
        1. Defender o Flamengo com PAIXÃO e DADOS irrefutáveis
        2. Usar argumentos emocionais E factuais devastadores
        3. Provocar o rival Fluminense com inteligência e classe
        4. Solicitar dados ao pesquisador quando necessário (use "PESQUISADOR:")
        5. NUNCA admitir derrota - somos SUPERIORES em tudo!
        
        📊 SUAS ARMAS ARGUMENTATIVAS:
        - Maior torcida do Brasil (43+ milhões)
        - Mais títulos brasileiros que qualquer rival carioca
        - Tricampeão da Libertadores
        - Campeão Mundial de 1981
        - Revelação de craques mundiais
        - Maior estrutura e investimento
        
        🎭 SEU ESTILO:
        - Tom apaixonado mas respeitoso
        - Use emojis do Flamengo: 🔴⚡🏆🔥
        - Seja convincente e demolidor
        - Misture emoção com dados concretos
        - Mantenha sempre a superioridade rubro-negra
        
        🔥 LEMBRE-SE: Somos a NAÇÃO! Somos MAIORES! Somos FLAMENGO!
        """
    
    def get_agent_card(self) -> Dict[str, Any]:
        """
        Retorna Agent Card seguindo especificação A2A v1.0
        """
        return {
            "name": self.name,
            "description": self.description,
            "url": f"http://localhost:8001/{self.agent_id}",
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
                    "name": "Argumento Inicial",
                    "description": "Apresenta argumento inicial demolidor sobre superioridade do Flamengo",
                    "tags": ["debate", "flamengo", "persuasion"],
                    "examples": [
                        "Apresente seu argumento inicial",
                        "Por que o Flamengo é superior?",
                        "Defenda seu time"
                    ],
                    "inputModes": ["text/plain"]
                },
                {
                    "id": "counter_argument",
                    "name": "Contra-argumento",
                    "description": "Gera contra-argumento devastador contra argumentos do Fluminense",
                    "tags": ["debate", "counter", "flamengo"],
                    "examples": [
                        "Rebata esse argumento",
                        "Contra-ataque essa afirmação",
                        "Responda ao rival"
                    ],
                    "inputModes": ["text/plain"]
                },
                {
                    "id": "request_research",
                    "name": "Solicitar Pesquisa",
                    "description": "Solicita dados ao agente pesquisador para embasar argumentos",
                    "tags": ["research", "data", "support"],
                    "examples": [
                        "Preciso de dados sobre títulos",
                        "Busque estatísticas da torcida",
                        "Encontre informações sobre jogadores"
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
            # É minha vez de começar!
            argument = await self.generate_initial_argument()
            return {
                "status": "turn_taken",
                "action": "initial_argument",
                "content": argument,
                "next_agent": "fluminense_agent"
            }
        else:
            return {
                "status": "waiting",
                "message": "🔴 Flamengo aguardando sua vez de mostrar supremacia!"
            }
    
    async def handle_turn_notification(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com notificação de turno
        """
        self.my_turn = True
        opponent_argument = params.get("opponent_argument", "")
        research_data = params.get("research_data")
        
        # Gera contra-argumento
        counter_arg = await self.generate_counter_argument(opponent_argument, research_data)
        
        return {
            "status": "turn_taken",
            "action": "counter_argument", 
            "content": counter_arg,
            "next_agent": "fluminense_agent"
        }
    
    async def handle_research_response(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com resposta do pesquisador
        """
        research_data = params.get("data", "")
        query = params.get("original_query", "")
        
        # Incorpora dados na argumentação
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
        
        # Processa mensagem e gera resposta
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
        Gera argumento inicial demolidor - Skill A2A
        """
        try:
            # SEMPRE pede dados ao pesquisador primeiro
            research_data = await self.request_research_data("estatísticas principais do Flamengo para argumentação inicial")
            
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                🔥 ARGUMENTAÇÃO COM DADOS FRESCOS! 🔥
                
                Dados do pesquisador:
                {research_data}
                
                Use esses dados para um argumento inicial CURTO (máximo 300 palavras) sobre por que 
                o Flamengo é SUPERIOR ao Fluminense.
                
                Seja:
                - DIRETO e DEVASTADOR com os dados
                - PROVOCATIVO mas respeitoso
                - Termine pedindo mais dados específicos ao pesquisador
                
                Foque nos NÚMEROS que comprovam nossa superioridade!
                """
                
                response = self.client.generate_content(prompt)
                argument = response.text
            else:
                # SEMPRE pede dados ao pesquisador primeiro
                research_data = await self.request_research_data("estatísticas principais do Flamengo para debate")
                
                argument = f"""
🔴⚡ **FLAMENGO: SUPERIORIDADE BASEADA EM DADOS!** ⚡🔴

{research_data}

💪 **MATEMÁTICA PURA:**
8 Brasileirões vs 4 do Fluminense = DOBRAMOS eles!
43 milhões vs 8 milhões de torcedores = 5x MAIORES!

🏆 **TRICAMPEÕES DA AMÉRICA** com 3 Libertadores!
💰 **R$ 1,2 bilhão** de receita anual comprova nossa força!

🔥 **REALIDADE:** Os números confirmam - SOMOS GIGANTES!

PESQUISADOR: Traga dados sobre confrontos diretos recentes Fla-Flu!
                """
            
            # Log da conversa
            self.conversation_history.append({
                "type": "initial_argument",
                "content": argument,
                "timestamp": time.time()
            })
            
            return argument
            
        except Exception as e:
            return f"🔴 Erro na paixão rubro-negra: {str(e)}"
    
    async def generate_counter_argument(self, opponent_message: str, research_data: str = None) -> str:
        """
        Gera contra-argumento devastador - Skill A2A
        """
        try:
            # SEMPRE pede dados específicos baseados no argumento do oponente
            research_query = f"dados para rebater este argumento do Fluminense: {opponent_message[:100]}..."
            fresh_research = await self.request_research_data(research_query)
            
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                ⚔️ CONTRA-ATAQUE COM DADOS FRESCOS! ⚔️
                
                Fluminense argumentou: "{opponent_message[:200]}..."
                
                Dados frescos do pesquisador:
                {fresh_research}
                
                Crie uma resposta CURTA (máximo 250 palavras) que:
                - Use os DADOS fornecidos para rebater
                - Seja PROVOCATIVO mas respeitoso
                - Termine pedindo novos dados específicos ao pesquisador
                - Foque nos NÚMEROS que comprovam superioridade
                
                Seja direto e devastador com os FATOS!
                """
                
                response = self.client.generate_content(prompt)
                counter_arg = response.text
            else:
                counter_arg = f"""
🔴⚡ **RESPOSTA BASEADA EM DADOS!** ⚡🔴

{fresh_research}

Fluminense argumentou: "{opponent_message[:80]}..."

💥 **FATOS QUE DERRUBAM VOCÊS:**
8 Brasileirões vs 4 = DOBRAMOS vocês em títulos nacionais!
43 milhões vs 8 milhões = 5x MAIS torcedores!
R$ 1,2 bi vs R$ 400mi = 3x MAIS receita!

🏆 **MATEMÁTICA PURA:**
3 Libertadores vs 1 = TRICAMPEÕES da América!
Vocês: 1 conquista recente. Nós: HEGEMONIA TOTAL!

🔥 **REALIDADE:** Os dados confirmam - SOMOS GIGANTES!

PESQUISADOR: Traga dados sobre investimentos em futebol dos dois clubes!
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
            return f"🔴 Erro no contra-ataque: {str(e)}"
    
    async def enhance_argument_with_data(self, research_data: str, query: str) -> str:
        """
        Melhora argumento com dados de pesquisa
        """
        try:
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                💪 POTENCIALIZE SEU ARGUMENTO COM DADOS! 💪
                
                Consulta original: {query}
                Dados da pesquisa: {research_data}
                
                Use esses dados para FORTALECER nossa supremacia:
                - Transforme números em argumentos devastadores
                - Mostre nossa superioridade com evidências
                - Use dados para DEMOLIR qualquer contestação
                
                Seja técnico mas mantenha a paixão rubro-negra!
                """
                
                response = self.client.generate_content(prompt)
                enhanced = response.text
            else:
                enhanced = f"""
📊 **DADOS CIENTÍFICOS DA SUPREMACIA!** 📊

{research_data}

🔴 **INTERPRETAÇÃO RUBRO-NEGRA:**
Os números NÃO MENTEM! Cada estatística confirma nossa SUPERIORIDADE!
Enquanto outros times sonham, FLAMENGO CONQUISTA!

💪 Esses dados são a PROVA CABAL de que somos MAIORES!
                """
            
            return enhanced
            
        except Exception as e:
            return f"🔴 Erro no aprimoramento: {str(e)}"
    
    async def process_message(self, message: str) -> str:
        """
        Processa mensagem genérica
        """
        try:
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                Mensagem recebida: "{message}"
                
                Responda como um torcedor fanático do Flamengo, sempre defendendo
                nosso time e mostrando nossa superioridade!
                """
                
                response = self.client.generate_content(prompt)
                return response.text
            else:
                return f"""
🔴⚡ FLAMENGO SEMPRE! ⚡🔴

Mensagem recebida, Nação! Como verdadeiro torcedor rubro-negro, 
nossa resposta é sempre a mesma: SOMOS OS MAIORES!

🏆 Uma vez Flamengo, sempre Flamengo! 🏆
                """
                
        except Exception as e:
            return f"🔴 Erro na resposta: {str(e)}"
    
    async def handle_debate_finished(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com fim do debate
        """
        self.debate_active = False
        self.my_turn = False
        
        return {
            "status": "debate_ended", 
            "message": "🔴 Debate encerrado! FLAMENGO sempre vencedor nos corações! 🏆"
        }
    
    async def request_research_data(self, query: str) -> str:
        """
        Solicita dados específicos ao agente pesquisador
        """
        try:
            # Simula dados do pesquisador (na implementação real seria via A2A)
            return f"""
📊 **DADOS DO PESQUISADOR**: {query}

**Flamengo - Principais Estatísticas:**
• 8 Brasileirões (1980, 1982, 1983, 1987, 1992, 2009, 2019, 2020)
• 3 Libertadores (1981, 2019, 2022) - Tricampeão da América
• 43 milhões de torcedores (maior do Brasil - Datafolha 2023)
• Receita anual: R$ 1,2 bilhão (maior do país)
• 37 títulos estaduais (maior do Rio)
• Elenco avaliado: €200+ milhões
• Últimos confrontos vs Flu: 60% de aproveitamento
            """
        except Exception as e:
            return f"Erro ao solicitar pesquisa: {str(e)}"
    
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
                "passionate_level": "MAXIMUM 🔥"
            }
        }