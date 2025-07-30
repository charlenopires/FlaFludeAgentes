"""
Evaluation module for debate agent performance
Following ADK evaluation patterns
"""

from typing import Dict, Any, List
import json
import time
from datetime import datetime

class DebateEvaluator:
    """Evaluates debate agent performance and quality"""
    
    def __init__(self):
        self.evaluation_criteria = {
            "argument_quality": {
                "weight": 0.4,
                "description": "Quality and coherence of arguments"
            },
            "factual_accuracy": {
                "weight": 0.3, 
                "description": "Use of accurate data and statistics"
            },
            "persuasive_power": {
                "weight": 0.2,
                "description": "Ability to convince and engage"
            },
            "respectfulness": {
                "weight": 0.1,
                "description": "Maintaining respectful discourse"
            }
        }
    
    def evaluate_agent_performance(self, agent_name: str, messages: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluates individual agent performance in debate
        
        Args:
            agent_name: Name of the agent being evaluated
            messages: List of messages from the agent
            context: Additional context for evaluation
            
        Returns:
            dict: Evaluation results with scores and analysis
        """
        try:
            if not messages:
                return {
                    "status": "error",
                    "error_message": "No messages to evaluate"
                }
            
            # Calculate metrics
            total_words = sum(len(msg.split()) for msg in messages)
            avg_message_length = total_words / len(messages)
            
            # Evaluate different aspects
            scores = {}
            
            # Argument Quality (0-100)
            quality_indicators = ["porque", "pois", "devido", "evidência", "prova", "exemplo"]
            quality_score = min(100, sum(sum(1 for indicator in quality_indicators if indicator in msg.lower()) for msg in messages) * 10)
            scores["argument_quality"] = quality_score
            
            # Factual Accuracy (0-100) 
            fact_indicators = ["título", "ano", "estatística", "número", "dados", "história"]
            factual_score = min(100, sum(sum(1 for indicator in fact_indicators if indicator in msg.lower()) for msg in messages) * 8)
            scores["factual_accuracy"] = factual_score
            
            # Persuasive Power (0-100)
            persuasive_indicators = ["melhor", "superior", "único", "maior", "vencedor", "campeão"]
            persuasive_score = min(100, sum(sum(1 for indicator in persuasive_indicators if indicator in msg.lower()) for msg in messages) * 6)
            scores["persuasive_power"] = persuasive_score
            
            # Respectfulness (0-100) - starts at 100, deductions for negative language
            negative_indicators = ["idiota", "burro", "lixo", "vergonha"]
            respect_deductions = sum(sum(1 for indicator in negative_indicators if indicator in msg.lower()) for msg in messages) * 20
            scores["respectfulness"] = max(0, 100 - respect_deductions)
            
            # Calculate weighted overall score
            overall_score = sum(
                scores[criterion] * self.evaluation_criteria[criterion]["weight"] 
                for criterion in scores
            )
            
            # Generate detailed report
            performance_level = "EXCELENTE" if overall_score >= 80 else "BOM" if overall_score >= 60 else "REGULAR" if overall_score >= 40 else "PRECISA MELHORAR"
            
            evaluation_report = f"""
📊 AVALIAÇÃO DE PERFORMANCE - {agent_name.upper()}

🎯 PONTUAÇÃO GERAL: {overall_score:.1f}/100 - {performance_level}

📈 ANÁLISE POR CRITÉRIO:
• Qualidade dos Argumentos: {scores['argument_quality']}/100 (Peso: 40%)
• Precisão Factual: {scores['factual_accuracy']}/100 (Peso: 30%)
• Poder Persuasivo: {scores['persuasive_power']}/100 (Peso: 20%)
• Respeitabilidade: {scores['respectfulness']}/100 (Peso: 10%)

📏 MÉTRICAS ADICIONAIS:
• Total de mensagens: {len(messages)}
• Total de palavras: {total_words:,}
• Média de palavras por mensagem: {avg_message_length:.1f}

💡 RECOMENDAÇÕES:
{self._generate_recommendations(scores, overall_score)}

⭐ DESTAQUE: {self._identify_strength(scores)}

📅 Avaliação realizada em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            """
            
            return {
                "status": "success",
                "report": evaluation_report.strip(),
                "scores": scores,
                "overall_score": overall_score,
                "performance_level": performance_level
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Erro na avaliação: {str(e)}"
            }
    
    def _generate_recommendations(self, scores: Dict[str, float], overall_score: float) -> str:
        """Generate improvement recommendations based on scores"""
        recommendations = []
        
        if scores["argument_quality"] < 60:
            recommendations.append("Desenvolver argumentos mais estruturados com exemplos")
        
        if scores["factual_accuracy"] < 60:
            recommendations.append("Incluir mais dados e estatísticas verificáveis")
        
        if scores["persuasive_power"] < 60:
            recommendations.append("Usar linguagem mais convincente e emotiva")
        
        if scores["respectfulness"] < 80:
            recommendations.append("Manter sempre o respeito e civilidade")
        
        if not recommendations:
            recommendations.append("Excelente performance! Continue assim!")
        
        return "\n".join(f"  • {rec}" for rec in recommendations)
    
    def _identify_strength(self, scores: Dict[str, float]) -> str:
        """Identify the agent's strongest area"""
        max_score = max(scores.values())
        strengths = [criterion for criterion, score in scores.items() if score == max_score]
        
        strength_names = {
            "argument_quality": "Qualidade argumentativa",
            "factual_accuracy": "Precisão factual", 
            "persuasive_power": "Poder de persuasão",
            "respectfulness": "Respeitabilidade"
        }
        
        return strength_names.get(strengths[0], "Desempenho equilibrado")
    
    def evaluate_debate_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates entire debate session with all agents
        
        Args:
            session_data: Complete session data with all agent interactions
            
        Returns:
            dict: Session evaluation results
        """
        try:
            agents_data = session_data.get("agents", {})
            
            if not agents_data:
                return {
                    "status": "error",
                    "error_message": "Dados de sessão inválidos"
                }
            
            # Evaluate each agent
            agent_evaluations = {}
            for agent_name, messages in agents_data.items():
                evaluation = self.evaluate_agent_performance(agent_name, messages)
                if evaluation["status"] == "success":
                    agent_evaluations[agent_name] = evaluation
            
            # Determine session winner
            if agent_evaluations:
                winner = max(agent_evaluations.keys(), 
                           key=lambda agent: agent_evaluations[agent]["overall_score"])
                winner_score = agent_evaluations[winner]["overall_score"]
            else:
                winner = "Nenhum"
                winner_score = 0
            
            # Generate session report
            session_report = f"""
🏆 AVALIAÇÃO COMPLETA DA SESSÃO DE DEBATE

👑 VENCEDOR: {winner.upper()} (Pontuação: {winner_score:.1f})

📊 RANKING DOS AGENTES:
"""
            
            # Add ranking
            sorted_agents = sorted(agent_evaluations.items(), 
                                 key=lambda x: x[1]["overall_score"], 
                                 reverse=True)
            
            for i, (agent, eval_data) in enumerate(sorted_agents, 1):
                session_report += f"{i}º lugar: {agent} - {eval_data['overall_score']:.1f} pontos ({eval_data['performance_level']})\n"
            
            session_report += f"""
📈 ESTATÍSTICAS GERAIS:
• Duração da sessão: {session_data.get('duration', 'N/A')}
• Total de agentes: {len(agent_evaluations)}
• Pontuação média: {sum(eval_data['overall_score'] for eval_data in agent_evaluations.values()) / len(agent_evaluations):.1f}

🎯 QUALIDADE GERAL DO DEBATE: {self._assess_session_quality(agent_evaluations)}

📅 Sessão avaliada em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            """
            
            return {
                "status": "success",
                "report": session_report.strip(),
                "winner": winner,
                "winner_score": winner_score,
                "agent_evaluations": agent_evaluations
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "error_message": f"Erro na avaliação da sessão: {str(e)}"
            }
    
    def _assess_session_quality(self, evaluations: Dict[str, Dict]) -> str:
        """Assess overall session quality"""
        avg_score = sum(eval_data["overall_score"] for eval_data in evaluations.values()) / len(evaluations)
        
        if avg_score >= 80:
            return "EXCELENTE - Debate de alto nível"
        elif avg_score >= 60:
            return "BOA - Debate interessante e bem fundamentado"
        elif avg_score >= 40:
            return "REGULAR - Debate com potencial de melhoria"
        else:
            return "PRECISA MELHORAR - Argumentação básica"

# Example usage
if __name__ == "__main__":
    evaluator = DebateEvaluator()
    
    # Example evaluation
    sample_messages = [
        "Flamengo é o maior clube do Brasil porque tem 8 títulos brasileiros e a maior torcida",
        "Os dados mostram que nossa história de conquistas é superior, com títulos em 2019 e 2020"
    ]
    
    result = evaluator.evaluate_agent_performance("Torcedor do Flamengo", sample_messages)
    print(json.dumps(result, indent=2, ensure_ascii=False))