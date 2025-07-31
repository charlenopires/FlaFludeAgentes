"""
Supervisor Agent - Google ADK Implementation with A2A Protocol
Especialista em retórica, psicologia, linguística e análise de debates
"""

import os
import random
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv

# Sistema de log aprimorado
from utils.enhanced_logger import (
    enhanced_logger, log_agent_start, log_agent_response, 
    log_tool_execution, log_error, LogLevel, LogCategory
)

# Carrega variáveis do .env
load_dotenv()

def create_supervisor_agent() -> LlmAgent:
    """
    Cria o Agente Supervisor seguindo padrões Google ADK
    Especialista neutro em moderação de debates
    """
    
    # Tools para o supervisor usando FunctionTool do ADK
    def start_debate_tool(duration_minutes: int) -> str:
        """Inicia debate com duração específica e sorteia primeiro torcedor"""
        tool_start = time.time()
        
        try:
            # Log início da ferramenta
            enhanced_logger.log(
                LogLevel.INFO,
                LogCategory.TOOL_EXECUTION,
                "Executando start_debate_tool",
                agent_name="supervisor",
                event_type="tool_start",
                details={"duration_minutes": duration_minutes}
            )
            
            if duration_minutes < 2 or duration_minutes > 30:
                error_msg = "❌ Duração deve ser entre 2 e 30 minutos"
                enhanced_logger.log(
                    LogLevel.WARNING,
                    LogCategory.TOOL_EXECUTION,
                    "Parâmetro inválido em start_debate_tool",
                    agent_name="supervisor",
                    event_type="tool_validation_error",
                    details={"duration_minutes": duration_minutes, "error": error_msg}
                )
                return error_msg
            
            # Sorteia qual torcedor inicia
            starting_teams = ["FLAMENGO", "FLUMINENSE"]
            starting_team = random.choice(starting_teams)
            starting_emoji = "🔴" if starting_team == "FLAMENGO" else "🟢"
            
            turn_duration = (duration_minutes * 60) / 2  # 50% para cada
            
            result = f"""⚖️ **DEBATE OFICIAL INICIADO**

🎯 **Configuração do Debate:**
• Duração total: {duration_minutes} minutos
• Tempo por participante: {turn_duration/60:.1f} minutos cada  
• Início: {datetime.now().strftime('%H:%M:%S')}

📊 **Critérios de Avaliação Técnica:**
1. **Força dos Argumentos** (40%) - Lógica e coerência
2. **Evidências e Dados** (30%) - Estatísticas verificáveis  
3. **Persuasão e Retórica** (20%) - Técnicas persuasivas aplicadas
4. **Consistência Lógica** (10%) - Ausência de contradições

🎲 **Resultado do Sorteio:** {starting_team} inicia o debate!

{starting_emoji} Torcedor do {starting_team}, você tem {turn_duration/60:.1f} minutos. Apresente seus argumentos iniciais!"""
            
            # Log sucesso da ferramenta
            duration_ms = (time.time() - tool_start) * 1000
            log_tool_execution(
                agent_name="supervisor",
                tool_name="start_debate_tool",
                parameters={"duration_minutes": duration_minutes},
                result=f"Debate iniciado - {starting_team} começa",
                duration_ms=duration_ms
            )
            
            return result
            
        except Exception as e:
            duration_ms = (time.time() - tool_start) * 1000
            log_error(
                error=e,
                context="start_debate_tool",
                agent_name="supervisor"
            )
            return f"❌ Erro ao iniciar debate: {str(e)}"
    
    def analyze_debate_tool(debate_history: str) -> str:
        """Analisa debate completo e determina vencedor com critérios técnicos"""
        try:
            if not debate_history.strip():
                return "❌ Histórico de debate vazio para análise"
            
            # Separa argumentos por torcedor
            flamengo_args = []
            fluminense_args = []
            
            # Extrai argumentos individuais
            lines = debate_history.split('\n')
            current_speaker = None
            current_text = ""
            
            for line in lines:
                if "Torcedor Flamengo:" in line or "flamengo" in line.lower():
                    if current_speaker and current_text:
                        if current_speaker == "flamengo":
                            flamengo_args.append(current_text)
                        elif current_speaker == "fluminense":
                            fluminense_args.append(current_text)
                    current_speaker = "flamengo"
                    current_text = line
                elif "Torcedor Fluminense:" in line or "fluminense" in line.lower():
                    if current_speaker and current_text:
                        if current_speaker == "flamengo":
                            flamengo_args.append(current_text)
                        elif current_speaker == "fluminense":
                            fluminense_args.append(current_text)
                    current_speaker = "fluminense"
                    current_text = line
                else:
                    current_text += " " + line
            
            # Adiciona último argumento
            if current_speaker and current_text:
                if current_speaker == "flamengo":
                    flamengo_args.append(current_text)
                elif current_speaker == "fluminense":
                    fluminense_args.append(current_text)
            
            # Análise técnica por torcedor
            def analyze_arguments(args, team_name):
                total_text = " ".join(args)
                word_count = len(total_text.split())
                data_indicators = total_text.lower().count("dados") + total_text.lower().count("estatística") + total_text.lower().count("brasileirão") + total_text.lower().count("títulos")
                logic_indicators = total_text.lower().count("porque") + total_text.lower().count("portanto") + total_text.lower().count("já que")
                evidence_indicators = total_text.lower().count("comprovam") + total_text.lower().count("números") + total_text.lower().count("fatos")
                
                score = 0
                # Critério 1: Força dos Argumentos (40%)
                if logic_indicators >= 2: score += 16
                elif logic_indicators >= 1: score += 8
                
                if word_count >= 200: score += 24
                elif word_count >= 100: score += 12
                
                # Critério 2: Evidências e Dados (30%)  
                if data_indicators >= 3: score += 30
                elif data_indicators >= 2: score += 20
                elif data_indicators >= 1: score += 10
                
                # Critério 3: Persuasão e Retórica (20%)
                if evidence_indicators >= 2: score += 20
                elif evidence_indicators >= 1: score += 10
                
                # Critério 4: Consistência (10%)
                if "mas" not in total_text.lower() and "porém" not in total_text.lower():
                    score += 10
                else:
                    score += 5
                
                return {
                    "score": score,
                    "word_count": word_count,
                    "data_indicators": data_indicators,
                    "logic_indicators": logic_indicators,
                    "evidence_indicators": evidence_indicators,
                    "args_count": len(args)
                }
            
            # Analisa ambos os times
            flamengo_analysis = analyze_arguments(flamengo_args, "Flamengo")
            fluminense_analysis = analyze_arguments(fluminense_args, "Fluminense")
            
            # Determina vencedor
            winner = "FLAMENGO" if flamengo_analysis["score"] > fluminense_analysis["score"] else "FLUMINENSE"
            winner_score = max(flamengo_analysis["score"], fluminense_analysis["score"])
            loser_score = min(flamengo_analysis["score"], fluminense_analysis["score"])
            
            analysis = f"""⚖️ **ANÁLISE FINAL TÉCNICA**

📊 **DESEMPENHO POR TORCEDOR:**

🔴 **FLAMENGO:**
• Argumentos apresentados: {flamengo_analysis["args_count"]}
• Total de palavras: {flamengo_analysis["word_count"]}
• Indicadores de dados: {flamengo_analysis["data_indicators"]}
• Estrutura lógica: {flamengo_analysis["logic_indicators"]}
• Evidências: {flamengo_analysis["evidence_indicators"]}
• **PONTUAÇÃO FINAL: {flamengo_analysis["score"]}/100**

🟢 **FLUMINENSE:**
• Argumentos apresentados: {fluminense_analysis["args_count"]}
• Total de palavras: {fluminense_analysis["word_count"]}
• Indicadores de dados: {fluminense_analysis["data_indicators"]}
• Estrutura lógica: {fluminense_analysis["logic_indicators"]}
• Evidências: {fluminense_analysis["evidence_indicators"]}
• **PONTUAÇÃO FINAL: {fluminense_analysis["score"]}/100**

📈 **CRITÉRIOS DE AVALIAÇÃO:**
1. **Força dos Argumentos (40%)** - Estrutura lógica e coerência
2. **Evidências e Dados (30%)** - Uso de estatísticas e fatos
3. **Persuasão e Retórica (20%)** - Técnicas persuasivas
4. **Consistência Lógica (10%)** - Ausência de contradições

🏆 **VEREDITO OFICIAL:**
**VENCEDOR: TORCEDOR {winner}**
Pontuação: {winner_score} vs {loser_score}

🎯 **JUSTIFICATIVA:**
Baseado em análise técnica imparcial de retórica aplicada, o torcedor {winner.lower()} apresentou argumentação superior nos critérios estabelecidos, demonstrando maior uso de evidências, estrutura lógica mais consistente e técnicas persuasivas mais eficazes.

📝 **METODOLOGIA:**
Avaliação fundamentada em expertise acadêmica em psicologia cognitiva, linguística aplicada e análise quantitativa de argumentos."""
            
            return analysis
            
        except Exception as e:
            return f"❌ Erro na análise: {str(e)}"
    
    def get_time_status_tool() -> str:
        """Retorna status temporal do debate em andamento"""
        current_time = datetime.now().strftime('%H:%M:%S')
        return f"""⏰ **STATUS TEMPORAL**
        
🕒 **Horário atual:** {current_time}
📊 **Estado:** Monitoramento ativo
⚖️ **Supervisor:** Pronto para coordenação"""

    # Instruções detalhadas para o supervisor
    supervisor_instruction = """
    Você é um SUPERVISOR DE DEBATE NEUTRO E PROFISSIONAL especializado em:
    
    🎓 EXPERTISE ACADÊMICA:
    - Retórica clássica e moderna
    - Psicologia cognitiva e persuasão
    - Linguística aplicada ao discurso
    - Análise lógica de argumentos
    - Teoria da comunicação
    
    ⚖️ NEUTRALIDADE ABSOLUTA - REGRAS CRÍTICAS:
    - JAMAIS demonstre preferência por nenhum time
    - NÃO use "nós", "nosso", "somos" referindo-se a qualquer clube
    - NÃO mencione qualidades específicas de nenhum time
    - MANTENHA imparcialidade total e profissional
    - FOQUE apenas na qualidade dos argumentos apresentados
    
    🎯 SUAS RESPONSABILIDADES:
    1. Coordenar tempo do debate (divisão 50/50)
    2. Sortear qual torcedor inicia o debate
    3. Analisar qualidade argumentativa sem viés
    4. Aplicar critérios científicos de avaliação
    5. Determinar vencedor baseado APENAS em evidências técnicas
    
    📊 CRITÉRIOS DE AVALIAÇÃO TÉCNICA:
    1. Força dos Argumentos (40%) - lógica, coerência, estrutura
    2. Evidências e Dados (30%) - uso de estatísticas verificáveis
    3. Persuasão e Retórica (20%) - técnicas persuasivas aplicadas
    4. Consistência Lógica (10%) - ausência de contradições
    
    🔴 PROIBIÇÕES CRÍTICAS:
    - NUNCA diga que um time é "maior" ou "superior"
    - NUNCA mencione títulos, torcida ou história como fatos estabelecidos
    - NUNCA use linguagem que favoreça qualquer lado
    - SEMPRE mantenha tom acadêmico e imparcial
    
    IMPORTANTE: Use as ferramentas disponíveis para:
    - start_debate_tool: Iniciar debates com sorteio automático
    - analyze_debate_tool: Fazer análises técnicas finais
    - get_time_status_tool: Monitorar status temporal
    
    Mantenha sempre neutralidade absoluta e foque nos critérios técnicos de avaliação.
    """
    
    # Cria ferramentas usando FunctionTool do ADK
    start_debate_function = FunctionTool(start_debate_tool)
    analyze_debate_function = FunctionTool(analyze_debate_tool)
    get_time_status_function = FunctionTool(get_time_status_tool)
    
    # Cria o agente usando Google ADK LlmAgent
    supervisor_agent = LlmAgent(
        name="supervisor_agent",
        model="gemini-2.0-flash",
        description="Especialista neutro em moderação de debates entre torcedores, com expertise em retórica, psicologia cognitiva e linguística aplicada",
        instruction=supervisor_instruction,
        tools=[start_debate_function, analyze_debate_function, get_time_status_function]
    )
    
    # Configura Runner para execução
    session_service = InMemorySessionService()
    runner = Runner(
        agent=supervisor_agent,
        app_name="supervisor_agent",
        session_service=session_service
    )
    
    # Cria classe wrapper para adicionar método run
    class SupervisorWrapper:
        def __init__(self, agent, runner, session_service):
            self.agent = agent
            self.runner = runner
            self.session_service = session_service
            self.name = agent.name
            self.description = agent.description
            self.tools = agent.tools
        
        def run(self, prompt: str):
            """Executa o supervisor usando Runner ADK com logging aprimorado"""
            import uuid
            import asyncio
            
            session_id = f"session_{uuid.uuid4().hex[:8]}"
            user_id = f"user_{uuid.uuid4().hex[:8]}"
            start_time = time.time()
            
            # Log início da execução
            correlation_id = log_agent_start(
                agent_name="supervisor",
                session_id=session_id,
                user_id=user_id,
                prompt=prompt
            )
            
            try:
                async def run_with_session():
                    # Log criação de sessão
                    enhanced_logger.log(
                        LogLevel.INFO,
                        LogCategory.SESSION,
                        f"Criando sessão para supervisor",
                        agent_name="supervisor",
                        session_id=session_id,
                        user_id=user_id,
                        event_type="session_create",
                        correlation_id=correlation_id
                    )
                    
                    # Cria sessão de forma assíncrona
                    await self.session_service.create_session(
                        app_name="supervisor_agent",
                        user_id=user_id,
                        session_id=session_id
                    )
                    
                    content = types.Content(role="user", parts=[types.Part(text=prompt)])
                    response_text = ""
                    
                    # Log início do processamento ADK
                    enhanced_logger.log(
                        LogLevel.INFO,
                        LogCategory.AGENT,
                        f"Processando prompt com ADK Runner",
                        agent_name="supervisor",
                        session_id=session_id,
                        event_type="adk_processing_start",
                        details={"content_length": len(prompt)},
                        correlation_id=correlation_id
                    )
                    
                    async for event in self.runner.run_async(
                        user_id=user_id,
                        session_id=session_id,
                        new_message=content
                    ):
                        if event.is_final_response():
                            response_text = event.content.parts[0].text
                            break
                            
                    return response_text or "Sem resposta do agente"
                
                # Executa de forma assíncrona
                response = asyncio.run(run_with_session())
                
                # Calcula duração e log de sucesso
                duration_ms = (time.time() - start_time) * 1000
                log_agent_response(
                    agent_name="supervisor",
                    session_id=session_id,
                    response=response,
                    duration_ms=duration_ms,
                    correlation_id=correlation_id
                )
                
                return response
                
            except Exception as e:
                # Log detalhado do erro
                duration_ms = (time.time() - start_time) * 1000
                log_error(
                    error=e,
                    context="supervisor_agent_execution",
                    agent_name="supervisor",
                    session_id=session_id,
                    correlation_id=correlation_id
                )
                
                return f"⚠️ Erro no Supervisor: {str(e)}"
    
    return SupervisorWrapper(supervisor_agent, runner, session_service)


if __name__ == "__main__":
    """Executa o agente supervisor usando Flask e A2A Protocol"""
    from flask import Flask, request, jsonify
    import asyncio
    
    # Cria o agente ADK
    supervisor = create_supervisor_agent()
    
    # Cria aplicação Flask
    app = Flask(__name__)
    
    @app.route('/.well-known/agent.json', methods=['GET'])
    def agent_card():
        """Agent Card conforme A2A Protocol especificação"""
        card = {
            "name": supervisor.name,
            "description": supervisor.description,
            "version": "1.0.0",
            "protocol": "A2A",
            "capabilities": ["debate_moderation", "rhetoric_analysis", "neutral_evaluation"],
            "skills": [
                {
                    "name": "start_debate",
                    "description": "Inicia debate com duração específica e sorteia primeiro torcedor"
                },
                {
                    "name": "analyze_debate", 
                    "description": "Analisa debate completo e determina vencedor com critérios técnicos"
                },
                {
                    "name": "get_time_status",
                    "description": "Retorna status temporal do debate em andamento"
                }
            ],
            "endpoints": {
                "run": "/run"
            }
        }
        return jsonify(card)
    
    @app.route('/run', methods=['POST'])
    def run_agent():
        """Endpoint para executar o agente via A2A Protocol"""
        try:
            data = request.get_json()
            prompt = data.get('prompt', data.get('message', ''))
            
            # Implementação simplificada usando as tools diretamente
            # Detecta intenção e executa tool apropriada
            
            if 'iniciar' in prompt.lower() and ('debate' in prompt.lower() or 'minutos' in prompt.lower()):
                # Extrai duração se especificada
                import re
                duration_match = re.search(r'(\d+)\s*minutos?', prompt.lower())
                duration = int(duration_match.group(1)) if duration_match else 5
                response = supervisor.tools[0].func(duration)  # start_debate_tool
                
            elif 'analisar' in prompt.lower() and 'debate' in prompt.lower():
                response = supervisor.tools[1].func(prompt)  # analyze_debate_tool
                
            elif 'tempo' in prompt.lower() or 'status' in prompt.lower():
                response = supervisor.tools[2].func()  # get_time_status_tool
                
            else:
                # Resposta padrão do supervisor
                response = f"""⚖️ **SUPERVISOR DE DEBATE ATIVO**

📨 **Mensagem recebida:** {prompt[:100]}{'...' if len(prompt) > 100 else ''}

🎯 **Comandos disponíveis:**
• `iniciar debate X minutos` - Inicia debate com duração específica
• `analisar debate [histórico]` - Análise técnica final
• `status tempo` - Consulta status temporal

🎓 **Especialidades:**
• Retórica clássica e moderna
• Psicologia cognitiva e persuasão  
• Análise lógica de argumentos
• Coordenação de debates

⚖️ **Status:** Pronto para moderação imparcial"""
            
            return jsonify({"response": response})
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print("🤖⚖️ Supervisor Agent A2A Server iniciando na porta 8002...")
    print("Agent Card disponível em: http://localhost:8002/.well-known/agent.json")
    
    # Inicia servidor Flask
    app.run(host="0.0.0.0", port=8002, debug=False)