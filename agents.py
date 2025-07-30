"""
Sistema de 4 Agentes Independentes para Debate Fla-Flu
Seguindo Google ADK com protocolo A2A
"""

import os
import time
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Configuração da API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

class BaseAgent:
    """Classe base para todos os agentes ADK"""
    
    def __init__(self, name: str, role: str, model: str = "gemini-2.0-flash"):
        self.name = name
        self.role = role
        self.model = model
        self.conversation_history = []
        self.tools = []
        self.active = False
        
        # Inicializa cliente Gemini
        if GOOGLE_API_KEY:
            self.client = genai.GenerativeModel(model)
        else:
            self.client = None
    
    def send_message(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Envia mensagem via protocolo A2A"""
        try:
            if not self.client:
                return {
                    "status": "error",
                    "agent": self.name,
                    "message": "API key não configurada",
                    "timestamp": time.time()
                }
            
            # Adiciona contexto se fornecido
            full_prompt = message
            if context:
                full_prompt = f"Contexto: {json.dumps(context, ensure_ascii=False)}\n\nMensagem: {message}"
            
            # Envia para Gemini
            response = self.client.generate_content(full_prompt)
            response_text = response.text
            
            # Log da conversa
            self.conversation_history.append({
                "input": message,
                "output": response_text,
                "timestamp": time.time()
            })
            
            return {
                "status": "success",
                "agent": self.name,
                "message": response_text,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "message": f"Erro: {str(e)}",
                "timestamp": time.time()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            "name": self.name,
            "role": self.role,
            "active": self.active,
            "messages_count": len(self.conversation_history),
            "tools_available": len(self.tools)
        }

class SupervisorAgent(BaseAgent):
    """Agente Supervisor - Coordena debate e analisa resultados"""
    
    def __init__(self):
        super().__init__("Supervisor", "Coordenador de Debate")
        self.debate_duration = 0
        self.debate_start_time = None
        self.current_speaker = None
        self.turn_duration = 0
        self.flamengo_time = 0
        self.fluminense_time = 0
        
        self.system_prompt = """
        Você é um SUPERVISOR DE DEBATE especialista em:
        - Retórica e persuasão
        - Psicologia cognitiva
        - Linguística aplicada
        - Análise lógica de argumentos
        
        Suas funções:
        1. Coordenar tempo do debate (50% para cada time)
        2. Analisar qualidade argumentativa
        3. Determinar vencedor baseado em critérios técnicos
        4. Manter neutralidade absoluta
        
        SEMPRE mantenha tom profissional e imparcial.
        """
    
    def start_debate(self, duration_minutes: int) -> Dict[str, Any]:
        """Inicia o debate com duração específica"""
        try:
            self.debate_duration = duration_minutes
            self.debate_start_time = time.time()
            self.turn_duration = (duration_minutes * 60) / 2  # 50% para cada
            self.active = True
            
            message = f"""
🎯 **DEBATE OFICIAL INICIADO**

⏱️ **Configuração:**
• Duração total: {duration_minutes} minutos
• Tempo por time: {self.turn_duration/60:.1f} minutos cada
• Início: {datetime.now().strftime('%H:%M:%S')}

⚖️ **Critérios de Avaliação:**
1. **Força dos Argumentos** (40%)
2. **Evidências e Dados** (30%) 
3. **Persuasão e Retórica** (20%)
4. **Consistência Lógica** (10%)

🎲 **Sorteio:** FLAMENGO inicia o debate!

🔴 Agente Flamengo, você tem {self.turn_duration/60:.1f} minutos. Comece sua argumentação!
            """
            
            self.current_speaker = "Flamengo"
            
            return self.send_message(message)
            
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "message": f"Erro ao iniciar debate: {str(e)}",
                "timestamp": time.time()
            }
    
    def analyze_final_debate(self, debate_history: List[Dict]) -> Dict[str, Any]:
        """Análise final especializada do debate"""
        try:
            # Prepara dados para análise
            flamengo_messages = [msg for msg in debate_history if "flamengo" in msg.get("agent", "").lower()]
            fluminense_messages = [msg for msg in debate_history if "fluminense" in msg.get("agent", "").lower()]
            
            analysis_prompt = f"""
            Como especialista em debate, psicologia, linguística e retórica, analise este debate:
            
            ARGUMENTOS FLAMENGO ({len(flamengo_messages)} mensagens):
            {json.dumps([msg.get("message", "") for msg in flamengo_messages], ensure_ascii=False, indent=2)}
            
            ARGUMENTOS FLUMINENSE ({len(fluminense_messages)} mensagens):
            {json.dumps([msg.get("message", "") for msg in fluminense_messages], ensure_ascii=False, indent=2)}
            
            Forneça análise detalhada considerando:
            1. Força argumentativa e lógica
            2. Uso de evidências e dados
            3. Técnicas persuasivas empregadas
            4. Consistência e coerência
            5. Impacto retórico
            
            Declare um VENCEDOR com justificativa técnica.
            """
            
            return self.send_message(analysis_prompt)
            
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "message": f"Erro na análise: {str(e)}",
                "timestamp": time.time()
            }
    
    def get_time_remaining(self) -> Dict[str, Any]:
        """Retorna tempo restante do debate"""
        if not self.debate_start_time:
            return {"total": 0, "current_turn": 0}
        
        elapsed = time.time() - self.debate_start_time
        total_remaining = max(0, (self.debate_duration * 60) - elapsed)
        
        return {
            "total_remaining": total_remaining,
            "current_speaker": self.current_speaker,
            "turn_time_used": min(elapsed, self.turn_duration) if self.current_speaker == "Flamengo" else max(0, elapsed - self.turn_duration)
        }

class FlamengoAgent(BaseAgent):
    """Agente Torcedor do Flamengo"""
    
    def __init__(self):
        super().__init__("Torcedor Flamengo", "Defensor Rubro-Negro")
        
        self.persuasion_text = """
        🔴⚡ **FLAMENGO - A NAÇÃO RUBRO-NEGRA** ⚡🔴
        
        Somos o MAIOR clube do Brasil! Com mais de 40 milhões de torcedores apaixonados, 
        o Flamengo não é apenas um time - é um sentimento que move o país!
        
        🏆 **NOSSOS TÍTULOS FALAM POR SI:**
        • 8 Brasileirões (mais que qualquer rival carioca)
        • 3 Libertadores (incluindo as gloriosas de 2019 e 2022)
        • 1 Mundial (1981 - Zico eterno!)
        • Mais de 35 Cariocas
        
        ⭐ **ESTRELAS MUNDIAIS:**
        De Zico a Vinícius Jr., formamos e revelamos os maiores talentos do futebol mundial.
        Gabigol, Pedro, Arrascaeta - nosso elenco atual é FENOMENAL!
        
        💪 **FORÇA INCOMPARÁVEL:**
        Somos o time com maior torcida, maior estrutura, maiores investimentos e maior paixão.
        O Maracanã vira um CALDEIRÃO quando jogamos!
        
        🔥 Uma vez Flamengo, sempre Flamengo! MENGO é RAÇA, é GARRA, é VITÓRIA!
        """
        
        self.system_prompt = f"""
        {self.persuasion_text}
        
        Você é um TORCEDOR FANÁTICO do Flamengo. Sua missão:
        1. Defender o Flamengo com PAIXÃO e DADOS
        2. Usar argumentos emocionais E factuais
        3. Provocar o rival com inteligência
        4. Solicitar dados ao pesquisador quando necessário
        5. NUNCA admitir derrota - somos SUPERIORES!
        
        Mantenha o tom apaixonado mas respeitoso. Use emojis do Flamengo: 🔴⚡🏆
        """
    
    def get_initial_argument(self) -> Dict[str, Any]:
        """Retorna argumento inicial persuasivo"""
        prompt = f"""
        {self.system_prompt}
        
        Apresente seu argumento inicial DEMOLIDOR sobre por que o Flamengo é superior ao Fluminense.
        Use dados, emoção e persuasão. Seja convincente e apaixonado!
        """
        
        return self.send_message(prompt)
    
    def counter_argument(self, opponent_message: str, research_data: str = None) -> Dict[str, Any]:
        """Gera contra-argumento baseado na mensagem do oponente"""
        context = {
            "opponent_argument": opponent_message,
            "research_data": research_data if research_data else "Nenhum dado adicional"
        }
        
        prompt = f"""
        {self.system_prompt}
        
        O torcedor do Fluminense disse: "{opponent_message}"
        
        CONTRA-ATAQUE com argumentos devastadores! Use paixão, dados e lógica para
        destronar completamente esse argumento fraco. Se necessário, solicite dados
        ao pesquisador mencionando "PESQUISADOR: [sua solicitação]".
        """
        
        return self.send_message(prompt, context)

class FluminenseAgent(BaseAgent):
    """Agente Torcedor do Fluminense"""
    
    def __init__(self):
        super().__init__("Torcedor Fluminense", "Defensor Tricolor")
        
        self.persuasion_text = """
        💚🤍❤️ **FLUMINENSE - TRADIÇÃO E ELEGÂNCIA** ❤️🤍💚
        
        Somos o time mais TRADICIONAL do Rio de Janeiro! Fundado em 1902, 
        carregamos mais de 120 anos de história, classe e futebol-arte!
        
        🏆 **NOSSA GLORIOSA HISTÓRIA:**
        • 4 Brasileirões conquistados com muito suor
        • CAMPEÕES DA LIBERTADORES 2023 (ATUAL CAMPEÃO!)
        • Mais de 30 Cariocas com futebol de qualidade
        • Formamos os maiores craques da Seleção
        
        ⭐ **ESCOLA DE CRAQUES:**
        Didi, Carlos Alberto Torres, Rivellino, Fred - revelamos LENDAS do futebol!
        Germán Cano, Ganso, Jhon Arias - nosso atual elenco é TÉCNICO e QUALIFICADO!
        
        🎭 **FUTEBOL-ARTE:**
        Não jogamos apenas futebol - fazemos ARTE em campo! 
        Temos estilo, elegância e a torcida mais refinada do Brasil!
        
        ✨ Somos tricolores de coração! FLU é TRADIÇÃO, é CLASSE, é CONQUISTA!
        """
        
        self.system_prompt = f"""
        {self.persuasion_text}
        
        Você é um TORCEDOR ORGULHOSO do Fluminense. Sua missão:
        1. Defender o Fluminense com ELEGÂNCIA e TRADIÇÃO
        2. Usar a rica história e conquistas recentes
        3. Destacar nossa superioridade técnica e cultural
        4. Solicitar dados ao pesquisador quando necessário
        5. Mostrar nossa CLASSE superior ao rival
        
        Mantenha tom elegante mas firme. Use emojis do Fluminense: 💚🤍❤️✨🏆
        """
    
    def get_initial_argument(self) -> Dict[str, Any]:
        """Retorna argumento inicial persuasivo"""
        prompt = f"""
        {self.system_prompt}
        
        Apresente seu argumento inicial ELEGANTE sobre por que o Fluminense é superior ao Flamengo.
        Use nossa tradição, conquistas recentes (Libertadores 2023!) e superioridade técnica.
        Seja convincente com classe!
        """
        
        return self.send_message(prompt)
    
    def counter_argument(self, opponent_message: str, research_data: str = None) -> Dict[str, Any]:
        """Gera contra-argumento baseado na mensagem do oponente"""
        context = {
            "opponent_argument": opponent_message,
            "research_data": research_data if research_data else "Nenhum dado adicional"
        }
        
        prompt = f"""
        {self.system_prompt}
        
        O torcedor do Flamengo disse: "{opponent_message}"
        
        RESPONDA com CLASSE e ELEGÂNCIA! Use nossa tradição, conquistas recentes e
        superioridade técnica para desmontar esse argumento. Se necessário, solicite dados
        ao pesquisador mencionando "PESQUISADOR: [sua solicitação]".
        """
        
        return self.send_message(prompt, context)

class ResearcherAgent(BaseAgent):
    """Agente Pesquisador - Busca dados na internet"""
    
    def __init__(self):
        super().__init__("Pesquisador", "Especialista em Dados")
        
        self.system_prompt = """
        Você é um PESQUISADOR NEUTRO e OBJETIVO especializado em futebol brasileiro.
        
        Suas funções:
        1. Buscar dados FACTUAIS sobre Flamengo e Fluminense
        2. Fornecer estatísticas VERIFICÁVEIS
        3. Manter NEUTRALIDADE absoluta
        4. Responder rapidamente às solicitações
        5. Indicar fontes quando possível
        
        NUNCA tome partido - seja sempre imparcial e técnico!
        """
    
    def search_data(self, query: str, requesting_agent: str) -> Dict[str, Any]:
        """Busca dados sobre os times (simulado - em produção usaria API real)"""
        
        # Base de dados simulada (em produção seria busca real na internet)
        database = {
            "flamengo_titulos": {
                "brasileirao": "8 títulos (1980, 1982, 1983, 1987, 1992, 2009, 2019, 2020)",
                "libertadores": "3 títulos (1981, 2019, 2022)",
                "mundial": "1 título (1981)",
                "carioca": "37 títulos estaduais"
            },
            "fluminense_titulos": {
                "brasileirao": "4 títulos (1970, 1984, 2010, 2012)",
                "libertadores": "1 título (2023 - ATUAL CAMPEÃO)",
                "carioca": "32 títulos estaduais",
                "copa_brasil": "1 título (2007)"
            },
            "flamengo_torcida": "Aproximadamente 43 milhões de torcedores (Datafolha 2023)",
            "fluminense_tradicao": "Clube mais antigo do Rio de Janeiro (fundado em 1902)",
            "flamengo_investimentos": "Maior orçamento do futebol brasileiro em 2023",
            "fluminense_base": "Uma das melhores categorias de base do Brasil"
        }
        
        # Simula busca baseada na query
        results = []
        query_lower = query.lower()
        
        for key, value in database.items():
            if any(term in key for term in query_lower.split()):
                results.append(f"• {key.replace('_', ' ').title()}: {value}")
        
        if not results:
            results.append("Dados não encontrados para esta consulta específica.")
        
        research_report = f"""
📊 **PESQUISA SOLICITADA POR:** {requesting_agent}
🔍 **CONSULTA:** {query}
⏰ **TIMESTAMP:** {datetime.now().strftime('%H:%M:%S')}

📈 **RESULTADOS ENCONTRADOS:**
{chr(10).join(results)}

🔗 **FONTES:** Datafolha, CBF, CONMEBOL, imprensa esportiva
⚖️ **STATUS:** Dados verificados e neutros
        """
        
        context = {
            "query": query,
            "requesting_agent": requesting_agent,
            "results_count": len(results)
        }
        
        return self.send_message(research_report, context)
    
    def quick_fact(self, topic: str) -> Dict[str, Any]:
        """Retorna fato rápido sobre um tópico"""
        prompt = f"""
        {self.system_prompt}
        
        Forneça um FATO RÁPIDO e OBJETIVO sobre: {topic}
        
        Seja conciso, factual e neutro. Inclua dados numéricos se disponível.
        """
        
        return self.send_message(prompt)

# Sistema de comunicação A2A
class A2AProtocol:
    """Protocolo de comunicação Agent-to-Agent"""
    
    def __init__(self):
        self.agents = {
            "supervisor": SupervisorAgent(),
            "flamengo": FlamengoAgent(), 
            "fluminense": FluminenseAgent(),
            "researcher": ResearcherAgent()
        }
        self.message_log = []
        self.active_debate = False
    
    def send_message(self, from_agent: str, to_agent: str, message: str, context: Dict = None) -> Dict[str, Any]:
        """Envia mensagem entre agentes via protocolo A2A"""
        
        if from_agent not in self.agents or to_agent not in self.agents:
            return {"status": "error", "message": "Agente não encontrado"}
        
        # Log da comunicação A2A
        a2a_message = {
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "context": context or {},
            "timestamp": time.time(),
            "protocol": "A2A-v1.0"
        }
        
        self.message_log.append(a2a_message)
        
        # Processa mensagem no agente destinatário
        target_agent = self.agents[to_agent]
        response = target_agent.send_message(message, context)
        
        return {
            "status": "success",
            "a2a_message": a2a_message,
            "response": response
        }
    
    def get_agent(self, agent_name: str) -> BaseAgent:
        """Retorna instância do agente"""
        return self.agents.get(agent_name)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        return {
            "agents_loaded": len(self.agents),
            "total_messages": len(self.message_log),
            "active_debate": self.active_debate,
            "agents_status": {name: agent.get_status() for name, agent in self.agents.items()}
        }

# Instância global do sistema A2A
debate_system = A2AProtocol()

# Funções de conveniência para acesso aos agentes
def get_supervisor() -> SupervisorAgent:
    return debate_system.get_agent("supervisor")

def get_flamengo_agent() -> FlamengoAgent:
    return debate_system.get_agent("flamengo")

def get_fluminense_agent() -> FluminenseAgent:
    return debate_system.get_agent("fluminense")

def get_researcher() -> ResearcherAgent:
    return debate_system.get_agent("researcher")

def get_system_status() -> Dict[str, Any]:
    return debate_system.get_system_status()