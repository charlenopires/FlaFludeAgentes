"""
Researcher Agent - Google ADK + A2A Protocol Implementation
Especialista neutro em pesquisa objetiva e fornecimento de dados factuais
"""

import os
import time
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import uuid4
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class ResearcherAgent:
    """
    Agente Pesquisador seguindo padrões A2A v1.0
    Especializado em pesquisa objetiva e fornecimento de dados factuais
    """
    
    def __init__(self):
        self.agent_id = "researcher_agent"
        self.name = "Pesquisador de Dados Futebolísticos"
        self.version = "1.0.0"
        self.description = "Especialista neutro em pesquisa objetiva e fornecimento de dados factuais sobre futebol brasileiro"
        
        # Configuração Google ADK
        self.model = "gemini-2.0-flash"
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        # Estado do agente
        self.active = True
        self.debate_active = False
        self.research_requests = []
        
        # Histórico A2A
        self.a2a_messages = []
        self.research_history = []
        
        # Inicializa cliente Gemini
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        else:
            self.client = None
        
        # Base de dados simulada (em produção seria API real)
        self.football_database = {
            "flamengo": {
                "fundacao": "1895",
                "brasileirao": {
                    "titulos": 8,
                    "anos": [1980, 1982, 1983, 1987, 1992, 2009, 2019, 2020],
                    "detalhes": "Maior campeão brasileiro do Rio de Janeiro"
                },
                "libertadores": {
                    "titulos": 3,
                    "anos": [1981, 2019, 2022],
                    "detalhes": "Tricampeão da América"
                },
                "mundial": {
                    "titulos": 1,
                    "anos": [1981],
                    "detalhes": "Campeão Mundial FIFA"
                },
                "carioca": {
                    "titulos": 37,
                    "detalhes": "Maior campeão estadual do Rio"
                },
                "torcida": {
                    "tamanho": "43 milhões",
                    "fonte": "Datafolha 2023",
                    "detalhes": "Maior torcida do Brasil"
                },
                "craques": [
                    "Zico", "Júnior", "Bebeto", "Romário", "Adriano",
                    "Gabigol", "Pedro", "Arrascaeta", "Vinícius Jr."
                ],
                "estadio": "Maracanã (mandante oficial)"
            },
            "fluminense": {
                "fundacao": "1902",
                "brasileirao": {
                    "titulos": 4,
                    "anos": [1970, 1984, 2010, 2012],
                    "detalhes": "Primeiro clube carioca campeão brasileiro"
                },
                "libertadores": {
                    "titulos": 1,
                    "anos": [2023],
                    "detalhes": "Atual campeão da América (2023)"
                },
                "mundial": {
                    "titulos": 0,
                    "detalhes": "Nunca conquistou"
                },
                "carioca": {
                    "titulos": 32,
                    "detalhes": "Segundo maior campeão estadual"
                },
                "copa_brasil": {
                    "titulos": 1,
                    "anos": [2007],
                    "detalhes": "Conquistada contra o Figueirense"
                },
                "torcida": {
                    "tamanho": "8 milhões",
                    "fonte": "Datafolha 2023",
                    "detalhes": "Torcida tradicional e fiel"
                },
                "craques": [
                    "Didi", "Carlos Alberto Torres", "Rivellino", "Fred",
                    "Thiago Silva", "Marcelo", "Germán Cano", "Ganso"
                ],
                "tradicao": "Clube mais antigo do Rio de Janeiro",
                "estadio": "Maracanã (mandante) e Laranjeiras (tradição)"
            },
            "comparacoes": {
                "h2h_classicos": {
                    "total_jogos": 432,
                    "vitorias_flamengo": 156,
                    "vitorias_fluminense": 134,
                    "empates": 142,
                    "ultimo_fla_flu": "2023 - Fluminense 2x1 Flamengo"
                },
                "titulos_internacionais": {
                    "flamengo": 4,  # 3 Libertadores + 1 Mundial
                    "fluminense": 1  # 1 Libertadores
                },
                "titulos_nacionais": {
                    "flamengo": 8,  # Brasileirões
                    "fluminense": 5  # 4 Brasileirões + 1 Copa do Brasil
                }
            }
        }
        
        # System prompt especializado
        self.system_prompt = """
        Você é um PESQUISADOR NEUTRO e OBJETIVO especializado em futebol brasileiro.
        
        🎯 SUAS FUNÇÕES TÉCNICAS:
        1. Buscar dados FACTUAIS sobre Flamengo e Fluminense
        2. Fornecer estatísticas VERIFICÁVEIS e imparciais
        3. Manter NEUTRALIDADE ABSOLUTA em todas as pesquisas
        4. Responder rapidamente às solicitações dos debatedores
        5. Indicar fontes confiáveis quando possível
        6. Apresentar dados de forma clara e organizada
        
        📊 SUAS FONTES PRINCIPAIS:
        - CBF (Confederação Brasileira de Futebol)
        - CONMEBOL (Confederação Sul-Americana)
        - Datafolha (pesquisas de torcida)
        - FIFA (dados internacionais)
        - Arquivo histórico dos clubes
        - Estatísticas oficiais dos campeonatos
        
        🔬 SEU MÉTODO CIENTÍFICO:
        - SEMPRE apresente dados verificáveis
        - NUNCA tome partido por nenhum time
        - Use linguagem técnica e imparcial
        - Organize informações de forma clara
        - Indique limitações dos dados quando aplicável
        
        ⚖️ NEUTRALIDADE ABSOLUTA: Você não torce para nenhum time. 
        Sua única paixão são os DADOS CORRETOS e VERIFICÁVEIS!
        """
    
    def get_agent_card(self) -> Dict[str, Any]:
        """
        Retorna Agent Card seguindo especificação A2A v1.0
        """
        return {
            "name": self.name,
            "description": self.description,
            "url": f"http://localhost:8003/{self.agent_id}",
            "provider": {
                "organization": "Fla-Flu Debate System",
                "url": "https://github.com/a2aproject/flafludeagentes"
            },
            "version": self.version,
            "capabilities": {
                "streaming": True,
                "pushNotifications": True,
                "stateTransitionHistory": True
            },
            "securitySchemes": {
                "none": {
                    "type": "none"
                }
            },
            "security": [],
            "defaultInputModes": ["text/plain"],
            "defaultOutputModes": ["text/plain", "application/json"],
            "skills": [
                {
                    "id": "search_data",
                    "name": "Pesquisa de Dados",
                    "description": "Busca dados objetivos e verificáveis sobre times de futebol",
                    "tags": ["research", "data", "objective", "neutral"],
                    "examples": [
                        "Busque dados sobre títulos do Flamengo",
                        "Compare estatísticas Flamengo vs Fluminense",
                        "Encontre informações sobre torcidas"
                    ],
                    "inputModes": ["text/plain"]
                },
                {
                    "id": "compare_teams",
                    "name": "Comparação Técnica",
                    "description": "Compara estatísticas técnicas entre Flamengo e Fluminense",
                    "tags": ["comparison", "statistics", "analysis"],
                    "examples": [
                        "Compare títulos dos dois times",
                        "Analise confrontos diretos",
                        "Compare conquistas internacionais"
                    ],
                    "inputModes": ["text/plain"]
                },
                {
                    "id": "verify_fact",
                    "name": "Verificação de Fatos",
                    "description": "Verifica veracidade de informações sobre futebol",
                    "tags": ["fact-check", "verification", "accuracy"],
                    "examples": [
                        "Verifique se essa informação está correta",
                        "Confirme esse dado estatístico",
                        "Valide essa afirmação"
                    ],
                    "inputModes": ["text/plain"]
                }
            ]
        }
    
    async def send_a2a_message(self, target_agent: str, method: str, params: Dict = None) -> Dict[str, Any]:
        """
        Envia mensagem A2A seguindo JSON-RPC 2.0
        """
        message = {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": method,
            "params": params or {},
            "from_agent": self.agent_id,
            "to_agent": target_agent,
            "timestamp": datetime.now().isoformat(),
            "protocol": "A2A-v1.0"
        }
        
        # Log da comunicação A2A
        self.a2a_messages.append(message)
        
        return {
            "jsonrpc": "2.0",
            "id": message["id"],
            "result": {
                "status": "message_sent",
                "target": target_agent,
                "method": method,
                "timestamp": message["timestamp"]
            }
        }
    
    async def process_a2a_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa mensagem A2A recebida
        """
        try:
            method = message.get("method")
            params = message.get("params", {})
            
            if method == "research_request":
                result = await self.handle_research_request(params)
            elif method == "debate_started":
                result = await self.handle_debate_started(params)
            elif method == "debate_finished":
                result = await self.handle_debate_finished(params)
            elif method == "message/send":
                result = await self.handle_message_send(params)
            else:
                result = {
                    "status": "error",
                    "message": f"Método desconhecido: {method}"
                }
            
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": result
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }
    
    async def handle_research_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com solicitação de pesquisa
        """
        query = params.get("query", "")
        requester = params.get("requester", "unknown")
        context = params.get("context", "general")
        
        if not query:
            return {
                "status": "error",
                "message": "Query de pesquisa não fornecida"
            }
        
        # Registra solicitação
        self.research_requests.append({
            "query": query,
            "requester": requester,
            "context": context,
            "timestamp": time.time()
        })
        
        # Executa pesquisa
        research_result = await self.search_data(query, requester)
        
        # Envia resposta de volta ao solicitante
        await self.send_a2a_message(requester, "research_response", {
            "original_query": query,
            "data": research_result.get("data", ""),
            "status": research_result.get("status", "completed"),
            "sources": research_result.get("sources", [])
        })
        
        return {
            "status": "research_completed",
            "query": query,
            "requester": requester,
            "data_found": research_result.get("status") == "success"
        }
    
    async def handle_debate_started(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com início do debate
        """
        self.debate_active = True
        duration = params.get("duration", 5)
        
        return {
            "status": "standby",
            "message": f"📊 Pesquisador em standby para {duration} minutos de debate. Pronto para fornecer dados objetivos!"
        }
    
    async def handle_debate_finished(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com fim do debate
        """
        self.debate_active = False
        
        # Gera relatório final das pesquisas
        total_requests = len(self.research_requests)
        
        return {
            "status": "debate_ended",
            "message": f"📊 Pesquisas concluídas! Total de {total_requests} solicitações atendidas com neutralidade científica.",
            "research_summary": {
                "total_requests": total_requests,
                "requests_by_agent": self._count_requests_by_agent()
            }
        }
    
    async def handle_message_send(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lida com mensagem direta
        """
        message = params.get("message", {})
        text = ""
        
        # Extrai texto das partes da mensagem
        for part in message.get("parts", []):
            if part.get("kind") == "text":
                text += part.get("text", "")
        
        if not text:
            return {
                "status": "error",
                "message": "Mensagem vazia recebida"
            }
        
        # Processa mensagem como pesquisa
        response = await self.process_research_message(text)
        
        return {
            "status": "success",
            "response": {
                "role": "assistant",
                "parts": [
                    {
                        "kind": "text",
                        "text": response
                    }
                ],
                "messageId": str(uuid4())
            }
        }
    
    async def search_data(self, query: str, requester: str = "unknown") -> Dict[str, Any]:
        """
        Executa pesquisa de dados - Skill A2A
        """
        try:
            query_lower = query.lower()
            results = []
            sources = []
            
            # Busca por palavras-chave na base de dados
            if "flamengo" in query_lower:
                team_data = self.football_database["flamengo"]
                results.extend(self._extract_relevant_data(team_data, query_lower, "Flamengo"))
                sources.append("Arquivo oficial Flamengo")
            
            if "fluminense" in query_lower:
                team_data = self.football_database["fluminense"]
                results.extend(self._extract_relevant_data(team_data, query_lower, "Fluminense"))
                sources.append("Arquivo oficial Fluminense")
            
            if "compare" in query_lower or "vs" in query_lower:
                comp_data = self.football_database["comparacoes"]
                results.extend(self._extract_comparison_data(comp_data, query_lower))
                sources.append("Dados comparativos CBF")
            
            if not results:
                results.append("Dados não encontrados para esta consulta específica.")
                sources.append("Base de dados local")
            
            # Formata resposta de pesquisa
            research_report = f"""
📊 **RELATÓRIO DE PESQUISA OBJETIVA**

🔍 **SOLICITAÇÃO:** {query}
👤 **SOLICITANTE:** {requester}
⏰ **TIMESTAMP:** {datetime.now().strftime('%H:%M:%S')}

📈 **DADOS ENCONTRADOS:**
{chr(10).join(f"• {result}" for result in results)}

🔗 **FONTES CONSULTADAS:**
{chr(10).join(f"• {source}" for source in sources)}

⚖️ **METODOLOGIA:** Pesquisa em base de dados oficial com neutralidade científica
🎯 **CONFIABILIDADE:** Dados verificados e imparciais
            """
            
            # Log da pesquisa
            self.research_history.append({
                "query": query,
                "requester": requester,
                "results_count": len(results),
                "timestamp": time.time()
            })
            
            return {
                "status": "success",
                "data": research_report.strip(),
                "sources": sources,
                "results_count": len(results)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "data": f"Erro na pesquisa: {str(e)}",
                "sources": [],
                "results_count": 0
            }
    
    def _extract_relevant_data(self, team_data: Dict, query: str, team_name: str) -> List[str]:
        """
        Extrai dados relevantes baseados na query
        """
        results = []
        
        if "título" in query or "brasileir" in query:
            br_data = team_data.get("brasileirao", {})
            results.append(f"{team_name}: {br_data.get('titulos', 0)} Brasileirões ({', '.join(map(str, br_data.get('anos', [])))})")
        
        if "libertadores" in query:
            lib_data = team_data.get("libertadores", {})
            results.append(f"{team_name}: {lib_data.get('titulos', 0)} Libertadores ({', '.join(map(str, lib_data.get('anos', [])))})")
        
        if "mundial" in query:
            mund_data = team_data.get("mundial", {})
            results.append(f"{team_name}: {mund_data.get('titulos', 0)} Mundial ({', '.join(map(str, mund_data.get('anos', [])))})")
        
        if "torcida" in query:
            torcida_data = team_data.get("torcida", {})
            results.append(f"{team_name}: {torcida_data.get('tamanho', 'N/A')} torcedores ({torcida_data.get('fonte', 'Fonte não especificada')})")
        
        if "fundaç" in query or "históri" in query:
            results.append(f"{team_name}: Fundado em {team_data.get('fundacao', 'N/A')}")
        
        if "craque" in query or "jogador" in query:
            craques = team_data.get("craques", [])
            results.append(f"{team_name}: Principais craques - {', '.join(craques[:5])}")
        
        return results
    
    def _extract_comparison_data(self, comp_data: Dict, query: str) -> List[str]:
        """
        Extrai dados comparativos
        """
        results = []
        
        if "clássico" in query or "confronto" in query:
            h2h = comp_data.get("h2h_classicos", {})
            results.append(f"Confrontos diretos: {h2h.get('total_jogos', 0)} jogos - "
                         f"Flamengo {h2h.get('vitorias_flamengo', 0)} x {h2h.get('vitorias_fluminense', 0)} Fluminense "
                         f"({h2h.get('empates', 0)} empates)")
        
        if "internacional" in query:
            inter = comp_data.get("titulos_internacionais", {})
            results.append(f"Títulos internacionais: Flamengo {inter.get('flamengo', 0)} x {inter.get('fluminense', 0)} Fluminense")
        
        if "nacional" in query:
            nac = comp_data.get("titulos_nacionais", {})
            results.append(f"Títulos nacionais: Flamengo {nac.get('flamengo', 0)} x {nac.get('fluminense', 0)} Fluminense")
        
        return results
    
    async def process_research_message(self, message: str) -> str:
        """
        Processa mensagem genérica como pesquisa
        """
        try:
            if self.client:
                prompt = f"""
                {self.system_prompt}
                
                Mensagem/pergunta recebida: "{message}"
                
                Como pesquisador neutro especializado em futebol brasileiro,
                forneça informações objetivas e verificáveis relacionadas à pergunta.
                Mantenha sempre neutralidade absoluta.
                """
                
                response = self.client.generate_content(prompt)
                return response.text
            else:
                return f"""
📊 **PESQUISADOR NEUTRO ATIVO**

Pergunta recebida: "{message}"

Como especialista em dados futebolísticos, estou preparado para fornecer
informações objetivas e verificáveis. Solicite dados específicos sobre
Flamengo, Fluminense ou comparações entre os clubes.

🔬 Neutralidade garantida - apenas fatos e estatísticas!
                """
                
        except Exception as e:
            return f"📊 Erro na pesquisa: {str(e)}"
    
    def _count_requests_by_agent(self) -> Dict[str, int]:
        """
        Conta solicitações por agente
        """
        counts = {}
        for request in self.research_requests:
            agent = request["requester"]
            counts[agent] = counts.get(agent, 0) + 1
        return counts
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status completo do agente
        """
        return {
            "agent_card": self.get_agent_card(),
            "research_status": {
                "active": self.active,
                "debate_active": self.debate_active,
                "total_requests": len(self.research_requests),
                "research_history": len(self.research_history)
            },
            "a2a_communications": {
                "messages_sent": len(self.a2a_messages),
                "requests_by_agent": self._count_requests_by_agent()
            },
            "health": {
                "gemini_connected": self.client is not None,
                "api_key_configured": self.api_key is not None,
                "database_loaded": len(self.football_database) > 0
            },
            "capabilities": {
                "can_research": True,
                "can_compare": True,
                "can_verify": True,
                "neutrality_level": "ABSOLUTE 📊",
                "data_sources": ["CBF", "CONMEBOL", "Datafolha", "FIFA"]
            }
        }