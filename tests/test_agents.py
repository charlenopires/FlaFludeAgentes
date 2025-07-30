"""
Test suite for ADK debate agents
Following ADK testing patterns
"""

import pytest
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from debate_system.agent import (
    get_team_statistics,
    analyze_argument_strength,
    generate_counter_argument,
    moderate_debate_session,
    create_supervisor_agent,
    create_flamengo_agent,
    create_fluminense_agent,
    create_researcher_agent
)

class TestTeamStatistics:
    """Test team statistics tool"""
    
    def test_flamengo_statistics(self):
        """Test Flamengo statistics retrieval"""
        result = get_team_statistics("Flamengo", "titles")
        
        assert result["status"] == "success"
        assert "Flamengo" in result["report"]
        assert "brasileirao" in result["report"].lower()
    
    def test_fluminense_statistics(self):
        """Test Fluminense statistics retrieval"""
        result = get_team_statistics("Fluminense", "history")
        
        assert result["status"] == "success"
        assert "Fluminense" in result["report"]
        assert "1902" in result["report"]
    
    def test_invalid_team(self):
        """Test invalid team handling"""
        result = get_team_statistics("InvalidTeam")
        
        assert result["status"] == "error"
        assert "não reconhecido" in result["error_message"]

class TestArgumentAnalysis:
    """Test argument analysis tool"""
    
    def test_strong_argument(self):
        """Test analysis of strong argument"""
        strong_arg = "Flamengo é o maior clube do Brasil com 8 títulos brasileiros, maior torcida do país e uma história de paixão que emociona milhões de torcedores apaixonados"
        
        result = analyze_argument_strength(strong_arg, "Flamengo")
        
        assert result["status"] == "success"
        assert "FORTE" in result["report"] or "MODERADO" in result["report"]
    
    def test_weak_argument(self):
        """Test analysis of weak argument"""
        weak_arg = "Time bom mesmo, muito bom, gosto muito deste time"
        
        result = analyze_argument_strength(weak_arg)
        
        assert result["status"] == "success"
        assert "FRACO" in result["report"]
    
    def test_empty_argument(self):
        """Test empty argument handling"""
        result = analyze_argument_strength("")
        
        assert result["status"] == "error"
        assert "muito curto" in result["error_message"]

class TestCounterArguments:
    """Test counter-argument generation"""
    
    def test_counter_flamengo(self):
        """Test counter-argument against Flamengo"""
        flamengo_arg = "Flamengo tem a maior torcida do Brasil"
        
        result = generate_counter_argument(flamengo_arg, "Flamengo")
        
        assert result["status"] == "success"
        assert "Fluminense" in result["report"]
        assert "CONTRA-ATAQUE" in result["report"]
    
    def test_counter_fluminense(self):
        """Test counter-argument against Fluminense"""
        flu_arg = "Fluminense tem mais tradição e história"
        
        result = generate_counter_argument(flu_arg, "Fluminense")
        
        assert result["status"] == "success" 
        assert "Flamengo" in result["report"]
        assert "CONTRA-ATAQUE" in result["report"]
    
    def test_empty_argument_counter(self):
        """Test counter-argument with empty input"""
        result = generate_counter_argument("", "Flamengo")
        
        assert result["status"] == "error"
        assert "necessário" in result["error_message"]

class TestDebateModeration:
    """Test debate moderation tool"""
    
    def test_start_debate(self):
        """Test debate session start"""
        result = moderate_debate_session("start", duration_minutes=5)
        
        assert result["status"] == "success"
        assert "SESSÃO DE DEBATE" in result["report"]
        assert "5 minutos" in result["report"]
    
    def test_invalid_duration(self):
        """Test invalid duration handling"""
        result = moderate_debate_session("start", duration_minutes=50)
        
        assert result["status"] == "error"
        assert "entre 1 e 30" in result["error_message"]
    
    def test_debate_status(self):
        """Test debate status check"""
        result = moderate_debate_session("status", remaining_seconds=120, interactions=5)
        
        assert result["status"] == "success"
        assert "02:00" in result["report"]
        assert "5" in result["report"]
    
    def test_debate_analysis(self):
        """Test final debate analysis"""
        transcript = "Flamengo é o melhor time do Brasil. Fluminense tem tradição mas Flamengo tem títulos."
        
        result = moderate_debate_session("analyze", transcript=transcript)
        
        assert result["status"] == "success"
        assert "ANÁLISE FINAL" in result["report"]
        assert "FLAMENGO" in result["report"] or "FLUMINENSE" in result["report"]

class TestAgentCreation:
    """Test agent factory functions"""
    
    def test_supervisor_agent_creation(self):
        """Test supervisor agent creation"""
        agent = create_supervisor_agent()
        
        assert agent["name"] == "supervisor"
        assert agent["model"] == "gemini-2.0-flash"
        assert "retórica" in agent["description"]
        assert len(agent["tools"]) >= 2
    
    def test_flamengo_agent_creation(self):
        """Test Flamengo agent creation"""
        agent = create_flamengo_agent()
        
        assert agent["name"] == "flamengo_fan"
        assert "Flamengo" in agent["description"]
        assert len(agent["tools"]) >= 3
    
    def test_fluminense_agent_creation(self):
        """Test Fluminense agent creation"""
        agent = create_fluminense_agent()
        
        assert agent["name"] == "fluminense_fan"
        assert "Fluminense" in agent["description"]
        assert len(agent["tools"]) >= 3
    
    def test_researcher_agent_creation(self):
        """Test researcher agent creation"""
        agent = create_researcher_agent()
        
        assert agent["name"] == "researcher"
        assert "objetiva" in agent["description"]
        assert len(agent["tools"]) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])