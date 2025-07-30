"""
Interface Streamlit para Sistema de Debate Fla-Flu
4 Agentes Independentes + Protocolo A2A + Google ADK
"""

import streamlit as st
import time
import json
from datetime import datetime
from typing import Dict, Any, List
from agents import (
    get_supervisor, 
    get_flamengo_agent, 
    get_fluminense_agent, 
    get_researcher,
    get_system_status,
    debate_system
)

# --- Configuração da Página ---
st.set_page_config(
    page_title="🔥 Fla-Flu Debate: 4 Agentes A2A",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Estilos CSS Avançados ---
st.markdown("""
<style>
    /* Tema principal */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 50%, #8B0000 100%);
        color: #ffffff;
    }
    
    /* Header personalizado */
    .main-header {
        background: linear-gradient(90deg, #DC143C 0%, #8B0000 50%, #006400 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Cards dos agentes */
    .agent-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* Status indicators */
    .status-active { color: #4CAF50; font-weight: bold; text-shadow: 0 0 10px #4CAF50; }
    .status-waiting { color: #FF9800; font-weight: bold; text-shadow: 0 0 10px #FF9800; }
    .status-speaking { color: #2196F3; font-weight: bold; text-shadow: 0 0 10px #2196F3; }
    .status-finished { color: #F44336; font-weight: bold; text-shadow: 0 0 10px #F44336; }
    
    /* Chat messages */
    .chat-message {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid;
        backdrop-filter: blur(5px);
    }
    
    .flamengo-msg { border-left-color: #DC143C; background: rgba(220, 20, 60, 0.1); }
    .fluminense-msg { border-left-color: #008000; background: rgba(0, 128, 0, 0.1); }
    .supervisor-msg { border-left-color: #FFD700; background: rgba(255, 215, 0, 0.1); }
    .researcher-msg { border-left-color: #4169E1; background: rgba(65, 105, 225, 0.1); }
    
    /* Bastidores */
    .backstage-panel {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* A2A Protocol indicator */
    .a2a-indicator {
        display: inline-block;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        padding: 3px 8px;
        border-radius: 15px;
        font-size: 0.7em;
        font-weight: bold;
        margin-left: 5px;
    }
    
    /* Timer */
    .timer-display {
        font-family: 'Courier New', monospace;
        font-size: 2em;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Debate controls */
    .debate-controls {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Funções Auxiliares ---
def init_session_state():
    """Inicializa estado da sessão"""
    if 'debate_messages' not in st.session_state:
        st.session_state.debate_messages = []
    if 'backstage_log' not in st.session_state:
        st.session_state.backstage_log = []
    if 'debate_active' not in st.session_state:
        st.session_state.debate_active = False
    if 'debate_finished' not in st.session_state:
        st.session_state.debate_finished = False
    if 'current_turn' not in st.session_state:
        st.session_state.current_turn = None
    if 'debate_duration' not in st.session_state:
        st.session_state.debate_duration = 0
    if 'agents_initialized' not in st.session_state:
        st.session_state.agents_initialized = False

def add_message(agent_name: str, message: str, message_type: str = "normal"):
    """Adiciona mensagem ao chat"""
    st.session_state.debate_messages.append({
        "agent": agent_name,
        "message": message,
        "timestamp": time.time(),
        "type": message_type
    })

def add_backstage_log(log_message: str, log_type: str = "info"):
    """Adiciona log aos bastidores"""
    st.session_state.backstage_log.append({
        "message": log_message,
        "type": log_type,
        "timestamp": time.time(),
        "formatted_time": datetime.now().strftime("%H:%M:%S")
    })

def format_time(seconds: int) -> str:
    """Formata tempo em MM:SS"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def get_agent_emoji(agent_name: str) -> str:
    """Retorna emoji do agente"""
    emojis = {
        "Supervisor": "⚖️",
        "Torcedor Flamengo": "🔴",
        "Torcedor Fluminense": "🟢", 
        "Pesquisador": "📊"
    }
    return emojis.get(agent_name, "🤖")

def get_message_class(agent_name: str) -> str:
    """Retorna classe CSS da mensagem"""
    classes = {
        "Supervisor": "supervisor-msg",
        "Torcedor Flamengo": "flamengo-msg",
        "Torcedor Fluminense": "fluminense-msg",
        "Pesquisador": "researcher-msg"
    }
    return classes.get(agent_name, "chat-message")

# --- Inicialização ---
init_session_state()

# --- Header Principal ---
st.markdown("""
<div class="main-header">
    <h1>🔥 FLA-FLU DEBATE: 4 AGENTES INTELIGENTES 🔥</h1>
    <p><strong>Sistema Multi-Agente com Protocolo A2A + Google ADK</strong></p>
    <p>⚖️ Supervisor | 🔴 Flamengo | 🟢 Fluminense | 📊 Pesquisador</p>
</div>
""", unsafe_allow_html=True)

# --- Layout Principal ---
col1, col2 = st.columns([2, 1])

with col1:
    # --- Área de Chat Principal ---
    st.markdown("### 💬 **Debate em Tempo Real**")
    
    chat_container = st.container()
    
    if not st.session_state.agents_initialized:
        st.markdown("### 🎯 **Bem-vindo ao Sistema de Debate A2A!**")
        
        st.markdown("""
        **🤖 4 Agentes Inteligentes prontos para debater:**
        
        - **⚖️ Supervisor**: Especialista em retórica, psicologia e linguística
        - **🔴 Flamengo**: Torcedor apaixonado com argumentos demolidores  
        - **🟢 Fluminense**: Defensor da tradição e elegância tricolor
        - **📊 Pesquisador**: Busca dados na internet para embasar argumentos
        
        **📋 Como funciona:**
        1. Supervisor pergunta a duração do debate
        2. Divide tempo em 50% para cada time
        3. Agentes debatem com protocolo A2A
        4. Pesquisador fornece dados quando solicitado
        5. Supervisor analisa e declara o vencedor
        """)
        
        if st.button("🚀 **Inicializar Sistema de Agentes**", key="init_agents"):
            with st.spinner("🤖 Carregando agentes ADK..."):
                try:
                    # Inicializa agentes
                    supervisor = get_supervisor()
                    flamengo = get_flamengo_agent()
                    fluminense = get_fluminense_agent()
                    researcher = get_researcher()
                    
                    st.session_state.agents_initialized = True
                    add_backstage_log("Sistema A2A inicializado com sucesso", "success")
                    add_backstage_log("4 agentes carregados e prontos", "info")
                    
                    # Supervisor se apresenta e pergunta duração
                    supervisor_intro = """⚖️ **SUPERVISOR DE DEBATE ATIVADO**

Olá! Sou o Supervisor especializado em retórica, psicologia cognitiva e linguística aplicada.

🎯 **Minha função:**
- Coordenar o tempo do debate (50% para cada time)
- Analisar qualidade argumentativa com critérios técnicos
- Determinar o vencedor baseado em evidências
- Manter neutralidade absoluta

Por favor, **quantos minutos** deve durar nosso debate Flamengo vs Fluminense?

⏱️ Recomendo entre 2 a 10 minutos para um debate dinâmico e completo."""
                    
                    add_message("Supervisor", supervisor_intro, "system")
                    add_backstage_log("Supervisor perguntou duração do debate", "info")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao inicializar agentes: {str(e)}")
                    add_backstage_log(f"Erro na inicialização: {str(e)}", "error")
    
    else:
        # Exibe mensagens do chat
        with chat_container:
            for msg in st.session_state.debate_messages:
                emoji = get_agent_emoji(msg["agent"])
                css_class = get_message_class(msg["agent"])
                timestamp = datetime.fromtimestamp(msg["timestamp"]).strftime("%H:%M:%S")
                
                st.markdown(f"""
                <div class="chat-message {css_class}">
                    <strong>{emoji} {msg["agent"]}</strong> 
                    <span class="a2a-indicator">A2A</span>
                    <small style="float: right; opacity: 0.7;">⏰ {timestamp}</small>
                    <br><br>
                    {msg["message"]}
                </div>
                """, unsafe_allow_html=True)
        
        # --- Controles do Debate ---
        if not st.session_state.debate_active and not st.session_state.debate_finished:
            st.markdown('<div class="debate-controls">', unsafe_allow_html=True)
            st.markdown("### ⚙️ **Configuração do Debate**")
            
            col_duration, col_start = st.columns([1, 1])
            
            with col_duration:
                debate_duration = st.slider(
                    "⏱️ Duração do debate (minutos):",
                    min_value=2, max_value=10, value=5,
                    help="Tempo será dividido igualmente entre os times"
                )
            
            with col_start:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🎬 **INICIAR DEBATE**", key="start_debate", use_container_width=True):
                    with st.spinner("⚖️ Supervisor iniciando debate..."):
                        supervisor = get_supervisor()
                        start_result = supervisor.start_debate(debate_duration)
                        
                        if start_result["status"] == "success":
                            st.session_state.debate_active = True
                            st.session_state.debate_duration = debate_duration
                            st.session_state.current_turn = "Flamengo"
                            
                            add_message("Supervisor", start_result["message"], "system")
                            add_backstage_log(f"Debate iniciado: {debate_duration} minutos", "success")
                            add_backstage_log("Flamengo vai começar!", "info")
                            
                            st.rerun()
                        else:
                            st.error(f"❌ Erro: {start_result['message']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # --- Lógica do Debate Ativo ---
        elif st.session_state.debate_active and not st.session_state.debate_finished:
            
            # Verifica tempo restante
            supervisor = get_supervisor()
            time_info = supervisor.get_time_remaining()
            
            if time_info["total_remaining"] <= 0:
                # Tempo esgotado - análise final
                st.session_state.debate_finished = True
                st.session_state.debate_active = False
                
                add_backstage_log("⏰ Tempo esgotado! Iniciando análise final", "warning")
                
                with st.spinner("🧠 Supervisor analisando debate..."):
                    analysis_result = supervisor.analyze_final_debate(st.session_state.debate_messages)
                    
                    if analysis_result["status"] == "success":
                        add_message("Supervisor", analysis_result["message"], "final")
                        add_backstage_log("Análise final concluída", "success")
                    else:
                        add_message("Supervisor", f"Erro na análise: {analysis_result['message']}", "error")
                
                st.balloons()
                st.rerun()
            
            else:
                # Continua debate
                current_agent = get_flamengo_agent() if st.session_state.current_turn == "Flamengo" else get_fluminense_agent()
                agent_name = f"Torcedor {st.session_state.current_turn}"
                
                with st.spinner(f"🤔 {agent_name} preparando argumento..."):
                    time.sleep(2)  # Simula tempo de processamento
                    
                    # Gera argumento
                    if len(st.session_state.debate_messages) <= 2:  # Primeiro argumento
                        argument_result = current_agent.get_initial_argument()
                    else:
                        # Busca último argumento do oponente
                        if st.session_state.current_turn == "Fluminense":
                            opponent_messages = [m for m in st.session_state.debate_messages if "flamengo" in m["agent"].lower()]
                        else:
                            opponent_messages = [m for m in st.session_state.debate_messages if "fluminense" in m["agent"].lower()]
                        last_opponent = opponent_messages[-1]["message"] if opponent_messages else ""
                        
                        # Verifica se precisa de pesquisa
                        research_data = None
                        if "PESQUISADOR:" in last_opponent.upper():
                            researcher = get_researcher()
                            research_result = researcher.search_data(f"dados sobre {st.session_state.current_turn}", agent_name)
                            if research_result["status"] == "success":
                                research_data = research_result["message"]
                                add_message("Pesquisador", research_result["message"], "research")
                                add_backstage_log("Pesquisa realizada", "info")
                        
                        argument_result = current_agent.counter_argument(last_opponent, research_data)
                    
                    if argument_result["status"] == "success":
                        add_message(agent_name, argument_result["message"], "argument")
                        add_backstage_log(f"{agent_name} argumentou", "info")
                        
                        # Alterna turno
                        st.session_state.current_turn = "Fluminense" if st.session_state.current_turn == "Flamengo" else "Flamengo"
                        
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Erro no agente: {argument_result['message']}")

with col2:
    # --- Painel Lateral: Bastidores ---
    st.markdown("### 🎭 **Bastidores dos Agentes**")
    
    # Status dos agentes
    system_status = get_system_status()
    
    st.markdown("#### 🤖 **Status dos Agentes**")
    
    agents_info = [
        ("Supervisor", "⚖️", "Coordenador"),
        ("Flamengo", "🔴", "Torcedor"),
        ("Fluminense", "🟢", "Torcedor"), 
        ("Pesquisador", "📊", "Dados")
    ]
    
    for agent_name, emoji, role in agents_info:
        if st.session_state.agents_initialized:
            if st.session_state.debate_active:
                if agent_name == st.session_state.current_turn:
                    status = "speaking"
                    status_text = "FALANDO"
                elif agent_name == "Supervisor":
                    status = "active"
                    status_text = "MODERANDO"
                else:
                    status = "waiting" 
                    status_text = "AGUARDANDO"
            elif st.session_state.debate_finished:
                status = "finished"
                status_text = "FINALIZADO"
            else:
                status = "active"
                status_text = "PRONTO"
        else:
            status = "waiting"
            status_text = "CARREGANDO"
        
        st.markdown(f"""
        <div class="agent-card">
            <strong>{emoji} {agent_name}</strong><br>
            <small>{role}</small><br>
            <span class="status-{status}">{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Timer do debate
    if st.session_state.debate_active:
        supervisor = get_supervisor()
        time_info = supervisor.get_time_remaining()
        remaining = int(time_info["total_remaining"])
        
        timer_color = "status-active" if remaining > 60 else "status-waiting" if remaining > 30 else "status-finished"
        
        st.markdown(f"""
        <div class="timer-display">
            <div class="{timer_color}">⏱️ {format_time(remaining)}</div>
            <small>Tempo Restante</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Log de bastidores
    st.markdown("#### 📋 **Log de Eventos A2A**")
    
    backstage_container = st.container()
    with backstage_container:
        if st.session_state.backstage_log:
            for log in reversed(st.session_state.backstage_log[-10:]):  # Últimos 10
                icon = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}.get(log["type"], "📝")
                
                st.markdown(f"""
                <div class="backstage-panel">
                    <small><strong>{log['formatted_time']}</strong></small><br>
                    {icon} {log['message']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("*Nenhum evento registrado ainda...*")
    
    # Protocolo A2A Info
    st.markdown("#### 🔗 **Protocolo A2A**")
    st.markdown(f"""
    <div class="backstage-panel">
        <strong>Mensagens trocadas:</strong> {len(debate_system.message_log)}<br>
        <strong>Agentes ativos:</strong> {system_status['agents_loaded']}<br>
        <strong>Status:</strong> {'🟢 ATIVO' if st.session_state.debate_active else '🟡 AGUARDANDO'}
    </div>
    """, unsafe_allow_html=True)

# --- Controles Finais ---
st.markdown("---")
col_reset, col_export, col_status = st.columns(3)

with col_reset:
    if st.button("🔄 **Reiniciar Sistema**", help="Reset completo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with col_export:
    if st.session_state.debate_messages:
        transcript_lines = []
        for msg in st.session_state.debate_messages:
            timestamp = datetime.fromtimestamp(msg["timestamp"]).strftime('%H:%M:%S')
            transcript_lines.append(f"**{msg['agent']}** ({timestamp})\n{msg['message']}")
        
        transcript = "\n\n".join(transcript_lines)
        st.download_button(
            "📥 **Exportar Debate**",
            transcript,
            file_name=f"debate_flaflu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

with col_status:
    if st.button("📊 **Status Completo**", help="Informações detalhadas"):
        if st.session_state.agents_initialized:
            status = get_system_status()
            st.json(status)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; opacity: 0.8;">
    <h4>🤖 Sistema Multi-Agente A2A + Google ADK</h4>
    <p><strong>4 Agentes Independentes:</strong> Supervisor, Flamengo, Fluminense, Pesquisador</p>
    <p><small>Protocolo A2A v1.0 | Powered by Google Gemini AI | Built with Streamlit</small></p>
</div>
""", unsafe_allow_html=True)