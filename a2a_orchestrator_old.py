"""
A2A Orchestrator - Sistema de orquestração para agentes A2A
Coordena descoberta de agentes e comunicação via protocolo A2A oficial
"""

import asyncio
import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from google.adk.agents import Agent
# A2AClient import removed - using HTTP-based communication instead

class A2AOrchestrator:
    """Orquestrador A2A para descoberta e comunicação entre agentes"""
    
    def __init__(self):
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.agent_urls: Dict[str, str] = {}
        self.message_log: List[Dict[str, Any]] = []
        
    def register_agent(self, name: str, url: str, port: int):
        """Registra um agente no orquestrador"""
        agent_url = f"{url}:{port}"
        self.agent_registry[name] = {
            "url": agent_url,
            "port": port,
            "card_url": f"{agent_url}/.well-known/agent.json",
            "status": "registered",
            "last_ping": None
        }
        
        # Armazena URL do agente para comunicação HTTP
        self.agent_urls[name] = agent_url
        
        print(f"✅ Agente {name} registrado em {agent_url}")
    
    def discover_agent(self, name: str) -> Optional[Dict[str, Any]]:
        """Descobre um agente e sua agent card"""
        if name not in self.agent_registry:
            return None
            
        agent_info = self.agent_registry[name]
        card_url = agent_info["card_url"]
        
        try:
            response = requests.get(card_url, timeout=5)
            if response.status_code == 200:
                agent_card = response.json()
                agent_info["card"] = agent_card
                agent_info["status"] = "discovered"
                agent_info["last_ping"] = datetime.now().isoformat()
                
                self.log_message("discovery", f"Descobriu agente {name}", {
                    "agent": name,
                    "card_url": card_url,
                    "capabilities": agent_card.get("capabilities", [])
                })
                
                return agent_card
            else:
                agent_info["status"] = "unreachable"
                return None
                
        except Exception as e:
            print(f"❌ Erro ao descobrir agente {name}: {str(e)}")
            agent_info["status"] = "error"
            return None
    
    async def send_a2a_message(self, from_agent: str, to_agent: str, method: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Envia mensagem A2A entre agentes via HTTP"""
        if to_agent not in self.agent_urls:
            print(f"❌ Agente destinatário {to_agent} não encontrado")
            return None
        
        try:
            # Pega URL do agente destinatário
            agent_url = self.agent_urls[to_agent]
            
            # Monta mensagem A2A
            message = {
                "method": method,
                "params": params,
                "from_agent": from_agent,
                "to_agent": to_agent,
                "timestamp": datetime.now().isoformat()
            }
            
            # Log da mensagem
            self.log_message("a2a_message", f"{from_agent} → {to_agent}: {method}", message)
            
            # Envia mensagem HTTP ao endpoint /run do agente
            run_url = f"{agent_url}/run"
            response = requests.post(run_url, json={"prompt": params.get("query", "")}, timeout=10)
            
            if response.status_code == 200:
                response_data = {
                    "from_agent": to_agent,
                    "to_agent": from_agent,
                    "response": response.json().get("response", ""),
                    "timestamp": datetime.now().isoformat()
                }
                
                self.log_message("a2a_response", f"{to_agent} → {from_agent}: resposta", response_data)
                return response_data
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            
        except Exception as e:
            error_msg = f"❌ Erro na comunicação A2A: {str(e)}"
            print(error_msg)
            self.log_message("a2a_error", error_msg, {"error": str(e)})
            return None
    
    def log_message(self, message_type: str, description: str, data: Dict[str, Any]):
        """Registra mensagem no log A2A"""
        log_entry = {
            "type": message_type,
            "description": description,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        self.message_log.append(log_entry)
        print(f"📋 A2A Log: {description}")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Retorna status de todos os agentes registrados"""
        return {
            "agents": self.agent_registry,
            "total_agents": len(self.agent_registry),
            "total_messages": len(self.message_log),
            "last_activity": self.message_log[-1]["timestamp"] if self.message_log else None
        }
    
    def get_message_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna log de mensagens A2A"""
        return self.message_log[-limit:]
    
    def ping_all_agents(self) -> Dict[str, bool]:
        """Verifica status de todos os agentes"""
        results = {}
        
        for name, info in self.agent_registry.items():
            try:
                response = requests.get(info["card_url"], timeout=3)
                is_alive = response.status_code == 200
                results[name] = is_alive
                
                if is_alive:
                    info["status"] = "online"
                    info["last_ping"] = datetime.now().isoformat()
                else:
                    info["status"] = "offline"
                    
            except Exception:
                results[name] = False
                info["status"] = "error"
        
        return results


# Instância global do orquestrador
a2a_orchestrator = A2AOrchestrator()

# Registra agentes padrão
def initialize_a2a_agents():
    """Inicializa registro dos agentes A2A"""
    agents_config = [
        ("supervisor", "http://localhost", 8002),
        ("flamengo", "http://localhost", 8003),
        ("fluminense", "http://localhost", 8004),
        ("researcher", "http://localhost", 8005)
    ]
    
    for name, url, port in agents_config:
        a2a_orchestrator.register_agent(name, url, port)
    
    print("🤖 A2A Orchestrator inicializado com 4 agentes")
    return a2a_orchestrator


if __name__ == "__main__":
    """Teste do orquestrador A2A"""
    orchestrator = initialize_a2a_agents()
    
    # Testa descoberta de agentes
    print("\n🔍 Testando descoberta de agentes...")
    for agent_name in ["supervisor", "flamengo", "fluminense", "researcher"]:
        card = orchestrator.discover_agent(agent_name)
        if card:
            print(f"✅ {agent_name}: {card.get('name', 'unknown')}")
        else:
            print(f"❌ {agent_name}: não encontrado")
    
    # Mostra status
    print(f"\n📊 Status: {orchestrator.get_agent_status()}")