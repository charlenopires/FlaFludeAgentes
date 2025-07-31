"""
ADK Agents - Sistema Multi-Agente usando Google ADK com A2A Protocol
Inicializa e coordena todos os 4 agentes do debate Fla-Flu via A2A
"""

import os
from typing import Dict, Any
from google.adk.agents import Agent
from dotenv import load_dotenv

# Importa as funções de criação dos agentes
from supervisor_agent.agent import create_supervisor_agent
from flamengo_agent.agent import create_flamengo_agent
from fluminense_agent.agent import create_fluminense_agent
from researcher_agent.agent import create_researcher_agent

# Importa orquestrador A2A
from a2a_orchestrator import initialize_a2a_agents, a2a_orchestrator

# Carrega variáveis do .env
load_dotenv()

class ADKDebateSystem:
    """
    Sistema de Debate usando Google ADK
    Coordena 4 agentes especializados em debate Flamengo vs Fluminense
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.initialized = False
    
    def initialize_agents(self) -> Dict[str, Agent]:
        """Inicializa todos os agentes ADK com suporte A2A"""
        try:
            print("🤖 Inicializando sistema de agentes ADK com A2A...")
            
            # Cria todos os agentes locais
            self.agents = {
                'supervisor': create_supervisor_agent(),
                'flamengo': create_flamengo_agent(),
                'fluminense': create_fluminense_agent(),
                'researcher': create_researcher_agent()
            }
            
            # Inicializa orquestrador A2A
            self.a2a_orchestrator = initialize_a2a_agents()
            
            self.initialized = True
            print("✅ Sistema ADK com A2A inicializado com sucesso!")
            print(f"📊 {len(self.agents)} agentes locais carregados")
            print("🔗 Orquestrador A2A configurado para descoberta de agentes")
            
            return self.agents
            
        except Exception as e:
            print(f"❌ Erro ao inicializar agentes ADK: {str(e)}")
            return {}
    
    def get_agent(self, agent_name: str) -> Agent:
        """Retorna um agente específico"""
        if not self.initialized:
            self.initialize_agents()
        
        return self.agents.get(agent_name)
    
    def get_all_agents(self) -> Dict[str, Agent]:
        """Retorna todos os agentes"""
        if not self.initialized:
            self.initialize_agents()
        
        return self.agents
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status do sistema ADK"""
        return {
            "initialized": self.initialized,
            "agents_count": len(self.agents),
            "agent_names": list(self.agents.keys()),
            "adk_version": "1.8.0",
            "system_type": "Multi-Agent Debate System"
        }

# Instância global do sistema
adk_system = ADKDebateSystem()

# Funções de conveniência para compatibilidade
def get_supervisor_agent() -> Agent:
    """Retorna o agente supervisor"""
    return adk_system.get_agent('supervisor')

def get_flamengo_agent() -> Agent:
    """Retorna o agente do Flamengo"""
    return adk_system.get_agent('flamengo')

def get_fluminense_agent() -> Agent:
    """Retorna o agente do Fluminense"""
    return adk_system.get_agent('fluminense')

def get_researcher_agent() -> Agent:
    """Retorna o agente pesquisador"""
    return adk_system.get_agent('researcher')

def initialize_all_agents() -> Dict[str, Agent]:
    """Inicializa todos os agentes ADK"""
    return adk_system.initialize_agents()

def get_adk_system_status() -> Dict[str, Any]:
    """Retorna status completo do sistema ADK"""
    return adk_system.get_system_status()

# Teste básico
if __name__ == "__main__":
    print("🚀 Testando Sistema ADK...")
    
    # Inicializa sistema
    agents = initialize_all_agents()
    
    if agents:
        print("\n📋 Agentes disponíveis:")
        for name, agent in agents.items():
            print(f"  ✅ {name}: {agent.name}")
        
        print(f"\n📊 Status: {get_adk_system_status()}")
        print("\n🎉 Sistema ADK funcionando corretamente!")
    else:
        print("\n❌ Falha na inicialização do sistema ADK")