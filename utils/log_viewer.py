"""
Componente de Visualização de Logs para Streamlit
Interface avançada para monitoramento em tempo real dos agentes
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json

# Importações opcionais para gráficos
try:
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly não instalado. Gráficos não estarão disponíveis. Execute: `uv add plotly pandas`")

from .enhanced_logger import enhanced_logger, LogLevel, LogCategory


class LogViewer:
    """Interface de visualização de logs no Streamlit"""
    
    def __init__(self):
        self.colors = {
            "supervisor": "#FFD700",
            "flamengo": "#DC143C", 
            "fluminense": "#008000",
            "researcher": "#4169E1",
            "system": "#708090"
        }
        
        self.level_colors = {
            "DEBUG": "#808080",
            "INFO": "#00CED1",
            "WARNING": "#FFA500", 
            "ERROR": "#FF4500",
            "CRITICAL": "#DC143C",
            "AGENT_ACTION": "#32CD32",
            "A2A_MESSAGE": "#9370DB",
            "SYSTEM_EVENT": "#20B2AA",
            "DEBATE_FLOW": "#FF6347"
        }
    
    def render_main_dashboard(self):
        """Renderiza o dashboard principal de logs"""
        st.markdown("### 📊 **Dashboard de Logs - Sistema A2A**")
        
        # Métricas de performance
        metrics = enhanced_logger.get_performance_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total de Eventos",
                metrics["total_events"],
                delta=f"+{metrics.get('recent_events', 0)} últimos"
            )
        
        with col2:
            st.metric(
                "Execuções de Agentes", 
                metrics["agent_executions"],
                delta=f"{metrics['avg_response_time']:.1f}ms média"
            )
        
        with col3:
            st.metric(
                "Mensagens A2A",
                metrics["a2a_messages"],
                delta=None
            )
        
        with col4:
            st.metric(
                "Erros",
                metrics["errors"],
                delta=None,
                delta_color="inverse"
            )
        
        # Filtros
        st.markdown("#### 🔍 **Filtros de Log**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_category = st.selectbox(
                "📂 Categoria:",
                ["Todas"] + [cat.value for cat in LogCategory],
                key="log_category_filter"
            )
            
        with col2:
            selected_agent = st.selectbox(
                "🤖 Agente:",
                ["Todos", "supervisor", "flamengo", "fluminense", "researcher"],
                key="log_agent_filter"
            )
        
        with col3:
            selected_level = st.selectbox(
                "⚡ Nível:",
                ["Todos"] + [level.value for level in LogLevel],
                key="log_level_filter"
            )
        
        # Aplicar filtros
        category_filter = None if selected_category == "Todas" else LogCategory(selected_category)
        agent_filter = None if selected_agent == "Todos" else selected_agent
        level_filter = None if selected_level == "Todos" else LogLevel(selected_level)
        
        # Buscar logs
        recent_logs = enhanced_logger.get_recent_logs(
            limit=100,
            category=category_filter,
            agent_name=agent_filter,
            level=level_filter
        )
        
        return recent_logs
    
    def render_log_timeline(self, logs: List[Dict[str, Any]]):
        """Renderiza timeline de eventos"""
        if not logs:
            st.warning("Nenhum log encontrado com os filtros aplicados")
            return
        
        st.markdown("#### ⏰ **Timeline de Eventos**")
        
        if not PLOTLY_AVAILABLE:
            # Versão simplificada sem gráficos
            st.markdown("**📊 Timeline Simplificada (Plotly não disponível):**")
            
            # Agrupa por horário
            timeline_data = {}
            for log in logs[-20:]:  # Últimos 20 eventos
                time_key = log['timestamp'][:16]  # YYYY-MM-DD HH:MM
                if time_key not in timeline_data:
                    timeline_data[time_key] = []
                timeline_data[time_key].append(log)
            
            for time_key in sorted(timeline_data.keys(), reverse=True):
                st.markdown(f"**🕓 {time_key}**")
                for log in timeline_data[time_key]:
                    agent_emoji = "🤖" if log.get('agent_name') else "⚙️"
                    st.markdown(f"  {agent_emoji} {log.get('agent_name', 'Sistema')}: {log['event_type']} - {log['level']}")
            return
        
        # Converte para DataFrame
        df = pd.DataFrame(logs)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Gráfico de timeline
        fig = px.scatter(
            df,
            x='timestamp',
            y='level',
            color='agent_name',
            size_max=15,
            hover_data=['event_type', 'message'],
            title="Timeline de Eventos dos Agentes",
            color_discrete_map=self.colors
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Timestamp",
            yaxis_title="Nível do Log",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_agent_activity(self, logs: List[Dict[str, Any]]):
        """Renderiza atividade por agente"""
        if not logs:
            return
        
        st.markdown("#### 🤖 **Atividade por Agente**")
        
        # Conta eventos por agente
        agent_counts = {}
        for log in logs:
            agent = log.get('agent_name') or 'system'
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        if agent_counts:
            if not PLOTLY_AVAILABLE:
                # Versão simplificada sem gráficos
                st.markdown("**📊 Estatísticas por Agente:**")
                
                # Ordena por quantidade de eventos
                sorted_agents = sorted(agent_counts.items(), key=lambda x: x[1], reverse=True)
                
                for agent, count in sorted_agents:
                    emoji = "🤖🔴" if agent == "flamengo" else "🤖🟢" if agent == "fluminense" else "🤖⚖️" if agent == "supervisor" else "🤖📈" if agent == "researcher" else "⚙️"
                    percentage = (count / sum(agent_counts.values())) * 100
                    st.markdown(f"  {emoji} **{agent.title()}**: {count} eventos ({percentage:.1f}%)")
                return
            
            # Gráfico de barras
            agents = list(agent_counts.keys())
            counts = list(agent_counts.values())
            
            fig = go.Figure(data=[
                go.Bar(
                    x=agents,
                    y=counts,
                    marker_color=[self.colors.get(agent, '#708090') for agent in agents],
                    text=counts,
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Eventos por Agente",
                xaxis_title="Agentes",
                yaxis_title="Número de Eventos",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_performance_chart(self, logs: List[Dict[str, Any]]):
        """Renderiza gráfico de performance"""
        if not logs:
            return
        
        st.markdown("#### ⚡ **Análise de Performance**")
        
        # Filtra logs com duration_ms
        perf_logs = [log for log in logs if log.get('duration_ms')]
        
        if perf_logs:
            if not PLOTLY_AVAILABLE:
                # Versão simplificada - apenas estatísticas
                durations = [log['duration_ms'] for log in perf_logs]
                agents_perf = {}
                
                for log in perf_logs:
                    agent = log.get('agent_name', 'system')
                    if agent not in agents_perf:
                        agents_perf[agent] = []
                    agents_perf[agent].append(log['duration_ms'])
                
                # Estatísticas gerais
                avg_duration = sum(durations) / len(durations)
                max_duration = max(durations)
                min_duration = min(durations)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("⏱️ Tempo Médio", f"{avg_duration:.1f}ms")
                
                with col2:
                    st.metric("🏃 Mais Lento", f"{max_duration:.1f}ms")
                
                with col3:
                    st.metric("⚡ Mais Rápido", f"{min_duration:.1f}ms")
                
                # Performance por agente
                st.markdown("**📊 Performance por Agente:**")
                for agent, times in agents_perf.items():
                    avg_time = sum(times) / len(times)
                    emoji = "🤖🔴" if agent == "flamengo" else "🤖🟢" if agent == "fluminense" else "🤖⚖️" if agent == "supervisor" else "🤖📈" if agent == "researcher" else "⚙️"
                    st.markdown(f"  {emoji} **{agent.title()}**: {avg_time:.1f}ms médio ({len(times)} execuções)")
                
                return
            
            df = pd.DataFrame(perf_logs)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Gráfico de linha para tempo de resposta
            fig = px.line(
                df.sort_values('timestamp'),
                x='timestamp',
                y='duration_ms',
                color='agent_name',
                title="Tempo de Resposta dos Agentes",
                color_discrete_map=self.colors
            )
            
            fig.update_layout(
                height=300,
                xaxis_title="Timestamp",
                yaxis_title="Duração (ms)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Estatísticas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_duration = df['duration_ms'].mean()
                st.metric("⏱️ Tempo Médio", f"{avg_duration:.1f}ms")
            
            with col2:
                max_duration = df['duration_ms'].max()
                st.metric("🏃 Mais Lento", f"{max_duration:.1f}ms")
            
            with col3:
                min_duration = df['duration_ms'].min()
                st.metric("⚡ Mais Rápido", f"{min_duration:.1f}ms")
    
    def render_detailed_logs(self, logs: List[Dict[str, Any]], limit: int = 20):
        """Renderiza lista detalhada de logs"""
        st.markdown("#### 📋 **Logs Detalhados**")
        
        if not logs:
            st.info("Nenhum log para exibir")
            return
        
        # Controle de paginação
        total_logs = len(logs)
        page_size = limit
        max_pages = (total_logs - 1) // page_size + 1
        
        if max_pages > 1:
            page = st.slider("📄 Página:", 1, max_pages, 1, key="log_page_slider")
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, total_logs)
            displayed_logs = logs[start_idx:end_idx]
            
            st.info(f"Mostrando logs {start_idx + 1}-{end_idx} de {total_logs}")
        else:
            displayed_logs = logs[:limit]
        
        # Renderiza cada log
        for i, log in enumerate(displayed_logs):
            with st.expander(
                f"🕒 {log['timestamp'][:19]} | "
                f"{'🤖' if log.get('agent_name') else '⚙️'} "
                f"{log.get('agent_name', 'Sistema').title()} | "
                f"{log['level']} | "
                f"{log['event_type']}"
            ):
                # Informações básicas
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**📂 Categoria:** {log['category']}")
                    st.markdown(f"**⚡ Nível:** {log['level']}")
                    st.markdown(f"**🎯 Evento:** {log['event_type']}")
                
                with col2:
                    if log.get('agent_name'):
                        st.markdown(f"**🤖 Agente:** {log['agent_name']}")
                    if log.get('session_id'):
                        st.markdown(f"**🆔 Sessão:** {log['session_id']}")
                    if log.get('correlation_id'):
                        st.markdown(f"**🔗 Correlação:** {log['correlation_id']}")
                
                # Mensagem principal
                st.markdown("**💬 Mensagem:**")
                st.markdown(f"```\n{log['message']}\n```")
                
                # Detalhes técnicos
                if log.get('details'):
                    st.markdown("**🔧 Detalhes Técnicos:**")
                    st.json(log['details'])
                
                # Performance
                if log.get('duration_ms'):
                    st.markdown(f"**⏱️ Duração:** {log['duration_ms']:.2f}ms")
                
                # Thread info
                if log.get('thread_id'):
                    st.markdown(f"**🧵 Thread:** {log['thread_id']}")
    
    def render_search_interface(self):
        """Interface de busca nos logs"""
        st.markdown("#### 🔍 **Busca Avançada**")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "🔎 Buscar nos logs:",
                placeholder="Digite termos para buscar...",
                key="log_search_query"
            )
        
        with col2:
            search_limit = st.number_input(
                "📊 Máximo:",
                min_value=10,
                max_value=500,
                value=50,
                key="search_limit"
            )
        
        if search_query:
            search_results = enhanced_logger.search_logs(search_query, limit=search_limit)
            
            if search_results:
                st.success(f"✅ Encontrados {len(search_results)} resultados para '{search_query}'")
                self.render_detailed_logs(search_results, limit=10)
            else:
                st.warning(f"❌ Nenhum resultado encontrado para '{search_query}'")
    
    def render_export_interface(self):
        """Interface de exportação de logs"""
        st.markdown("#### 📥 **Exportar Logs**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            export_format = st.selectbox(
                "📄 Formato:",
                ["JSON", "CSV"],
                key="export_format"
            )
        
        with col2:
            hours_back = st.number_input(
                "🕒 Últimas horas:",
                min_value=1,
                max_value=168,  # 1 semana
                value=24,
                key="export_hours"
            )
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📥 Exportar", key="export_logs_btn"):
                end_time = datetime.now()
                start_time = end_time - timedelta(hours=hours_back)
                
                # Exporta logs
                exported_data = enhanced_logger.export_logs(
                    format=export_format.lower(),
                    time_range=(start_time.isoformat(), end_time.isoformat())
                )
                
                # Download
                filename = f"fla_flu_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}"
                st.download_button(
                    label=f"⬇️ Download {export_format}",
                    data=exported_data,
                    file_name=filename,
                    mime=f"application/{export_format.lower()}"
                )
    
    def render_correlation_tracker(self):
        """Interface para rastrear correlações"""
        st.markdown("#### 🔗 **Rastreamento de Correlação**")
        
        correlation_id = st.text_input(
            "🆔 ID de Correlação:",
            placeholder="Digite o ID de correlação...",
            key="correlation_tracker_id"
        )
        
        if correlation_id:
            # Busca logs com essa correlação
            flow_logs = enhanced_logger.get_agent_flow(
                session_id="", 
                correlation_id=correlation_id
            )
            
            if flow_logs:
                st.success(f"✅ Encontrados {len(flow_logs)} eventos para correlação {correlation_id}")
                
                # Timeline específica
                if len(flow_logs) > 1:
                    df = pd.DataFrame(flow_logs)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df = df.sort_values('timestamp')
                    
                    # Gráfico de fluxo
                    fig = px.line(
                        df,
                        x='timestamp',
                        y='agent_name',
                        title=f"Fluxo de Correlação: {correlation_id}",
                        markers=True
                    )
                    
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detalhes
                self.render_detailed_logs(flow_logs, limit=20)
            else:
                st.warning(f"❌ Nenhum evento encontrado para correlação {correlation_id}")


def render_log_dashboard():
    """Função principal para renderizar o dashboard de logs"""
    log_viewer = LogViewer()
    
    # Tabs de navegação
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard", 
        "🔍 Busca", 
        "🔗 Correlações", 
        "📥 Exportar"
    ])
    
    with tab1:
        recent_logs = log_viewer.render_main_dashboard()
        
        if recent_logs:
            # Visualizações
            col1, col2 = st.columns(2)
            
            with col1:
                log_viewer.render_agent_activity(recent_logs)
            
            with col2:
                log_viewer.render_performance_chart(recent_logs)
            
            # Timeline
            log_viewer.render_log_timeline(recent_logs)
            
            # Logs detalhados
            log_viewer.render_detailed_logs(recent_logs)
    
    with tab2:
        log_viewer.render_search_interface()
    
    with tab3:
        log_viewer.render_correlation_tracker()
    
    with tab4:
        log_viewer.render_export_interface()