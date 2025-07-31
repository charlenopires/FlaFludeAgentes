"""
Sistema de Log Aprimorado para FlaFludeAgentes
Monitora fluxo completo dos agentes ADK, protocolo A2A e sistema geral
"""

import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import threading
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class LogLevel(Enum):
    """Níveis de log personalizados para o sistema"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    AGENT_ACTION = "AGENT_ACTION"
    A2A_MESSAGE = "A2A_MESSAGE"
    SYSTEM_EVENT = "SYSTEM_EVENT"
    DEBATE_FLOW = "DEBATE_FLOW"


class LogCategory(Enum):
    """Categorias de log para filtros"""
    SYSTEM = "system"
    AGENT = "agent"
    A2A_PROTOCOL = "a2a_protocol"
    DEBATE = "debate"
    SESSION = "session"
    TOOL_EXECUTION = "tool_execution"
    ERROR_HANDLING = "error_handling"
    PERFORMANCE = "performance"


@dataclass
class LogEntry:
    """Estrutura padronizada de entrada de log"""
    timestamp: str
    level: str
    category: str
    agent_name: Optional[str]
    session_id: Optional[str]
    user_id: Optional[str]
    event_type: str
    message: str
    details: Dict[str, Any]
    duration_ms: Optional[float] = None
    correlation_id: Optional[str] = None
    thread_id: Optional[str] = None


class EnhancedLogger:
    """Sistema de log aprimorado com estrutura JSON e filtros avançados"""
    
    def __init__(self, log_dir: str = "logs", max_entries: int = 10000):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.max_entries = max_entries
        self.entries: List[LogEntry] = []
        self.lock = threading.Lock()
        
        # Configuração do logger padrão
        self.setup_file_logging()
        
        # Métricas de performance
        self.metrics = {
            "total_events": 0,
            "agent_executions": 0,
            "a2a_messages": 0,
            "errors": 0,
            "avg_response_time": 0.0,
            "session_count": 0
        }
    
    def setup_file_logging(self):
        """Configura logging para arquivos com rotação"""
        log_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        )
        
        # Log geral do sistema
        self.system_logger = logging.getLogger('FlaFludeSystem')
        self.system_logger.setLevel(logging.DEBUG)
        
        # Handler para arquivo geral
        system_handler = logging.FileHandler(
            self.log_dir / f"system_{datetime.now().strftime('%Y%m%d')}.log"
        )
        system_handler.setFormatter(log_formatter)
        self.system_logger.addHandler(system_handler)
        
        # Log específico para agentes
        self.agent_logger = logging.getLogger('FlaFludeAgents')
        self.agent_logger.setLevel(logging.DEBUG)
        
        # Handler para arquivo de agentes
        agent_handler = logging.FileHandler(
            self.log_dir / f"agents_{datetime.now().strftime('%Y%m%d')}.log"
        )
        agent_handler.setFormatter(log_formatter)
        self.agent_logger.addHandler(agent_handler)
        
        # Log específico para A2A
        self.a2a_logger = logging.getLogger('FlaFludeA2A')
        self.a2a_logger.setLevel(logging.DEBUG)
        
        # Handler para arquivo A2A
        a2a_handler = logging.FileHandler(
            self.log_dir / f"a2a_{datetime.now().strftime('%Y%m%d')}.log"
        )
        a2a_handler.setFormatter(log_formatter)
        self.a2a_logger.addHandler(a2a_handler)
    
    def log(self, 
            level: LogLevel,
            category: LogCategory, 
            message: str,
            agent_name: Optional[str] = None,
            session_id: Optional[str] = None,
            user_id: Optional[str] = None,
            event_type: str = "general",
            details: Optional[Dict[str, Any]] = None,
            duration_ms: Optional[float] = None,
            correlation_id: Optional[str] = None) -> str:
        """
        Log principal com estrutura padronizada
        Retorna correlation_id para rastreamento
        """
        
        if correlation_id is None:
            correlation_id = str(uuid.uuid4())[:8]
        
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level.value,
            category=category.value,
            agent_name=agent_name,
            session_id=session_id,
            user_id=user_id,
            event_type=event_type,
            message=message,
            details=details or {},
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            thread_id=threading.current_thread().name
        )
        
        with self.lock:
            self.entries.append(entry)
            
            # Limita o número de entries em memória
            if len(self.entries) > self.max_entries:
                self.entries = self.entries[-self.max_entries:]
            
            # Atualiza métricas
            self._update_metrics(entry)
        
        # Log para arquivo apropriado
        self._write_to_file(entry)
        
        return correlation_id
    
    def _update_metrics(self, entry: LogEntry):
        """Atualiza métricas do sistema"""
        self.metrics["total_events"] += 1
        
        if entry.category == LogCategory.AGENT.value:
            self.metrics["agent_executions"] += 1
        
        if entry.category == LogCategory.A2A_PROTOCOL.value:
            self.metrics["a2a_messages"] += 1
        
        if entry.level in [LogLevel.ERROR.value, LogLevel.CRITICAL.value]:
            self.metrics["errors"] += 1
        
        if entry.duration_ms:
            # Calcula média móvel do tempo de resposta
            current_avg = self.metrics["avg_response_time"]
            total_events = self.metrics["total_events"]
            self.metrics["avg_response_time"] = (
                (current_avg * (total_events - 1) + entry.duration_ms) / total_events
            )
    
    def _write_to_file(self, entry: LogEntry):
        """Escreve entrada para o arquivo apropriado"""
        log_message = f"{entry.message} | {json.dumps(entry.details, ensure_ascii=False)}"
        
        if entry.category == LogCategory.AGENT.value:
            if entry.level == LogLevel.ERROR.value:
                self.agent_logger.error(log_message)
            elif entry.level == LogLevel.WARNING.value:
                self.agent_logger.warning(log_message)
            else:
                self.agent_logger.info(log_message)
        
        elif entry.category == LogCategory.A2A_PROTOCOL.value:
            self.a2a_logger.info(log_message)
        
        else:
            if entry.level == LogLevel.ERROR.value:
                self.system_logger.error(log_message)
            elif entry.level == LogLevel.WARNING.value:
                self.system_logger.warning(log_message)
            else:
                self.system_logger.info(log_message)
    
    def get_recent_logs(self, 
                       limit: int = 100,
                       category: Optional[LogCategory] = None,
                       agent_name: Optional[str] = None,
                       level: Optional[LogLevel] = None) -> List[Dict[str, Any]]:
        """Recupera logs recentes com filtros"""
        with self.lock:
            filtered_entries = self.entries.copy()
        
        # Aplica filtros
        if category:
            filtered_entries = [e for e in filtered_entries if e.category == category.value]
        
        if agent_name:
            filtered_entries = [e for e in filtered_entries if e.agent_name == agent_name]
        
        if level:
            filtered_entries = [e for e in filtered_entries if e.level == level.value]
        
        # Ordena por timestamp (mais recentes primeiro)
        filtered_entries.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Limita resultado
        return [asdict(entry) for entry in filtered_entries[:limit]]
    
    def get_agent_flow(self, session_id: str, correlation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Recupera fluxo completo de uma sessão ou correlação específica"""
        with self.lock:
            entries = self.entries.copy()
        
        if correlation_id:
            filtered = [e for e in entries if e.correlation_id == correlation_id]
        else:
            filtered = [e for e in entries if e.session_id == session_id]
        
        # Ordena cronologicamente
        filtered.sort(key=lambda x: x.timestamp)
        
        return [asdict(entry) for entry in filtered]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de performance do sistema"""
        with self.lock:
            return {
                **self.metrics.copy(),
                "memory_entries": len(self.entries),
                "uptime_hours": (time.time() - getattr(self, 'start_time', time.time())) / 3600,
                "log_files": list(self.log_dir.glob("*.log"))
            }
    
    def search_logs(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Busca textual nos logs"""
        with self.lock:
            entries = self.entries.copy()
        
        query_lower = query.lower()
        matches = []
        
        for entry in entries:
            if (query_lower in entry.message.lower() or 
                query_lower in str(entry.details).lower() or
                (entry.agent_name and query_lower in entry.agent_name.lower())):
                matches.append(entry)
        
        # Ordena por relevância (mais recentes primeiro)
        matches.sort(key=lambda x: x.timestamp, reverse=True)
        
        return [asdict(entry) for entry in matches[:limit]]
    
    def export_logs(self, format: str = "json", time_range: Optional[tuple] = None) -> str:
        """Exporta logs em formato especificado"""
        with self.lock:
            entries = self.entries.copy()
        
        if time_range:
            start_time, end_time = time_range
            entries = [e for e in entries if start_time <= e.timestamp <= end_time]
        
        if format.lower() == "json":
            return json.dumps([asdict(entry) for entry in entries], 
                            indent=2, ensure_ascii=False)
        
        elif format.lower() == "csv":
            try:
                import csv
                import io
                
                output = io.StringIO()
                if entries:
                    # Converte entries para dicionários
                    entries_dict = [asdict(entry) for entry in entries]
                    
                    writer = csv.DictWriter(output, fieldnames=entries_dict[0].keys())
                    writer.writeheader()
                    for entry_dict in entries_dict:
                        writer.writerow(entry_dict)
                
                return output.getvalue()
            except Exception as e:
                return f"Erro na exportação CSV: {str(e)}"
        
        return str(entries)

    # Métodos de conveniência para diferentes tipos de log
    
    def log_agent_start(self, agent_name: str, session_id: str, user_id: str, prompt: str) -> str:
        """Log específico para início de execução de agente"""
        return self.log(
            LogLevel.AGENT_ACTION,
            LogCategory.AGENT,
            f"Agent {agent_name} iniciando execução",
            agent_name=agent_name,
            session_id=session_id,
            user_id=user_id,
            event_type="agent_start",
            details={"prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt}
        )
    
    def log_agent_response(self, agent_name: str, session_id: str, response: str, 
                          duration_ms: float, correlation_id: str) -> str:
        """Log específico para resposta de agente"""
        return self.log(
            LogLevel.AGENT_ACTION,
            LogCategory.AGENT,
            f"Agent {agent_name} completou execução",
            agent_name=agent_name,
            session_id=session_id,
            event_type="agent_response",
            details={
                "response_length": len(response),
                "response_preview": response[:200] + "..." if len(response) > 200 else response
            },
            duration_ms=duration_ms,
            correlation_id=correlation_id
        )
    
    def log_tool_execution(self, agent_name: str, tool_name: str, parameters: Dict[str, Any], 
                          result: str, duration_ms: float) -> str:
        """Log específico para execução de tools"""
        return self.log(
            LogLevel.INFO,
            LogCategory.TOOL_EXECUTION,
            f"Tool {tool_name} executada por {agent_name}",
            agent_name=agent_name,
            event_type="tool_execution",
            details={
                "tool_name": tool_name,
                "parameters": parameters,
                "result_preview": result[:100] + "..." if len(result) > 100 else result
            },
            duration_ms=duration_ms
        )
    
    def log_a2a_message(self, from_agent: str, to_agent: str, message_type: str, 
                       content: Dict[str, Any], correlation_id: str) -> str:
        """Log específico para mensagens A2A"""
        return self.log(
            LogLevel.A2A_MESSAGE,
            LogCategory.A2A_PROTOCOL,
            f"A2A: {from_agent} → {to_agent} ({message_type})",
            event_type="a2a_message",
            details={
                "from_agent": from_agent,
                "to_agent": to_agent,
                "message_type": message_type,
                "content": content
            },
            correlation_id=correlation_id
        )
    
    def log_debate_event(self, event_type: str, details: Dict[str, Any], 
                        session_id: Optional[str] = None) -> str:
        """Log específico para eventos do debate"""
        return self.log(
            LogLevel.DEBATE_FLOW,
            LogCategory.DEBATE,
            f"Debate: {event_type}",
            session_id=session_id,
            event_type=event_type,
            details=details
        )
    
    def log_error(self, error: Exception, context: str, agent_name: Optional[str] = None,
                 session_id: Optional[str] = None, correlation_id: Optional[str] = None) -> str:
        """Log específico para erros"""
        return self.log(
            LogLevel.ERROR,
            LogCategory.ERROR_HANDLING,
            f"Erro em {context}: {str(error)}",
            agent_name=agent_name,
            session_id=session_id,
            event_type="error",
            details={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context
            },
            correlation_id=correlation_id
        )


# Instância global do logger
enhanced_logger = EnhancedLogger()

# Funções de conveniência para uso direto
def log_agent_start(agent_name: str, session_id: str, user_id: str, prompt: str) -> str:
    return enhanced_logger.log_agent_start(agent_name, session_id, user_id, prompt)

def log_agent_response(agent_name: str, session_id: str, response: str, 
                      duration_ms: float, correlation_id: str) -> str:
    return enhanced_logger.log_agent_response(agent_name, session_id, response, duration_ms, correlation_id)

def log_tool_execution(agent_name: str, tool_name: str, parameters: Dict[str, Any], 
                      result: str, duration_ms: float) -> str:
    return enhanced_logger.log_tool_execution(agent_name, tool_name, parameters, result, duration_ms)

def log_a2a_message(from_agent: str, to_agent: str, message_type: str, 
                   content: Dict[str, Any], correlation_id: str) -> str:
    return enhanced_logger.log_a2a_message(from_agent, to_agent, message_type, content, correlation_id)

def log_debate_event(event_type: str, details: Dict[str, Any], 
                    session_id: Optional[str] = None) -> str:
    return enhanced_logger.log_debate_event(event_type, details, session_id)

def log_error(error: Exception, context: str, agent_name: Optional[str] = None,
             session_id: Optional[str] = None, correlation_id: Optional[str] = None) -> str:
    return enhanced_logger.log_error(error, context, agent_name, session_id, correlation_id)