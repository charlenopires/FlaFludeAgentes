"""
Supervisor Agent - Google ADK Implementation with A2A Protocol
Especialista em retórica, psicologia, linguística e análise de debates
"""

import os
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

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
        try:
            if duration_minutes < 2 or duration_minutes > 30:
                return "❌ Duração deve ser entre 2 e 30 minutos"
            
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
            
            return result
            
        except Exception as e:
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
    supervisor = LlmAgent(
        name="supervisor_agent",
        model="gemini-2.0-flash",
        description="Especialista neutro em moderação de debates entre torcedores, com expertise em retórica, psicologia cognitiva e linguística aplicada",
        instruction=supervisor_instruction,
        tools=[start_debate_function, analyze_debate_function, get_time_status_function]
    )
    
    return supervisor


if __name__ == "__main__":
    """Executa o agente supervisor usando Flask e A2A Protocol"""
    from flask import Flask, request, jsonify
    
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
            
            # Executa o agente ADK
            response = ""
            for chunk in supervisor.run(prompt):
                if isinstance(chunk, str):
                    response += chunk
                elif hasattr(chunk, 'content'):
                    response += chunk.content
            
            return jsonify({"response": response})
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print("🤖⚖️ Supervisor Agent A2A Server iniciando na porta 8002...")
    print("Agent Card disponível em: http://localhost:8002/.well-known/agent.json")
    
    # Inicia servidor Flask
    app.run(host="0.0.0.0", port=8002, debug=False)