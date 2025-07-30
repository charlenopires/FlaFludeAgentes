"""
Interface Streamlit para Sistema ADK + A2A v1.0
4 Agentes Independentes seguindo padrões Google ADK
"""

import streamlit as st
import asyncio
import time
import json
import html
from datetime import datetime
from typing import Dict, Any, List

# Importa sistema A2A
from a2a_system import get_a2a_system, get_system_status, get_agent_discovery

# --- Configuração da Página ---
st.set_page_config(
    page_title="🚀 ADK + A2A: Fla-Flu Debate System",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Estilos CSS Avançados ---
st.markdown("""
<style>
    /* Tema principal ADK */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a365d 50%, #744210 100%);
        color: #ffffff;
    }
    
    /* Header ADK */
    .adk-header {
        background: linear-gradient(90deg, #4285F4 0%, #34A853 25%, #FBBC04 50%, #EA4335 75%, #9C27B0 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Agent cards ADK style */
    .agent-card-adk {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .agent-card-adk:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .agent-card-adk::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4285F4, #34A853, #FBBC04, #EA4335);
        border-radius: 15px 15px 0 0;
    }
    
    /* A2A Protocol indicators */
    .a2a-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .adk-badge {
        display: inline-block;
        background: linear-gradient(45deg, #4285F4, #34A853);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 2px 10px rgba(66, 133, 244, 0.3);
    }
    
    /* Status indicators */
    .status-active { color: #4CAF50; font-weight: bold; text-shadow: 0 0 10px #4CAF50; }
    .status-waiting { color: #FF9800; font-weight: bold; text-shadow: 0 0 10px #FF9800; }
    .status-speaking { color: #2196F3; font-weight: bold; text-shadow: 0 0 10px #2196F3; }
    .status-researching { color: #9C27B0; font-weight: bold; text-shadow: 0 0 10px #9C27B0; }
    .status-finished { color: #F44336; font-weight: bold; text-shadow: 0 0 10px #F44336; }
    
    /* Chat messages ADK style */
    .chat-message-adk {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid;
        backdrop-filter: blur(8px);
        position: relative;
    }
    
    .supervisor-msg-adk { border-left-color: #FBBC04; background: rgba(251, 188, 4, 0.1); }
    .flamengo-msg-adk { border-left-color: #EA4335; background: rgba(234, 67, 53, 0.1); }
    .fluminense-msg-adk { border-left-color: #34A853; background: rgba(52, 168, 83, 0.1); }
    .researcher-msg-adk { border-left-color: #4285F4; background: rgba(66, 133, 244, 0.1); }
    
    /* A2A Communication logs */
    .a2a-log {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(102, 126, 234, 0.3);
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    
    /* Protocol status */
    .protocol-status {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Timer ADK */
    .timer-adk {
        font-family: 'Courier New', monospace;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        padding: 15px;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid rgba(66, 133, 244, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- Funções Auxiliares ---
def init_session_state():
    """Inicializa estado da sessão"""
    if 'debate_messages' not in st.session_state:
        st.session_state.debate_messages = []
    if 'a2a_log' not in st.session_state:
        st.session_state.a2a_log = []
    if 'debate_active' not in st.session_state:
        st.session_state.debate_active = False
    if 'debate_finished' not in st.session_state:
        st.session_state.debate_finished = False
    if 'current_turn' not in st.session_state:
        st.session_state.current_turn = None
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False
    if 'debate_start_time' not in st.session_state:
        st.session_state.debate_start_time = None
    if 'debate_duration_seconds' not in st.session_state:
        st.session_state.debate_duration_seconds = 0

def add_message(agent_name: str, message: str, message_type: str = "normal"):
    """Adiciona mensagem ao debate"""
    st.session_state.debate_messages.append({
        "agent": agent_name,
        "message": message,
        "timestamp": time.time(),
        "type": message_type
    })

def add_a2a_log(log_message: str, log_type: str = "info"):
    """Adiciona log A2A"""
    st.session_state.a2a_log.append({
        "message": log_message,
        "type": log_type,
        "timestamp": time.time(),
        "formatted_time": datetime.now().strftime("%H:%M:%S.%f")[:-3]
    })

def format_time(seconds: int) -> str:
    """Formata tempo em MM:SS"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def get_debate_time_info() -> Dict[str, Any]:
    """Retorna informações sobre o tempo do debate"""
    if not st.session_state.debate_start_time or not st.session_state.debate_active:
        return {
            "elapsed": 0,
            "remaining": 0,
            "total": 0,
            "status": "not_started"
        }
    
    current_time = time.time()
    elapsed = int(current_time - st.session_state.debate_start_time)
    total = st.session_state.debate_duration_seconds
    remaining = max(0, total - elapsed)
    
    status = "active"
    if remaining == 0:
        status = "finished"
    elif remaining <= 30:
        status = "ending"
    
    return {
        "elapsed": elapsed,
        "remaining": remaining,
        "total": total,
        "status": status
    }

def get_agent_emoji(agent_name: str) -> str:
    """Retorna emoji do agente"""
    emojis = {
        "supervisor": "⚖️",
        "flamengo": "🔴",
        "fluminense": "🟢", 
        "researcher": "📊"
    }
    return emojis.get(agent_name.lower(), "🤖")

def get_message_class(agent_name: str) -> str:
    """Retorna classe CSS da mensagem"""
    classes = {
        "supervisor": "supervisor-msg-adk",
        "flamengo": "flamengo-msg-adk",
        "fluminense": "fluminense-msg-adk",
        "researcher": "researcher-msg-adk"
    }
    return classes.get(agent_name.lower(), "chat-message-adk")

def clean_message_text(message: str) -> str:
    """Limpa e sanitiza texto da mensagem"""
    # Remove possíveis tags HTML existentes
    import re
    
    # Remove tags HTML
    cleaned = re.sub(r'<[^>]+>', '', message)
    
    # Escape HTML characters
    cleaned = html.escape(cleaned)
    
    # Converte quebras de linha para <br>
    cleaned = cleaned.replace('\n', '<br>').replace('\r', '')
    
    # Remove múltiplas quebras de linha consecutivas
    cleaned = re.sub(r'(<br>\s*){3,}', '<br><br>', cleaned)
    
    return cleaned.strip()

# --- Inicialização ---
init_session_state()

# --- Header Principal ADK ---
st.markdown("""
<div class="adk-header">
    <h1>🚀 GOOGLE ADK + A2A PROTOCOL DEBATE SYSTEM</h1>
    <p><strong>4 Agentes Independentes • Protocolo A2A v1.0 • Google ADK Compatible</strong></p>
    <div>
        <span class="adk-badge">Google ADK</span>
        <span class="a2a-badge">A2A v1.0</span>
        <span class="adk-badge">JSON-RPC 2.0</span>
        <span class="a2a-badge">Multi-Agent</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Layout Principal ---
col1, col2 = st.columns([2, 1])

with col1:
    # --- Área de Debate Principal ---
    st.markdown("### 💬 **Debate em Tempo Real via A2A**")
    
    # --- Cronômetro ---
    if st.session_state.debate_active:
        time_info = get_debate_time_info()
        progress = (time_info["elapsed"] / time_info["total"]) if time_info["total"] > 0 else 0
        
        # Cores baseadas no status
        if time_info["status"] == "ending":
            timer_color = "#F44336"  # Vermelho
            status_text = "⚠️ FINALIZANDO"
        elif time_info["status"] == "finished":
            timer_color = "#757575"  # Cinza
            status_text = "✅ CONCLUÍDO"
        else:
            timer_color = "#4CAF50"  # Verde
            status_text = "🟢 ATIVO"
        
        st.markdown(f"""
        <div class="timer-adk" style="background: rgba(0,0,0,0.6); border: 2px solid {timer_color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 1.2em; color: {timer_color};">{status_text}</div>
                <div style="font-size: 0.9em; opacity: 0.8;">
                    Turno: <strong>{st.session_state.current_turn.title() if st.session_state.current_turn else 'N/A'}</strong>
                </div>
            </div>
            <div style="font-size: 3em; color: {timer_color}; text-align: center; font-weight: bold; font-family: 'Courier New', monospace;">
                {format_time(time_info["remaining"])}
            </div>
            <div style="margin-top: 10px;">
                <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 8px;">
                    <div style="background: {timer_color}; width: {progress*100:.0f}%; height: 100%; border-radius: 10px; transition: width 0.3s;"></div>
                </div>
            </div>
            <div style="text-align: center; margin-top: 8px; font-size: 0.9em; opacity: 0.7;">
                Decorrido: {format_time(time_info["elapsed"])} / Total: {format_time(time_info["total"])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-refresh a cada segundo se debate ativo (usar com cuidado)
        if time_info["status"] == "active" and time_info["remaining"] > 0:
            placeholder = st.empty()
            placeholder.markdown("*Cronômetro atualizado automaticamente*", help="O cronômetro é atualizado conforme interações")
    
    chat_container = st.container()
    
    if not st.session_state.system_initialized:
        st.markdown("### 🎯 **Sistema Multi-Agente ADK + A2A**")
        
        st.markdown("""
        **🤖 4 Agentes Independentes seguindo Google ADK:**
        
        - **⚖️ Supervisor**: Coordenador especialista em retórica, psicologia e linguística
        - **🔴 Flamengo**: Torcedor apaixonado com argumentação demolidora  
        - **🟢 Fluminense**: Defensor elegante da tradição tricolor
        - **📊 Pesquisador**: Especialista neutro em dados objetivos
        
        **🔗 Protocolo A2A v1.0:**
        - Comunicação via JSON-RPC 2.0 sobre HTTP(S)
        - Agent Cards para descoberta de capacidades
        - Skills especializadas por agente
        - Comunicação assíncrona e streaming
        - Autenticação e segurança
        
        **📋 Fluxo de Comunicação:**
        1. Supervisor recebe duração do usuário via A2A
        2. Sistema distribui tempo 50/50 entre times
        3. Agentes comunicam via protocolo A2A
        4. Pesquisador responde solicitações via A2A
        5. Supervisor analisa e declara vencedor
        """)
        
        if st.button("🚀 **Inicializar Sistema ADK + A2A**", key="init_system"):
            with st.spinner("🤖 Carregando sistema ADK + A2A..."):
                try:
                    # Inicializa sistema A2A
                    a2a_system = get_a2a_system()
                    
                    st.session_state.system_initialized = True
                    add_a2a_log("Sistema A2A inicializado com sucesso", "success")
                    add_a2a_log("4 agentes carregados seguindo padrões ADK", "info")
                    add_a2a_log("Protocolo A2A v1.0 ativo", "info")
                    
                    # Supervisor se apresenta
                    supervisor_intro = """⚖️ **SISTEMA ADK + A2A ATIVADO**

🎯 **Google Agent Development Kit Inicializado:**
- Supervisor especialista em retórica, psicologia e linguística
- Protocolo A2A v1.0 para comunicação entre agentes
- JSON-RPC 2.0 como formato de payload
- Agent Cards para descoberta de capacidades

📊 **Agentes Conectados via A2A:**
- 🔴 **Flamengo Agent**: Skills de argumentação persuasiva
- 🟢 **Fluminense Agent**: Skills de argumentação elegante  
- 📊 **Researcher Agent**: Skills de pesquisa objetiva
- ⚖️ **Supervisor Agent**: Skills de coordenação e análise

🚀 **Sistema Pronto!** Por favor, configure a duração do debate para iniciarmos 
a comunicação A2A entre os agentes especializados."""
                    
                    add_message("Supervisor ADK", supervisor_intro, "system")
                    add_a2a_log("Supervisor ADK apresentou sistema", "info")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao inicializar sistema ADK: {str(e)}")
                    add_a2a_log(f"Erro na inicialização: {str(e)}", "error")
    
    else:
        # Exibe mensagens do debate
        with chat_container:
            for msg in st.session_state.debate_messages:
                agent_lower = msg["agent"].replace(" ADK", "").lower()
                emoji = get_agent_emoji(agent_lower)
                css_class = get_message_class(agent_lower)
                timestamp = datetime.fromtimestamp(msg["timestamp"]).strftime("%H:%M:%S")
                
                # Tratamento especial para diferentes tipos de agentes
                if "pesquisador" in agent_lower:
                    # UI especial para pesquisador
                    st.markdown(f"""
                    <div class="chat-message-adk {css_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <strong>{emoji} {html.escape(msg["agent"])}</strong>
                            <div>
                                <span class="a2a-badge">A2A</span>
                                <span style="background: linear-gradient(45deg, #4285F4, #9C27B0); padding: 2px 8px; border-radius: 10px; font-size: 0.7em; color: white; margin-left: 5px;">📊 DADOS</span>
                                <small style="opacity: 0.7; margin-left: 8px;">⏰ {timestamp}</small>
                            </div>
                        </div>
                        <div style="background: rgba(66, 133, 244, 0.1); border-left: 4px solid #4285F4; padding: 15px; margin-top: 10px; border-radius: 0 8px 8px 0; font-family: monospace; font-size: 0.9em;">
                            {clean_message_text(msg["message"])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # UI normal para outros agentes
                    st.markdown(f"""
                    <div class="chat-message-adk {css_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <strong>{emoji} {html.escape(msg["agent"])}</strong>
                            <div>
                                <span class="a2a-badge">A2A</span>
                                <small style="opacity: 0.7;">⏰ {timestamp}</small>
                            </div>
                        </div>
                        <div style="margin-top: 10px; line-height: 1.6;">
                            {clean_message_text(msg["message"])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # --- Controles do Debate ---
        if not st.session_state.debate_active and not st.session_state.debate_finished:
            st.markdown("### ⚙️ **Configuração do Debate A2A**")
            
            col_duration, col_start = st.columns([1, 1])
            
            with col_duration:
                debate_duration = st.slider(
                    "⏱️ Duração do debate (minutos):",
                    min_value=1, max_value=10, value=5, step=1,
                    help="Tempo será gerenciado pelo Supervisor via protocolo A2A"
                )
            
            with col_start:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🎬 **INICIAR DEBATE A2A**", key="start_debate", use_container_width=True):
                    with st.spinner("⚖️ Sistema A2A iniciando debate..."):
                        try:
                            a2a_system = get_a2a_system()
                            
                            add_a2a_log(f"Iniciando debate via A2A: {debate_duration} min", "info")
                            
                            # Função auxiliar para executar asyncio
                            async def start_debate_async():
                                return await a2a_system.start_debate(debate_duration)
                            
                            # Executa função assíncrona
                            result = asyncio.run(start_debate_async())
                            
                            if result["status"] == "success":
                                st.session_state.debate_active = True
                                st.session_state.current_turn = result["current_turn"]
                                
                                # Configura cronômetro
                                st.session_state.debate_start_time = time.time()
                                st.session_state.debate_duration_seconds = debate_duration * 60
                                
                                # Mensagem do supervisor
                                supervisor_msg = result["supervisor_response"].get("message", "")
                                if supervisor_msg:
                                    add_message("Supervisor ADK", supervisor_msg, "system")
                                
                                add_a2a_log("Debate iniciado com sucesso via A2A", "success")
                                add_a2a_log(f"Flamengo inicia (protocolo A2A)", "info")
                                
                                # Primeiro argumento do Flamengo
                                async def get_flamengo_arg():
                                    flamengo_agent = a2a_system.agents["flamengo"]
                                    return await flamengo_agent.generate_initial_argument()
                                
                                initial_arg = asyncio.run(get_flamengo_arg())
                                add_message("Flamengo ADK", initial_arg, "argument")
                                add_a2a_log("Flamengo apresentou argumento inicial", "success")
                                
                                st.session_state.current_turn = "fluminense"
                                st.success("✅ Debate iniciado com sucesso!")
                                
                            else:
                                st.error(f"❌ Erro: {result['message']}")
                                add_a2a_log(f"Erro no início: {result['message']}", "error")
                        
                        except Exception as e:
                            st.error(f"❌ Erro no sistema A2A: {str(e)}")
                            add_a2a_log(f"Erro crítico: {str(e)}", "error")
                        
                        st.rerun()
        
        # --- Debate Ativo ---
        elif st.session_state.debate_active and not st.session_state.debate_finished:
            
            # Simula continuação do debate
            if st.button("▶️ **Próximo Turno A2A**", key="next_turn"):
                with st.spinner(f"🤔 {st.session_state.current_turn.title()} via A2A..."):
                    try:
                        a2a_system = get_a2a_system()
                        current_agent = st.session_state.current_turn
                        
                        add_a2a_log(f"Processando turno: {current_agent}", "info")
                        
                        # Busca último argumento do oponente
                        if current_agent == "fluminense":
                            opponent_messages = [m for m in st.session_state.debate_messages 
                                               if "flamengo" in m["agent"].lower()]
                        else:
                            opponent_messages = [m for m in st.session_state.debate_messages 
                                               if "fluminense" in m["agent"].lower()]
                        last_opponent = opponent_messages[-1]["message"] if opponent_messages else ""
                        
                        # Função async para processar turno
                        async def process_turn():
                            return await a2a_system.process_turn(current_agent, last_opponent)
                        
                        turn_result = asyncio.run(process_turn())
                        
                        if turn_result["status"] == "success":
                            # Gera resposta do agente atual
                            agent = a2a_system.agents[current_agent]
                            
                            if current_agent == "fluminense":
                                async def get_response():
                                    return await agent.generate_counter_argument(last_opponent)
                                response = asyncio.run(get_response())
                                add_message("Fluminense ADK", response, "argument")
                            elif current_agent == "flamengo":
                                async def get_response():
                                    return await agent.generate_counter_argument(last_opponent)
                                response = asyncio.run(get_response())
                                add_message("Flamengo ADK", response, "argument")
                            
                            add_a2a_log(f"{current_agent.title()} argumentou via A2A", "success")
                            
                            # Atualiza turno
                            st.session_state.current_turn = turn_result["next_agent"]
                            
                            # Verifica se deve finalizar (simples contador)
                            if len(st.session_state.debate_messages) >= 6:  # 3 rodadas
                                st.session_state.debate_finished = True
                                st.session_state.debate_active = False
                                
                                # Análise final
                                async def finish_debate():
                                    return await a2a_system.finish_debate(st.session_state.debate_messages)
                                
                                analysis_result = asyncio.run(finish_debate())
                                if analysis_result["status"] == "success":
                                    analysis_msg = analysis_result["analysis"].get("analysis", "Análise concluída")
                                    add_message("Supervisor ADK", analysis_msg, "final")
                                    add_a2a_log("Análise final concluída via A2A", "success")
                            
                            st.success(f"✅ {current_agent.title()} argumentou com sucesso!")
                        
                        else:
                            add_a2a_log(f"Erro no turno: {turn_result['message']}", "error")
                            st.error(f"❌ Erro no turno: {turn_result['message']}")
                    
                    except Exception as e:
                        add_a2a_log(f"Erro no turno: {str(e)}", "error")
                        st.error(f"❌ Erro no turno: {str(e)}")
                
                st.rerun()

with col2:
    # --- Painel ADK + A2A ---
    st.markdown("### 🎭 **ADK Agent Status**")
    
    # Status dos agentes ADK
    try:
        system_status = get_system_status()
        agent_discovery = get_agent_discovery()
        
        st.markdown("#### 🤖 **Agent Cards (ADK)**")
        
        for agent_name, agent_info in agent_discovery["agents"].items():
            agent_card = agent_info["agent_card"]
            status = agent_info["status"]
            
            emoji = get_agent_emoji(agent_name)
            
            status_class = "status-active" if status == "active" else "status-waiting"
            status_text = "ATIVO" if status == "active" else "STANDBY"
            
            if st.session_state.debate_active and agent_name == st.session_state.current_turn:
                status_class = "status-speaking"
                status_text = "ARGUMENTANDO"
            
            st.markdown(f"""
            <div class="agent-card-adk">
                <strong>{emoji} {agent_card['name']}</strong><br>
                <small>{agent_card['description'][:60]}...</small><br>
                <span class="adk-badge">ADK v{agent_card['version']}</span><br>
                <span class="{status_class}">{status_text}</span><br>
                <small><strong>Skills:</strong> {len(agent_card['skills'])}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Protocolo A2A Status
        st.markdown("#### 🔗 **Protocolo A2A Status**")
        a2a_status = system_status["a2a_communications"]
        
        st.markdown(f"""
        <div class="protocol-status">
            <strong>📊 Comunicações A2A:</strong><br>
            • Total de mensagens: {a2a_status["total_messages"]}<br>
            • Conversas ativas: {a2a_status["active_conversations"]}<br>
            • Protocolo: {system_status["system"]["protocol"]}<br>
            • Status: {'🟢 ATIVO' if system_status["system"]["active"] else '🔴 INATIVO'}
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar status: {str(e)}")
    
    # Log A2A
    st.markdown("#### 📋 **Log A2A Protocol**")
    
    log_container = st.container()
    with log_container:
        if st.session_state.a2a_log:
            for log in reversed(st.session_state.a2a_log[-8:]):  # Últimos 8
                icon = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}.get(log["type"], "📝")
                
                st.markdown(f"""
                <div class="a2a-log">
                    <small><strong>{log['formatted_time']}</strong></small><br>
                    {icon} {log['message']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("*Aguardando eventos A2A...*")

# --- Controles Finais ---
st.markdown("---")
col_reset, col_discovery, col_export = st.columns(3)

with col_reset:
    if st.button("🔄 **Reset Sistema ADK**", help="Reset completo do sistema"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with col_discovery:
    if st.button("🔍 **Agent Discovery**", help="Mostra Agent Cards ADK"):
        if st.session_state.system_initialized:
            try:
                discovery = get_agent_discovery()
                st.json(discovery)
            except Exception as e:
                st.error(f"Erro: {str(e)}")

with col_export:
    if st.session_state.debate_messages:
        transcript_lines = []
        for msg in st.session_state.debate_messages:
            timestamp = datetime.fromtimestamp(msg["timestamp"]).strftime('%H:%M:%S')
            transcript_lines.append(f"**{msg['agent']}** ({timestamp})\n{msg['message']}")
        
        transcript = "\n\n".join(transcript_lines)
        st.download_button(
            "📥 **Export A2A Debate**",
            transcript,
            file_name=f"debate_adk_a2a_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

# --- Footer ADK ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 25px; opacity: 0.9;">
    <h4>🚀 Google ADK + A2A Protocol v1.0</h4>
    <p><strong>4 Agentes Independentes:</strong> Supervisor, Flamengo, Fluminense, Pesquisador</p>
    <div style="margin: 15px 0;">
        <span class="adk-badge">Google ADK Compatible</span>
        <span class="a2a-badge">A2A Protocol v1.0</span>
        <span class="adk-badge">JSON-RPC 2.0</span>
        <span class="a2a-badge">Multi-Agent System</span>
    </div>
    <p><small>Agent Cards • Skills • Streaming • Push Notifications • State History</small></p>
    <p><small>Powered by Google Gemini AI | Built with Streamlit</small></p>
</div>
""", unsafe_allow_html=True)