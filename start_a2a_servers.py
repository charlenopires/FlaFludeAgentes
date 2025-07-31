#!/usr/bin/env python3
"""
Script para iniciar todos os servidores A2A usando Google ADK oficial
Refatorado para usar apenas implementações oficiais do ADK
"""

import os
import sys
import time
import asyncio
import subprocess
from multiprocessing import Process
from typing import List
import signal

def start_agent_server(agent_module: str, port: int, agent_name: str):
    """Inicia um servidor A2A individual usando ADK oficial"""
    try:
        print(f"🚀 Iniciando servidor {agent_name} na porta {port}...")
        
        # Executa o módulo do agente
        result = subprocess.run([
            sys.executable, "-m", agent_module
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar servidor {agent_name}: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado no servidor {agent_name}: {e}")

def check_agent_health(port: int, agent_name: str) -> bool:
    """Verifica se o agente está rodando corretamente"""
    try:
        import httpx
        response = httpx.get(f"http://localhost:{port}/.well-known/agent.json", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Função principal para iniciar todos os servidores A2A"""
    print("🤖 Iniciando Sistema Multi-Agente com Google ADK oficial")
    print("=" * 60)
    
    # Configuração dos agentes com ADK oficial
    agents_config = [
        {
            "name": "Supervisor Agent",
            "module": "supervisor_agent.agent",
            "port": 8002,
            "emoji": "🤖⚖️"
        },
        {
            "name": "Flamengo Agent", 
            "module": "flamengo_agent.agent",
            "port": 8003,
            "emoji": "🤖🔴"
        },
        {
            "name": "Fluminense Agent",
            "module": "fluminense_agent.agent", 
            "port": 8004,
            "emoji": "🤖🟢"
        },
        {
            "name": "Researcher Agent",
            "module": "researcher_agent.agent",
            "port": 8005,
            "emoji": "🤖📊"
        }
    ]
    
    processes: List[Process] = []
    
    try:
        # Inicia cada servidor A2A em processo separado
        for agent in agents_config:
            print(f"{agent['emoji']} Iniciando {agent['name']} na porta {agent['port']}...")
            
            process = Process(
                target=start_agent_server,
                args=(agent['module'], agent['port'], agent['name'])
            )
            process.start()
            processes.append(process)
            time.sleep(2)  # Aguarda um pouco entre inicializações
        
        print("\n✅ Todos os servidores A2A iniciados!")
        print("=" * 60)
        
        # Verifica status dos agentes
        print("🔍 Verificando status dos agentes...")
        time.sleep(5)  # Aguarda servidores iniciarem
        
        for agent in agents_config:
            if check_agent_health(agent['port'], agent['name']):
                print(f"✅ {agent['emoji']} {agent['name']}: Online na porta {agent['port']}")
                print(f"   Agent Card: http://localhost:{agent['port']}/.well-known/agent.json")
            else:
                print(f"❌ {agent['emoji']} {agent['name']}: Offline ou com problemas")
        
        print("\n" + "=" * 60)
        print("🎯 Sistema A2A pronto! Execute: uv run streamlit run app.py")
        print("💡 Pressione Ctrl+C para parar todos os servidores")
        print("=" * 60)
        
        # Aguarda sinal de interrupção
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando todos os servidores A2A...")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        
    finally:
        # Para todos os processos
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()
        
        print("✅ Todos os servidores A2A foram parados")

if __name__ == "__main__":
    main()