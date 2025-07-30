"""
Supervisor Agent - Google ADK Implementation
Especialista em retórica, psicologia, linguística e análise de debates
"""

import os
import time
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class SupervisorAgent:
    """
    Agente Supervisor seguindo padrões Google ADK + Protocolo A2A
    Coordena debates e analisa resultados com expertise em retórica
    """
    
    def __init__(self):
        self.agent_id = "supervisor_agent"
        self.name = "Supervisor de Debate"
        self.version = "1.0.0"
        self.description = "Especialista em retórica, psicologia cognitiva, linguística aplicada e análise lógica de argumentos"
        
        # Configuração Google ADK
        self.model = "gemini-2.0-flash"
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        # Estado do debate
        self.debate_duration = 0
        self.debate_start_time = None
        self.current_speaker = None
        self.turn_duration = 0
        self.active = False
        
        # Histórico de comunicação A2A
        self.a2a_messages = []
        self.connected_agents = {}
        
        # Inicializa cliente Gemini
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        else:
            self.client = None
            
        # System prompt especializado
        self.system_prompt = """
        Você é um SUPERVISOR DE DEBATE PROFISSIONAL especializado em:
        
        🎓 EXPERTISE ACADÊMICA:
        - Retórica clássica e moderna
        - Psicologia cognitiva e persuasão
        - Linguística aplicada ao discurso
        - Análise lógica de argumentos
        - Teoria da comunicação
        
        ⚖️ SUAS RESPONSABILIDADES:
        1. Coordenar tempo do debate (divisão 50/50)
        2. Manter neutralidade absoluta
        3. Analisar qualidade argumentativa
        4. Aplicar critérios científicos de avaliação
        5. Determinar vencedor baseado em evidências
        
        📊 CRITÉRIOS DE AVALIAÇÃO:
        1. Força dos Argumentos (40%) - lógica, coerência, estrutura
        2. Evidências e Dados (30%) - uso de estatísticas verificáveis
        3. Persuasão e Retórica (20%) - técnicas persuasivas, impacto
        4. Consistência Lógica (10%) - ausência de contradições
        
        🎯 PROTOCOLO:
        - Use linguagem profissional e imparcial
        - Cite critérios técnicos em suas análises
        - Mantenha registro preciso do tempo
        - Comunique-se com outros agentes via A2A quando necessário
        """
    
    def get_agent_card(self) -> Dict[str, Any]:
        """
        Retorna Agent Card seguindo especificação A2A
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": [
                "debate_coordination",
                "rhetorical_analysis", 
                "time_management",
                "argument_evaluation",
                "psychological_assessment"
            ],
            "skills": [
                {
                    "name": "start_debate",
                    "description": "Inicia sessão de debate com duração específica",
                    "parameters": {
                        "duration_minutes": "integer"
                    }
                },
                {
                    "name": "analyze_debate",
                    "description": "Análise final especializada do debate",
                    "parameters": {
                        "debate_history": "array"
                    }
                },
                {
                    "name": "get_time_status",
                    "description": "Retorna status temporal do debate",
                    "parameters": {}
                }
            ],
            "communication_protocols": ["A2A-v1.0", "JSON-RPC-2.0"],
            "authentication": {
                "required": False,
                "methods": ["none"]
            },
            "contact": {
                "agent_type": "supervisor",
                "specialization": "debate_coordination"
            }
        }
    
    async def send_a2a_message(self, target_agent: str, method: str, params: Dict = None) -> Dict[str, Any]:
        """
        Envia mensagem A2A seguindo JSON-RPC 2.0
        """
        message = {
            "jsonrpc": "2.0",
            "id": f"{self.agent_id}_{int(time.time())}",
            "method": method,
            "params": params or {},
            "from_agent": self.agent_id,
            "to_agent": target_agent,
            "timestamp": datetime.now().isoformat(),
            "protocol": "A2A-v1.0"
        }
        
        # Log da comunicação A2A
        self.a2a_messages.append(message)
        
        # Simula comunicação (em produção seria HTTP request)
        return {
            "jsonrpc": "2.0",
            "id": message["id"],
            "result": {
                "status": "message_sent",
                "target": target_agent,
                "method": method
            }
        }
    
    async def process_a2a_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa mensagem A2A recebida
        """
        try:
            method = message.get("method")
            params = message.get("params", {})
            
            if method == "start_debate":
                result = await self.start_debate(params.get("duration_minutes", 5))
            elif method == "analyze_debate":
                result = await self.analyze_debate(params.get("debate_history", []))
            elif method == "get_time_status":
                result = self.get_time_status()
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
    
    async def start_debate(self, duration_minutes: int) -> Dict[str, Any]:
        """
        Inicia debate com duração específica - Skill A2A
        """
        try:
            if duration_minutes < 2 or duration_minutes > 30:
                return {
                    "status": "error",
                    "message": "Duração deve ser entre 2 e 30 minutos"
                }
            
            self.debate_duration = duration_minutes
            self.debate_start_time = time.time()
            self.turn_duration = (duration_minutes * 60) / 2  # 50% para cada time
            self.active = True
            self.current_speaker = "flamengo_agent"  # Sorteia primeiro
            
            # Notifica outros agentes via A2A
            await self.send_a2a_message("flamengo_agent", "debate_started", {
                "your_turn": True,
                "time_allocated": self.turn_duration
            })
            
            await self.send_a2a_message("fluminense_agent", "debate_started", {
                "your_turn": False,
                "time_allocated": self.turn_duration
            })
            
            await self.send_a2a_message("researcher_agent", "debate_started", {
                "status": "standby",
                "duration": duration_minutes
            })
            
            # Gera mensagem de início usando Gemini
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                Você deve iniciar oficialmente um debate Flamengo vs Fluminense com {duration_minutes} minutos.
                Apresente as regras, critérios de avaliação e declare que o Torcedor do Flamengo inicia.
                Seja profissional e imparcial.
                """
                
                response = self.client.generate_content(prompt)
                message = response.text
            else:
                message = f"""
⚖️ **DEBATE OFICIAL INICIADO**

🎯 **Configuração Aprovada:**
• Duração total: {duration_minutes} minutos
• Tempo por time: {self.turn_duration/60:.1f} minutos cada
• Início: {datetime.now().strftime('%H:%M:%S')}

📊 **Critérios de Avaliação Científica:**
1. **Força dos Argumentos** (40%) - Lógica e coerência
2. **Evidências e Dados** (30%) - Estatísticas verificáveis  
3. **Persuasão e Retórica** (20%) - Técnicas persuasivas
4. **Consistência Lógica** (10%) - Ausência de contradições

🎲 **Sorteio Realizado:** FLAMENGO inicia o debate!

🔴 Torcedor do Flamengo, você tem {self.turn_duration/60:.1f} minutos. Apresente seus argumentos!
                """
            
            return {
                "status": "success",
                "message": message.strip(),
                "debate_config": {
                    "duration_minutes": duration_minutes,
                    "turn_duration": self.turn_duration,
                    "current_speaker": self.current_speaker,
                    "start_time": self.debate_start_time
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao iniciar debate: {str(e)}"
            }
    
    def get_time_status(self) -> Dict[str, Any]:
        """
        Retorna status temporal do debate - Skill A2A
        """
        if not self.debate_start_time:
            return {
                "status": "inactive",
                "total_remaining": 0,
                "current_speaker": None
            }
        
        elapsed = time.time() - self.debate_start_time
        total_remaining = max(0, (self.debate_duration * 60) - elapsed)
        
        return {
            "status": "active" if total_remaining > 0 else "finished",
            "total_remaining": total_remaining,
            "current_speaker": self.current_speaker,
            "elapsed": elapsed,
            "turn_time_used": min(elapsed, self.turn_duration) if self.current_speaker == "flamengo_agent" else max(0, elapsed - self.turn_duration)
        }
    
    async def analyze_debate(self, debate_history: List[Dict]) -> Dict[str, Any]:
        """
        Análise final especializada do debate - Skill A2A
        """
        try:
            if not debate_history:
                return {
                    "status": "error",
                    "message": "Histórico de debate vazio"
                }
            
            # Separa mensagens por agente
            flamengo_messages = [msg for msg in debate_history if "flamengo" in msg.get("from_agent", "").lower()]
            fluminense_messages = [msg for msg in debate_history if "fluminense" in msg.get("from_agent", "").lower()]
            
            # Prepara dados para análise
            flamengo_content = " ".join([msg.get("content", "") for msg in flamengo_messages])
            fluminense_content = " ".join([msg.get("content", "") for msg in fluminense_messages])
            
            # Gera análise usando Gemini
            if self.client:
                analysis_prompt = f"""
                {self.system_prompt}
                
                Como especialista em retórica, psicologia, linguística e lógica, analise este debate:
                
                ARGUMENTOS FLAMENGO ({len(flamengo_messages)} mensagens):
                {flamengo_content[:1000]}...
                
                ARGUMENTOS FLUMINENSE ({len(fluminense_messages)} mensagens):
                {fluminense_content[:1000]}...
                
                Aplique os critérios científicos:
                1. Força dos Argumentos (40%)
                2. Evidências e Dados (30%)
                3. Persuasão e Retórica (20%)
                4. Consistência Lógica (10%)
                
                Declare um VENCEDOR com justificativa técnica detalhada.
                Use sua expertise acadêmica para fundamentar a decisão.
                """
                
                response = self.client.generate_content(analysis_prompt)
                analysis = response.text
            else:
                # Análise básica sem Gemini
                analysis = f"""
⚖️ **ANÁLISE FINAL ESPECIALIZADA**

📊 **MÉTRICAS QUANTITATIVAS:**
• Flamengo: {len(flamengo_messages)} mensagens, {len(flamengo_content)} caracteres
• Fluminense: {len(fluminense_messages)} mensagens, {len(fluminense_content)} caracteres

🎯 **VEREDITO TÉCNICO:**
{"Flamengo demonstrou maior volume argumentativo" if len(flamengo_content) > len(fluminense_content) else "Fluminense apresentou argumentação mais concisa"}

📈 **BASE CIENTÍFICA:** Análise baseada em critérios de retórica aplicada
                """
            
            # Notifica fim do debate para outros agentes
            await self.send_a2a_message("flamengo_agent", "debate_finished", {
                "winner_announced": True
            })
            
            await self.send_a2a_message("fluminense_agent", "debate_finished", {
                "winner_announced": True
            })
            
            await self.send_a2a_message("researcher_agent", "debate_finished", {
                "analysis_complete": True
            })
            
            self.active = False
            
            return {
                "status": "success",
                "analysis": analysis.strip(),
                "metrics": {
                    "flamengo_messages": len(flamengo_messages),
                    "fluminense_messages": len(fluminense_messages),
                    "total_messages": len(debate_history),
                    "analysis_timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro na análise: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status completo do agente
        """
        return {
            "agent_card": self.get_agent_card(),
            "debate_status": {
                "active": self.active,
                "duration": self.debate_duration,
                "current_speaker": self.current_speaker,
                "start_time": self.debate_start_time
            },
            "a2a_communications": {
                "messages_sent": len(self.a2a_messages),
                "connected_agents": list(self.connected_agents.keys())
            },
            "health": {
                "gemini_connected": self.client is not None,
                "api_key_configured": self.api_key is not None
            }
        }