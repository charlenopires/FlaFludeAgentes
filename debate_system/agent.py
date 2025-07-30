"""
Multi-Agent Football Debate System using Google ADK
Following official ADK patterns from adk-samples and quickstart
"""

from typing import Dict, Any, List
import json
import time
import random
from datetime import datetime

# --- Tools Following ADK Patterns ---

def get_team_statistics(team: str, query_type: str = "general") -> Dict[str, Any]:
    """
    Retrieves team statistics and historical data for debate support.
    
    Args:
        team: Team name (Flamengo or Fluminense)
        query_type: Type of data requested (titles, players, history, recent)
        
    Returns:
        dict: Contains 'status' and 'report' with team statistics
    """
    try:
        team_lower = team.lower()
        
        # Flamengo data
        flamengo_data = {
            "titles": {
                "brasileirao": "8 títulos (1980, 1982, 1983, 1987, 1992, 2009, 2019, 2020)",
                "libertadores": "3 títulos (1981, 2019, 2022)",
                "mundial": "1 título (1981)",
                "carioca": "Mais de 35 títulos estaduais"
            },
            "players": {
                "legends": "Zico, Júnior, Bebeto, Romário, Adriano",
                "current": "Pedro, Gabigol, Arrascaeta, De la Cruz",
                "exports": "Vinícius Jr. (Real Madrid), Lucas Paquetá (West Ham)"
            },
            "history": {
                "founded": "Fundado em 1895",
                "nickname": "Mengão, Clube de Regatas do Flamengo",
                "fanbase": "Maior torcida do Brasil com 40+ milhões",
                "stadium": "Maracanã (estádio próprio em construção)"
            },
            "recent": {
                "achievements": "Bicampeão brasileiro (2019-2020)",
                "performance": "Sempre entre os primeiros colocados",
                "investments": "Contratações de alto nível constantemente"
            }
        }
        
        # Fluminense data
        fluminense_data = {
            "titles": {
                "brasileirao": "4 títulos (1970, 1984, 2010, 2012)",
                "libertadores": "1 título (2023 - ATUAL CAMPEÃO)",
                "carioca": "Mais de 30 títulos estaduais",
                "others": "Diversos títulos nacionais e internacionais"
            },
            "players": {
                "legends": "Didi, Carlos Alberto Torres, Rivellino, Fred",
                "current": "Germán Cano, Paulo Henrique Ganso, Jhon Arias",
                "academy": "Uma das melhores categorias de base do Brasil"
            },
            "history": {
                "founded": "Fundado em 1902 - mais antigo do Rio",
                "nickname": "Tricolor, Flu, Time de Guerreiros",
                "tradition": "Clube mais tradicional do futebol carioca",
                "stadium": "Maracanã e Laranjeiras"
            },
            "recent": {
                "achievements": "CAMPEÃO DA LIBERTADORES 2023",
                "performance": "Crescimento consistente nos últimos anos",
                "recognition": "Reconhecimento internacional recente"
            }
        }
        
        # Select team data
        if "flamengo" in team_lower or "fla" in team_lower:
            data = flamengo_data
            team_name = "Flamengo"
        elif "fluminense" in team_lower or "flu" in team_lower:
            data = fluminense_data  
            team_name = "Fluminense"
        else:
            return {
                "status": "error",
                "error_message": f"Time '{team}' não reconhecido. Use 'Flamengo' ou 'Fluminense'."
            }
        
        # Format response based on query type
        if query_type in data:
            result_data = data[query_type]
            report = f"📊 Dados sobre {team_name} - {query_type.title()}:\n\n"
            for key, value in result_data.items():
                report += f"• {key.title()}: {value}\n"
        else:
            # Return all data
            report = f"📊 Informações Completas - {team_name}:\n\n"
            for category, items in data.items():
                report += f"🏆 {category.upper()}:\n"
                for key, value in items.items():
                    report += f"  • {key.title()}: {value}\n"
                report += "\n"
        
        return {
            "status": "success",
            "report": report.strip()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Erro ao buscar estatísticas: {str(e)}"
        }

def analyze_argument_strength(argument: str, team_context: str = "") -> Dict[str, Any]:
    """
    Analyzes the rhetorical strength and persuasive power of an argument.
    
    Args:
        argument: The argument text to analyze
        team_context: Team context for the argument
        
    Returns:
        dict: Contains 'status' and 'report' with argument analysis
    """
    try:
        if not argument or len(argument.strip()) < 10:
            return {
                "status": "error",
                "error_message": "Argumento muito curto para análise adequada"
            }
        
        # Analyze argument characteristics
        word_count = len(argument.split())
        emotional_words = ["paixão", "amor", "coração", "alma", "sangue", "vida", "emoção"]
        factual_indicators = ["título", "campeão", "dados", "estatística", "números", "história"]
        
        emotional_score = sum(1 for word in emotional_words if word in argument.lower())
        factual_score = sum(1 for word in factual_indicators if word in argument.lower())
        
        # Calculate strength metrics
        length_score = min(word_count / 50, 1.0)  # Normalized to max 1.0
        emotional_strength = min(emotional_score / 3, 1.0)  # Max 1.0
        factual_strength = min(factual_score / 3, 1.0)  # Max 1.0
        
        overall_strength = (length_score + emotional_strength + factual_strength) / 3
        
        # Generate analysis report
        strength_level = "FORTE" if overall_strength > 0.7 else "MODERADO" if overall_strength > 0.4 else "FRACO"
        
        analysis = f"""
🔍 ANÁLISE DE FORÇA ARGUMENTATIVA:

📏 MÉTRICAS BÁSICAS:
• Palavras: {word_count}
• Contexto: {team_context or "Geral"}

💪 FORÇA GERAL: {strength_level} ({overall_strength:.1%})

📊 COMPONENTES:
• Estrutura e Extensão: {length_score:.1%}
• Apelo Emocional: {emotional_strength:.1%} ({emotional_score} indicadores)
• Base Factual: {factual_strength:.1%} ({factual_score} indicadores)

🎯 RECOMENDAÇÕES:
{"• Excelente equilíbrio entre emoção e fatos!" if overall_strength > 0.7 else "• Considere adicionar mais dados ou apelo emocional" if overall_strength > 0.4 else "• Argumento precisa ser fortalecido significativamente"}

⚡ IMPACTO PERSUASIVO: {"ALTO - Argumento convincente" if overall_strength > 0.6 else "MÉDIO - Pode ser melhorado" if overall_strength > 0.3 else "BAIXO - Necessita reformulação"}
        """
        
        return {
            "status": "success",
            "report": analysis.strip()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Erro na análise: {str(e)}"
        }

def generate_counter_argument(original_argument: str, opposing_team: str) -> Dict[str, Any]:
    """
    Generates counter-arguments against opposing team's points.
    
    Args:
        original_argument: The argument to counter
        opposing_team: The team making the original argument
        
    Returns:
        dict: Contains 'status' and 'report' with counter-argument
    """
    try:
        if not original_argument:
            return {
                "status": "error", 
                "error_message": "Argumento original necessário para contra-argumentação"
            }
        
        team_lower = opposing_team.lower()
        
        # Counter-argument strategies based on opposing team
        if "flamengo" in team_lower:
            # Countering Flamengo arguments
            counter_strategies = {
                "popularity": "Quantidade não significa qualidade! Fluminense tem torcida mais refinada e leal.",
                "recent_titles": "Títulos recentes são temporários. Fluminense tem TRADIÇÃO centenária!",
                "players": "Flamengo compra jogadores, Fluminense FORMA craques! Nossa base é superior.",
                "investment": "Dinheiro não compra história nem elegância no futebol.",
                "general": "Flamengo pode ter números, mas Fluminense tem CLASSE e TRADIÇÃO!"
            }
            defending_team = "Fluminense"
            defending_colors = "🟢✨"
            
        elif "fluminense" in team_lower:
            # Countering Fluminense arguments  
            counter_strategies = {
                "tradition": "Tradição sem títulos recentes é passado morto! Flamengo é PRESENTE e FUTURO!",
                "elegance": "Futebol-arte não ganha jogos, GARRA e PAIXÃO sim! Somos a NAÇÃO!",
                "libertadores": "Um título isolado não faz história. Flamengo tem 3 Libertadores!",
                "history": "História bonita, mas Flamengo tem a história VENCEDORA dos últimos tempos!",
                "general": "Fluminense pode ter classe, mas Flamengo tem FORÇA e CONQUISTAS!"
            }
            defending_team = "Flamengo"
            defending_colors = "🔴⚡"
            
        else:
            return {
                "status": "error",
                "error_message": f"Time oponente '{opposing_team}' não reconhecido"
            }
        
        # Select counter strategy based on argument content
        selected_strategy = counter_strategies["general"]  # Default
        
        for key, strategy in counter_strategies.items():
            if key in original_argument.lower():
                selected_strategy = strategy
                break
        
        # Build counter-argument
        counter_argument = f"""
{defending_colors} CONTRA-ATAQUE {defending_team.upper()}! {defending_colors}

🛡️ RESPOSTA AO ARGUMENTO RIVAL:
"{original_argument[:100]}{'...' if len(original_argument) > 100 else ''}"

⚔️ NOSSA TRÉPLICA:
{selected_strategy}

💥 E MAIS:
• Enquanto vocês falam, nós CONQUISTAMOS!
• {defending_team} não precisa se provar, já É o melhor!
• A verdade dói, mas é isso: somos SUPERIORES!

🏆 {defending_team.upper()} SEMPRE! 🏆
        """
        
        return {
            "status": "success",
            "report": counter_argument.strip()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Erro ao gerar contra-argumento: {str(e)}"
        }

def moderate_debate_session(action: str, **kwargs) -> Dict[str, Any]:
    """
    Moderates debate sessions with timing and rule enforcement.
    
    Args:
        action: Action to perform (start, status, analyze, end)
        **kwargs: Additional parameters for the action
        
    Returns:
        dict: Contains 'status' and 'report' with moderation result
    """
    try:
        if action == "start":
            duration = kwargs.get("duration_minutes", 5)
            
            if duration < 1 or duration > 30:
                return {
                    "status": "error",
                    "error_message": "Duração deve ser entre 1 e 30 minutos"
                }
            
            session_info = f"""
⚖️ SESSÃO DE DEBATE OFICIAL INICIADA ⚖️

📋 CONFIGURAÇÃO:
• Duração: {duration} minutos
• Moderador: Sistema ADK Oficial
• Protocolo: A2A (Agent-to-Agent)
• Participantes: 4 agentes especializados

🎯 REGRAS ESTABELECIDAS:
1. Argumentos baseados em fatos têm prioridade
2. Respeito mútuo é obrigatório
3. Cada agente terá tempo igual de exposição
4. Pesquisas podem ser solicitadas a qualquer momento
5. Análise final será imparcial e técnica

⏰ CRONÔMETRO INICIADO!
Que comece o melhor debate de futebol do Rio de Janeiro!

🚀 SISTEMA ADK ATIVO - AGENTES PRONTOS PARA INTERAÇÃO!
            """
            
            return {
                "status": "success",
                "report": session_info.strip()
            }
            
        elif action == "status":
            remaining_time = kwargs.get("remaining_seconds", 0)
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            
            status_report = f"""
📊 STATUS DA SESSÃO DE DEBATE:

⏰ Tempo Restante: {minutes:02d}:{seconds:02d}
🎤 Agentes Ativos: 4/4
🔄 Protocolo A2A: Funcionando
📈 Interações: {kwargs.get("interactions", 0)}

{"⚠️ ÚLTIMOS MINUTOS DO DEBATE!" if remaining_time < 60 else "✅ Debate em andamento normal"}
            """
            
            return {
                "status": "success", 
                "report": status_report.strip()
            }
            
        elif action == "analyze":
            transcript = kwargs.get("transcript", "")
            
            if not transcript:
                return {
                    "status": "error",
                    "error_message": "Transcrição necessária para análise"
                }
            
            # Perform final analysis
            words = len(transcript.split())
            flamengo_mentions = transcript.lower().count("flamengo")
            fluminense_mentions = transcript.lower().count("fluminense")
            
            winner = "FLAMENGO" if flamengo_mentions > fluminense_mentions else "FLUMINENSE" if fluminense_mentions > flamengo_mentions else "EMPATE"
            
            final_analysis = f"""
🏆 ANÁLISE FINAL DO DEBATE - MODERAÇÃO ADK 🏆

📊 ESTATÍSTICAS GERAIS:
• Total de palavras: {words:,}
• Menções Flamengo: {flamengo_mentions}
• Menções Fluminense: {fluminense_mentions}
• Duração da análise: {datetime.now().strftime("%H:%M:%S")}

🔴 PERFORMANCE FLAMENGO:
• Frequência de menções: {flamengo_mentions}
• Estratégia: {"Ofensiva" if flamengo_mentions > fluminense_mentions else "Defensiva"}

🟢 PERFORMANCE FLUMINENSE:
• Frequência de menções: {fluminense_mentions}  
• Estratégia: {"Ofensiva" if fluminense_mentions > flamengo_mentions else "Defensiva"}

⚖️ VEREDICTO TÉCNICO: {winner}

🎭 CONSIDERAÇÕES FINAIS:
{"Debate equilibrado com argumentos sólidos de ambos os lados" if winner == "EMPATE" else f"{winner} demonstrou maior presença argumentativa"}

🤖 Análise realizada pelo Sistema ADK com protocolo A2A
            """
            
            return {
                "status": "success",
                "report": final_analysis.strip()
            }
            
        else:
            return {
                "status": "error",
                "error_message": f"Ação '{action}' não reconhecida"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Erro na moderação: {str(e)}"
        }

# Agent definitions following ADK patterns
def create_supervisor_agent():
    """Creates the supervisor agent following ADK patterns"""
    return {
        "name": "supervisor", 
        "model": "gemini-2.0-flash",
        "description": "Especialista em retórica e moderação de debates esportivos",
        "instruction": """Você é um supervisor de debates especializado em retórica, persuasão e análise linguística. 
        Sua função é moderar debates entre torcedores, garantir que as regras sejam seguidas, e ao final fornecer 
        uma análise imparcial sobre a qualidade dos argumentos apresentados. Use suas ferramentas para gerenciar 
        sessões de debate e analisar a força argumentativa.""",
        "tools": [moderate_debate_session, analyze_argument_strength]
    }

def create_flamengo_agent():
    """Creates the Flamengo fan agent following ADK patterns"""
    return {
        "name": "flamengo_fan",
        "model": "gemini-2.0-flash", 
        "description": "Torcedor apaixonado do Flamengo especializado em argumentação persuasiva",
        "instruction": """Você é um torcedor fanático do Flamengo. Seu objetivo é usar argumentos apaixonados, 
        dados históricos e provocações inteligentes para defender seu time. Use suas ferramentas para buscar 
        estatísticas e gerar contra-argumentos convincentes. Seja passionate mas respeitoso.""",
        "tools": [get_team_statistics, generate_counter_argument, analyze_argument_strength]
    }

def create_fluminense_agent():
    """Creates the Fluminense fan agent following ADK patterns"""
    return {
        "name": "fluminense_fan",
        "model": "gemini-2.0-flash",
        "description": "Torcedor orgulhoso do Fluminense especializado em argumentação elegante", 
        "instruction": """Você é um torcedor orgulhoso do Fluminense. Use a rica história do clube, a tradição 
        e a beleza do futebol para argumentar com classe e elegância. Suas ferramentas ajudam a buscar dados 
        históricos e criar contra-argumentos sofisticados. Mantenha sempre a postura digna do Tricolor.""",
        "tools": [get_team_statistics, generate_counter_argument, analyze_argument_strength]
    }

def create_researcher_agent():
    """Creates the researcher agent following ADK patterns"""
    return {
        "name": "researcher",
        "model": "gemini-2.0-flash",
        "description": "Especialista em pesquisa objetiva e fornecimento de dados factuais",
        "instruction": """Você é um pesquisador neutro e objetivo. Sua função é fornecer dados factuais, 
        estatísticas e informações verificáveis quando solicitado pelos outros agentes. Não tome partido, 
        seja sempre imparcial e baseie suas respostas em fatos. Use suas ferramentas para analisar argumentos 
        tecnicamente.""",
        "tools": [get_team_statistics, analyze_argument_strength]
    }

# Multi-agent system following ADK patterns
root_agent = {
    "name": "debate_coordinator",
    "model": "gemini-2.0-flash",
    "description": "Coordenador principal do sistema de debate multi-agente",
    "instruction": """Você é o coordenador principal de um sistema de debate entre torcedores de futebol usando 
    protocolo A2A. Gerencie a interação entre os 4 agentes especializados (supervisor, torcedor do Flamengo, 
    torcedor do Fluminense, e pesquisador) para criar debates dinâmicos e informativos. Garanta que todos os 
    agentes participem de forma equilibrada.""",
    "tools": [moderate_debate_session, get_team_statistics, analyze_argument_strength],
    "sub_agents": [
        create_supervisor_agent(),
        create_flamengo_agent(), 
        create_fluminense_agent(),
        create_researcher_agent()
    ]
}