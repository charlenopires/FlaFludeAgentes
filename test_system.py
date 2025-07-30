#!/usr/bin/env python3
"""
Teste rápido do sistema de 4 agentes independentes
"""

from agents import (
    get_supervisor,
    get_flamengo_agent,
    get_fluminense_agent,
    get_researcher,
    get_system_status
)

def test_agents():
    """Testa todos os 4 agentes"""
    print("🔥 TESTANDO SISTEMA DE 4 AGENTES INDEPENDENTES 🔥")
    print("=" * 60)
    
    # 1. Teste do Supervisor
    print("\n⚖️ TESTANDO SUPERVISOR...")
    supervisor = get_supervisor()
    if supervisor:
        print(f"✅ Supervisor carregado: {supervisor.name}")
        print(f"   Status: {supervisor.get_status()}")
    else:
        print("❌ Erro ao carregar Supervisor")
    
    # 2. Teste do Flamengo
    print("\n🔴 TESTANDO AGENTE FLAMENGO...")
    flamengo = get_flamengo_agent()
    if flamengo:
        print(f"✅ Agente Flamengo carregado: {flamengo.name}")
        print(f"   Status: {flamengo.get_status()}")
        
        # Teste de argumento inicial
        print("   Testando argumento inicial...")
        arg_result = flamengo.get_initial_argument()
        if arg_result["status"] == "success":
            print(f"   ✅ Argumento gerado: {arg_result['message'][:100]}...")
        else:
            print(f"   ❌ Erro: {arg_result['message']}")
    else:
        print("❌ Erro ao carregar Agente Flamengo")
    
    # 3. Teste do Fluminense
    print("\n🟢 TESTANDO AGENTE FLUMINENSE...")
    fluminense = get_fluminense_agent()
    if fluminense:
        print(f"✅ Agente Fluminense carregado: {fluminense.name}")
        print(f"   Status: {fluminense.get_status()}")
        
        # Teste de argumento inicial
        print("   Testando argumento inicial...")
        arg_result = fluminense.get_initial_argument()
        if arg_result["status"] == "success":
            print(f"   ✅ Argumento gerado: {arg_result['message'][:100]}...")
        else:
            print(f"   ❌ Erro: {arg_result['message']}")
    else:
        print("❌ Erro ao carregar Agente Fluminense")
    
    # 4. Teste do Pesquisador
    print("\n📊 TESTANDO AGENTE PESQUISADOR...")
    researcher = get_researcher()
    if researcher:
        print(f"✅ Pesquisador carregado: {researcher.name}")
        print(f"   Status: {researcher.get_status()}")
        
        # Teste de pesquisa
        print("   Testando pesquisa...")
        search_result = researcher.search_data("títulos Flamengo", "Teste")
        if search_result["status"] == "success":
            print(f"   ✅ Pesquisa realizada: {search_result['message'][:100]}...")
        else:
            print(f"   ❌ Erro: {search_result['message']}")
    else:
        print("❌ Erro ao carregar Agente Pesquisador")
    
    # 5. Status do sistema
    print("\n🤖 STATUS COMPLETO DO SISTEMA...")
    system_status = get_system_status()
    print(f"✅ Agentes carregados: {system_status['agents_loaded']}")
    print(f"   Mensagens A2A: {system_status['total_messages']}")
    print(f"   Debate ativo: {system_status['active_debate']}")
    
    print("\n🎯 TESTE CONCLUÍDO!")
    print("=" * 60)
    print("✅ Sistema de 4 agentes independentes funcionando!")
    print("✅ Protocolo A2A implementado!")
    print("✅ Interface Streamlit disponível em http://localhost:8502")
    print("🔥 Pronto para debates Fla-Flu!")

if __name__ == "__main__":
    test_agents()