"""
Sistema Central A2A - Agent-to-Agent Communication
Coordena comunicação entre os 4 agentes seguindo protocolo A2A v1.0
"""

import asyncio
import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import uuid4

# Importa todos os agentes
from supervisor_agent import SupervisorAgent
from flamengo_agent import FlamengoAgent
from fluminense_agent import FluminenseAgent
from researcher_agent import ResearcherAgent


class A2AProtocolSystem:
    """
    Sistema central de comunicação A2A seguindo especificação oficial
    Gerencia comunicação entre agentes usando JSON-RPC 2.0
    """
    
    def __init__(self):
        self.system_id = "a2a_debate_system"
        self.version = "1.0.0"
        self.protocol_version = "A2A-v1.0"
        
        # Inicializa agentes
        self.agents = {
            "supervisor": SupervisorAgent(),
            "flamengo": FlamengoAgent(),
            "fluminense": FluminenseAgent(),
            "researcher": ResearcherAgent()
        }
        
        # Estado do sistema
        self.active = True
        self.debate_active = False
        self.current_turn = None
        self.turn_sequence = ["flamengo", "fluminense"]
        self.turn_index = 0
        
        # Log de comunicações A2A
        self.message_log = []
        self.agent_cards = {}
        
        # Inicializa agent cards
        self._initialize_agent_cards()
    
    def _initialize_agent_cards(self):
        """
        Inicializa Agent Cards de todos os agentes
        """
        for agent_name, agent in self.agents.items():
            self.agent_cards[agent_name] = agent.get_agent_card()
    
    async def send_a2a_message(self, from_agent: str, to_agent: str, method: str, params: Dict = None) -> Dict[str, Any]:
        """
        Envia mensagem A2A entre agentes seguindo JSON-RPC 2.0
        """
        if from_agent not in self.agents or to_agent not in self.agents:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32001,
                    "message": "Agent not found",
                    "data": f"From: {from_agent}, To: {to_agent}"
                }
            }
        
        # Cria mensagem JSON-RPC 2.0
        message = {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": method,
            "params": params or {},
            "from_agent": from_agent,
            "to_agent": to_agent,
            "timestamp": datetime.now().isoformat(),
            "protocol": self.protocol_version
        }
        
        # Log da comunicação
        self.message_log.append({
            **message,
            "system_timestamp": time.time(),
            "status": "sent"
        })
        
        try:
            # Processa mensagem no agente destinatário
            target_agent = self.agents[to_agent]
            response = await target_agent.process_a2a_message(message)
            
            # Log da resposta
            self.message_log.append({
                "jsonrpc": "2.0",
                "id": message["id"],
                "from_agent": to_agent,
                "to_agent": from_agent,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "system_timestamp": time.time(),
                "status": "response"
            })
            
            return response
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": message["id"],
                "error": {
                    "code": -32603,
                    "message": "Internal error in target agent",
                    "data": str(e)
                }
            }
            
            self.message_log.append({
                **error_response,
                "system_timestamp": time.time(),
                "status": "error"
            })
            
            return error_response
    
    async def broadcast_message(self, from_agent: str, method: str, params: Dict = None, exclude_agents: List[str] = None) -> Dict[str, Any]:
        """
        Envia mensagem para todos os agentes (broadcast A2A)
        """
        exclude_agents = exclude_agents or []
        responses = {}
        
        for agent_name in self.agents.keys():
            if agent_name != from_agent and agent_name not in exclude_agents:
                response = await self.send_a2a_message(from_agent, agent_name, method, params)
                responses[agent_name] = response
        
        return {
            "broadcast_id": str(uuid4()),
            "from_agent": from_agent,
            "method": method,
            "responses": responses,
            "timestamp": datetime.now().isoformat()
        }
    
    async def start_debate(self, duration_minutes: int) -> Dict[str, Any]:
        """
        Inicia debate coordenado via A2A
        """
        try:
            self.debate_active = True
            self.current_turn = "flamengo"  # Flamengo sempre inicia
            
            # 1. Supervisor inicia debate (chamada direta ao invés de A2A)
            supervisor_agent = self.agents["supervisor"]
            supervisor_response = await supervisor_agent.process_a2a_message({
                "jsonrpc": "2.0",
                "id": "start_debate_direct",
                "method": "start_debate",
                "params": {"duration_minutes": duration_minutes},
                "from_agent": "a2a_system",
                "to_agent": "supervisor"
            })
            
            if supervisor_response.get("error"):
                return {
                    "status": "error",
                    "message": "Erro ao iniciar supervisão",
                    "details": supervisor_response["error"]
                }
            
            # 2. Notifica todos os agentes sobre início
            broadcast_result = await self.broadcast_message(
                "supervisor", "debate_started",
                {
                    "duration_minutes": duration_minutes,
                    "first_speaker": "flamengo",
                    "turn_sequence": self.turn_sequence
                },
                exclude_agents=["supervisor"]
            )
            
            # 3. Notifica especificamente quem inicia
            await self.send_a2a_message(
                "supervisor", "flamengo", "turn_notification",
                {
                    "your_turn": True,
                    "time_allocated": (duration_minutes * 60) / 2,
                    "action_required": "initial_argument"
                }
            )
            
            await self.send_a2a_message(
                "supervisor", "fluminense", "turn_notification",
                {
                    "your_turn": False,
                    "time_allocated": (duration_minutes * 60) / 2,
                    "status": "waiting"
                }
            )
            
            return {
                "status": "success",
                "message": "Debate iniciado via protocolo A2A",
                "supervisor_response": supervisor_response.get("result", {}),
                "broadcast_responses": broadcast_result["responses"],
                "current_turn": self.current_turn,
                "protocol": self.protocol_version
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro no sistema A2A: {str(e)}"
            }
    
    async def process_turn(self, current_agent: str, opponent_message: str = None) -> Dict[str, Any]:
        """
        Processa turno de um agente
        """
        try:
            if current_agent not in self.agents:
                return {
                    "status": "error",
                    "message": f"Agente {current_agent} não encontrado"
                }
            
            agent = self.agents[current_agent]
            
            # 1. Verifica se agente precisa de pesquisa
            research_needed = opponent_message and "PESQUISADOR:" in opponent_message.upper()
            research_data = None
            
            if research_needed:
                # Extrai query de pesquisa
                query_start = opponent_message.upper().find("PESQUISADOR:") + 12
                query = opponent_message[query_start:].strip()
                if query:
                    # Solicita pesquisa
                    research_response = await self.send_a2a_message(
                        current_agent, "researcher", "research_request",
                        {
                            "query": query,
                            "requester": current_agent,
                            "context": "debate"
                        }
                    )
                    
                    if research_response.get("result", {}).get("status") == "research_completed":
                        research_data = research_response["result"].get("data", "")
            
            # 2. Notifica agente sobre seu turno
            turn_response = await self.send_a2a_message(
                "supervisor", current_agent, "turn_notification",
                {
                    "your_turn": True,
                    "opponent_argument": opponent_message,
                    "research_data": research_data,
                    "action_required": "counter_argument" if opponent_message else "initial_argument"
                }
            )
            
            # 3. Alterna turno
            self.turn_index = (self.turn_index + 1) % len(self.turn_sequence)
            next_agent = self.turn_sequence[self.turn_index]
            self.current_turn = next_agent
            
            return {
                "status": "success",
                "current_agent": current_agent,
                "next_agent": next_agent,
                "turn_response": turn_response.get("result", {}),
                "research_used": research_data is not None,
                "protocol": self.protocol_version
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro no processamento do turno: {str(e)}"
            }
    
    async def finish_debate(self, debate_history: List[Dict]) -> Dict[str, Any]:
        """
        Finaliza debate e solicita análise final
        """
        try:
            self.debate_active = False
            self.current_turn = None
            
            # 1. Solicita análise final ao supervisor (chamada direta)
            supervisor_agent = self.agents["supervisor"]
            analysis_response = await supervisor_agent.process_a2a_message({
                "jsonrpc": "2.0",
                "id": "analyze_debate_direct", 
                "method": "analyze_debate",
                "params": {"debate_history": debate_history},
                "from_agent": "a2a_system",
                "to_agent": "supervisor"
            })
            
            # 2. Notifica todos sobre fim do debate
            broadcast_result = await self.broadcast_message(
                "supervisor", "debate_finished",
                {
                    "analysis_available": True,
                    "winner_announced": True
                },
                exclude_agents=["supervisor"]
            )
            
            return {
                "status": "success",
                "message": "Debate finalizado via protocolo A2A",
                "analysis": analysis_response.get("result", {}),
                "broadcast_responses": broadcast_result["responses"],
                "protocol": self.protocol_version
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro na finalização: {str(e)}"
            }
    
    def get_agent_discovery(self) -> Dict[str, Any]:
        """
        Retorna informações de descoberta de agentes (Agent Discovery)
        """
        return {
            "system_id": self.system_id,
            "version": self.version,
            "protocol": self.protocol_version,
            "agents": {
                agent_name: {
                    "agent_card": card,
                    "status": "active" if self.agents[agent_name].active else "inactive",
                    "endpoint": card.get("url", f"http://localhost:800{i}/{agent_name}")
                }
                for i, (agent_name, card) in enumerate(self.agent_cards.items())
            },
            "capabilities": {
                "multi_agent_debate": True,
                "real_time_research": True,
                "rhetorical_analysis": True,
                "a2a_protocol": self.protocol_version
            },
            "communication_patterns": [
                "request_response",
                "broadcast",
                "turn_based",
                "research_request"
            ]
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Retorna status completo do sistema A2A
        """
        return {
            "system": {
                "id": self.system_id,
                "active": self.active,
                "protocol": self.protocol_version,
                "version": self.version
            },
            "debate": {
                "active": self.debate_active,
                "current_turn": self.current_turn,
                "turn_sequence": self.turn_sequence,
                "turn_index": self.turn_index
            },
            "agents": {
                agent_name: agent.get_status()
                for agent_name, agent in self.agents.items()
            },
            "a2a_communications": {
                "total_messages": len(self.message_log),
                "messages_by_type": self._count_messages_by_type(),
                "active_conversations": self._count_active_conversations()
            },
            "health": {
                "all_agents_connected": all(agent.api_key for agent in self.agents.values()),
                "protocol_compliance": "A2A-v1.0",
                "last_activity": max([msg["system_timestamp"] for msg in self.message_log]) if self.message_log else 0
            }
        }
    
    def _count_messages_by_type(self) -> Dict[str, int]:
        """
        Conta mensagens por tipo/método
        """
        counts = {}
        for msg in self.message_log:
            method = msg.get("method", "unknown")
            counts[method] = counts.get(method, 0) + 1
        return counts
    
    def _count_active_conversations(self) -> int:
        """
        Conta conversas ativas
        """
        recent_threshold = time.time() - 300  # 5 minutos
        recent_messages = [msg for msg in self.message_log if msg.get("system_timestamp", 0) > recent_threshold]
        
        conversations = set()
        for msg in recent_messages:
            from_agent = msg.get("from_agent")
            to_agent = msg.get("to_agent")
            if from_agent and to_agent:
                conversations.add(tuple(sorted([from_agent, to_agent])))
        
        return len(conversations)
    
    async def shutdown(self):
        """
        Encerra sistema A2A de forma segura
        """
        try:
            # Notifica todos os agentes sobre encerramento
            await self.broadcast_message(
                "system", "shutdown",
                {"reason": "system_shutdown", "timestamp": datetime.now().isoformat()}
            )
            
            self.active = False
            self.debate_active = False
            
            return {
                "status": "success",
                "message": "Sistema A2A encerrado com segurança",
                "final_message_count": len(self.message_log)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro no encerramento: {str(e)}"
            }


# Instância global do sistema A2A
a2a_system = A2AProtocolSystem()


# Funções de conveniência para acesso
def get_a2a_system() -> A2AProtocolSystem:
    """Retorna instância do sistema A2A"""
    return a2a_system

def get_agent(agent_name: str):
    """Retorna agente específico"""
    return a2a_system.agents.get(agent_name)

def get_system_status() -> Dict[str, Any]:
    """Retorna status do sistema"""
    return a2a_system.get_system_status()

def get_agent_discovery() -> Dict[str, Any]:
    """Retorna informações de descoberta"""
    return a2a_system.get_agent_discovery()