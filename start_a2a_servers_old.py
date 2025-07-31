#!/usr/bin/env python3
"""
Start A2A Servers - Inicia todos os servidores A2A dos agentes
Script para executar todos os agentes como servidores A2A em paralelo
"""

import os
import sys
import time
import signal
import subprocess
import threading
from typing import List, Dict

class A2AServerManager:
    """Gerenciador para iniciar e monitorar servidores A2A"""
    
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.servers = [
            {"name": "Supervisor", "module": "supervisor_agent.agent", "port": 8002, "emoji": "🤖⚖️"},
            {"name": "Flamengo", "module": "flamengo_agent.agent", "port": 8003, "emoji": "🤖🔴"},
            {"name": "Fluminense", "module": "fluminense_agent.agent", "port": 8004, "emoji": "🤖🟢"},
            {"name": "Researcher", "module": "researcher_agent.agent", "port": 8005, "emoji": "🤖📊"}
        ]
    
    def start_servers(self):
        """Inicia todos os servidores A2A"""
        print("🚀 Iniciando servidores A2A para todos os agentes...")
        print("📋 Pressione Ctrl+C para parar todos os servidores\n")
        
        for server in self.servers:
            self.start_server(server)
            time.sleep(2)  # Aguarda um pouco entre inicializações
        
        self.monitor_servers()
    
    def start_server(self, server: Dict):
        """Inicia um servidor A2A específico"""
        try:
            # Usa python do ambiente virtual se disponível
            python_cmd = ".venv/bin/python" if os.path.exists(".venv/bin/python") else "python"
            
            # Comando para iniciar o servidor
            cmd = [python_cmd, "-m", server["module"]]
            
            # Inicia o processo
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes.append(process)
            
            print(f"{server['emoji']} {server['name']} Agent A2A Server")
            print(f"   📡 Porta: {server['port']}")
            print(f"   🔗 Agent Card: http://localhost:{server['port']}/.well-known/agent.json")
            print(f"   🆔 PID: {process.pid}")
            print()
            
        except Exception as e:
            print(f"❌ Erro ao iniciar {server['name']}: {str(e)}")
    
    def monitor_servers(self):
        """Monitora servidores e aguarda interrupção"""
        try:
            print("✅ Todos os servidores A2A iniciados!")
            print("🌐 URLs dos Agent Cards:")
            for server in self.servers:
                print(f"   • {server['name']}: http://localhost:{server['port']}/.well-known/agent.json")
            
            print(f"\n📊 {len(self.processes)} processos ativos")
            print("⏳ Aguardando... (Ctrl+C para parar)")
            
            # Aguarda até que todos os processos terminem ou Ctrl+C
            while True:
                active_processes = [p for p in self.processes if p.poll() is None]
                
                if not active_processes:
                    print("\n⚠️ Todos os processos terminaram")
                    break
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop_servers()
    
    def stop_servers(self):
        """Para todos os servidores A2A"""
        print("\n🛑 Parando todos os servidores A2A...")
        
        for i, process in enumerate(self.processes):
            if process.poll() is None:  # Processo ainda ativo
                server_name = self.servers[i]['name']
                print(f"   ⏹️ Parando {server_name} (PID: {process.pid})")
                
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"   🔥 Forçando parada de {server_name}")
                    process.kill()
                except Exception as e:
                    print(f"   ❌ Erro ao parar {server_name}: {str(e)}")
        
        print("✅ Todos os servidores A2A foram parados")
    
    def signal_handler(self, signum, frame):
        """Handler para sinais de interrupção"""
        self.stop_servers()
        sys.exit(0)


def main():
    """Função principal"""
    print("🔥 FLA-FLU DEBATE - A2A SERVERS MANAGER")
    print("=" * 50)
    
    # Verifica se está no diretório correto
    if not os.path.exists("supervisor_agent"):
        print("❌ Execute este script no diretório raiz do projeto FlaFludeAgentes")
        sys.exit(1)
    
    # Cria gerenciador
    manager = A2AServerManager()
    
    # Configura handler para Ctrl+C
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    # Inicia servidores
    try:
        manager.start_servers()
    except Exception as e:
        print(f"❌ Erro fatal: {str(e)}")
        manager.stop_servers()
        sys.exit(1)


if __name__ == "__main__":
    main()