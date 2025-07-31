#!/usr/bin/env python3
"""
Script de Teste do Sistema de Logging Aprimorado
Demonstra todas as funcionalidades implementadas
"""

import time
from utils.enhanced_logger import (
    enhanced_logger, 
    LogLevel, 
    LogCategory,
    log_agent_start,
    log_agent_response,
    log_tool_execution,
    log_a2a_message,
    log_debate_event,
    log_error
)

def test_basic_logging():
    """Testa logging básico"""
    print("🔍 Testando logging básico...")
    
    enhanced_logger.log(
        LogLevel.INFO,
        LogCategory.SYSTEM,
        "Sistema de teste iniciado",
        event_type="test_start",
        details={"test_version": "1.0"}
    )
    
    enhanced_logger.log(
        LogLevel.AGENT_ACTION,
        LogCategory.AGENT,
        "Agente de teste executando",
        agent_name="test_agent",
        event_type="agent_test",
        details={"operation": "unit_test"}
    )
    
    print("✅ Logging básico funcionando!")

def test_agent_logging():
    """Testa logging específico de agentes"""
    print("🤖 Testando logging de agentes...")
    
    # Simula execução de agente
    correlation_id = log_agent_start(
        agent_name="supervisor",
        session_id="test_session_123",
        user_id="test_user_456",
        prompt="Teste de funcionamento do sistema"
    )
    
    time.sleep(0.1)  # Simula processamento
    
    log_agent_response(
        agent_name="supervisor",
        session_id="test_session_123",
        response="Resposta de teste do supervisor",
        duration_ms=100.5,
        correlation_id=correlation_id
    )
    
    print("✅ Logging de agentes funcionando!")

def test_tool_logging():
    """Testa logging de ferramentas"""
    print("🔧 Testando logging de ferramentas...")
    
    log_tool_execution(
        agent_name="supervisor",
        tool_name="start_debate_tool",
        parameters={"duration_minutes": 5},
        result="Debate iniciado com sucesso",
        duration_ms=50.2
    )
    
    print("✅ Logging de ferramentas funcionando!")

def test_a2a_logging():
    """Testa logging A2A"""
    print("📡 Testando logging A2A...")
    
    log_a2a_message(
        from_agent="flamengo",
        to_agent="researcher",
        message_type="research_request",
        content={"query": "dados sobre títulos"},
        correlation_id="test_corr_789"
    )
    
    print("✅ Logging A2A funcionando!")

def test_debate_logging():
    """Testa logging de debate"""
    print("🎭 Testando logging de debate...")
    
    log_debate_event(
        event_type="debate_started",
        details={
            "duration_minutes": 5,
            "starting_team": "flamengo",
            "participants": ["flamengo", "fluminense"]
        },
        session_id="debate_test_session"
    )
    
    print("✅ Logging de debate funcionando!")

def test_error_logging():
    """Testa logging de erros"""
    print("❌ Testando logging de erros...")
    
    try:
        # Simula um erro
        raise ValueError("Erro simulado para teste")
    except Exception as e:
        log_error(
            error=e,
            context="test_error_simulation",
            agent_name="test_agent",
            correlation_id="error_test_123"
        )
    
    print("✅ Logging de erros funcionando!")

def test_search_and_retrieval():
    """Testa busca e recuperação de logs"""
    print("🔍 Testando busca e recuperação...")
    
    # Busca logs recentes
    recent_logs = enhanced_logger.get_recent_logs(limit=5)
    print(f"📋 Encontrados {len(recent_logs)} logs recentes")
    
    # Busca por texto
    search_results = enhanced_logger.search_logs("teste", limit=10)
    print(f"🔎 Encontrados {len(search_results)} logs com 'teste'")
    
    # Métricas de performance
    metrics = enhanced_logger.get_performance_metrics()
    print(f"📊 Métricas: {metrics['total_events']} eventos, {metrics['errors']} erros")
    
    print("✅ Busca e recuperação funcionando!")

def test_export():
    """Testa exportação de logs"""
    print("📥 Testando exportação...")
    
    # Exporta em JSON
    json_export = enhanced_logger.export_logs(format="json")
    print(f"📄 Exportação JSON: {len(json_export)} caracteres")
    
    # Exporta em CSV
    csv_export = enhanced_logger.export_logs(format="csv")
    print(f"📊 Exportação CSV: {len(csv_export)} caracteres")
    
    print("✅ Exportação funcionando!")

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes do Sistema de Logging Aprimorado")
    print("=" * 60)
    
    test_basic_logging()
    test_agent_logging()
    test_tool_logging()
    test_a2a_logging()
    test_debate_logging()
    test_error_logging()
    test_search_and_retrieval()
    test_export()
    
    print("=" * 60)
    print("🎉 Todos os testes concluídos com sucesso!")
    print("\n📊 Estatísticas finais:")
    
    metrics = enhanced_logger.get_performance_metrics()
    for key, value in metrics.items():
        print(f"  • {key}: {value}")
    
    print("\n💡 Para visualizar os logs, execute:")
    print("  uv run streamlit run app.py")
    print("  E clique em '📈 Mostrar Logs' na interface")

if __name__ == "__main__":
    main()