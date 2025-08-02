# 🔥 FlaFludeAgentes: Sistema Multi-Agente A2A

Sistema inteligente de debate entre torcedores do Flamengo e Fluminense usando **4 agentes independentes** que se comunicam via **protocolo A2A** (Agent-to-Agent) implementando padrões do **Google ADK**.

## 🎯 **Visão Geral**

Este projeto implementa um sistema de debate automatizado entre Flamengo e Fluminense, onde 4 agentes especializados rodam como servidores A2A independentes e interagem de forma autônoma para criar debates dinâmicos e informativos.

### 🤖 **Os 4 Agentes A2A**

1. **⚖️ Supervisor Agent** (Port 8002): Coordena o debate de forma completamente neutra, gerencia turnos e analisa o vencedor baseado em critérios técnicos de retórica e persuasão
2. **🔴 Flamengo Agent** (Port 8003): Defende o Flamengo com paixão, usando dados e argumentos convincentes
3. **🟢 Fluminense Agent** (Port 8004): Argumenta com elegância sobre a tradição e superioridade tricolor
4. **📊 Researcher Agent** (Port 8005): Fornece dados objetivos e neutros para embasar os argumentos dos torcedores

## 🛠️ **Tecnologias**

- **Google ADK**: Padrões oficiais do Agent Development Kit
- **Protocolo A2A v1.0**: Comunicação Agent-to-Agent com agent cards
- **Google Gemini 2.0 Flash**: LLM para processamento de linguagem natural
- **Streamlit**: Interface web interativa moderna
- **Python 3.8+**: Backend do sistema com asyncio
- **UV**: Gerenciamento de dependências
- **HTTP/JSON**: Comunicação entre agentes via REST APIs

## ⚡ **Funcionalidades**

### 🎬 **Fluxo do Debate**
1. **Inicialização**: Supervisor questiona duração do debate
2. **Configuração**: Tempo dividido igualmente (50% cada time)
3. **Sorteio**: Sistema define qual time inicia (geralmente Flamengo)
4. **Debate**: Agentes alternam argumentos com protocolo A2A
5. **Pesquisa**: Pesquisador fornece dados quando solicitado
6. **Análise**: Supervisor analisa e declara vencedor

### 🎭 **Interface Avançada**
- **Chat em Tempo Real**: Visualização das mensagens dos agentes
- **Bastidores**: Status em tempo real de cada agente
- **Timer**: Cronômetro com tempo restante do debate
- **Log A2A**: Registro das comunicações entre agentes
- **Exportação**: Download da transcrição completa
- **Design Responsivo**: Interface moderna com gradientes e animações

## 🚀 **Como Usar**

### 📋 **Pré-requisitos**
```bash
# Python 3.8+
# UV package manager
# Google API Key (Gemini)
```

### 🔧 **Instalação e Execução**
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/FlaFludeAgentes.git
cd FlaFludeAgentes

# 2. Instale dependências com UV
uv sync

# 3. Inicie os servidores A2A (em um terminal)
uv run python start_a2a_servers.py

# 4. Execute a aplicação Streamlit (em outro terminal)
uv run streamlit run app.py
```

### 🌐 **Acesso e Configuração**
1. **Abra http://localhost:8501** no navegador
2. **Configure sua Google API Key** na interface
3. **Clique em "Inicializar Sistema"** para descobrir agentes A2A
4. **Configure duração do debate** (2-10 minutos)  
5. **Clique em "Iniciar Debate"**
6. **Acompanhe o debate em tempo real**
7. **Veja a análise final do supervisor**

### 🔌 **Servidores A2A Individuais**
Os agentes rodam como servidores independentes:
```bash
# Iniciar agentes individualmente (opcional)
uv run python -m supervisor_agent.agent    # Port 8002
uv run python -m flamengo_agent.agent      # Port 8003  
uv run python -m fluminense_agent.agent    # Port 8004
uv run python -m researcher_agent.agent    # Port 8005
```

### 🕸️ **Agent Discovery**
Cada agente expõe seu Agent Card A2A:
- http://localhost:8002/.well-known/agent.json (Supervisor)
- http://localhost:8003/.well-known/agent.json (Flamengo)
- http://localhost:8004/.well-known/agent.json (Fluminense)
- http://localhost:8005/.well-known/agent.json (Researcher)

## 🔗 **Protocolo A2A**

O sistema implementa comunicação Agent-to-Agent seguindo padrões JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "id": "a2a_1234567890_flamengo_researcher",
  "method": "conduct_research",
  "params": {
    "query": "Flamengo vs Fluminense recent titles comparison",
    "requesting_agent": "flamengo_agent"
  },
  "from_agent": "flamengo_agent",
  "to_agent": "researcher_agent", 
  "timestamp": "2024-01-01T12:00:00Z",
  "protocol": "A2A-v1.0"
}
```

### 📊 **Métricas A2A**
- **Agent Discovery**: Descoberta automática via Agent Cards
- **Message Routing**: Roteamento HTTP entre agentes
- **State Sync**: Sincronização de estado do debate
- **Health Checks**: Monitoramento em tempo real
- **Logging**: Registro completo de comunicações A2A

## 🧠 **Especialidades dos Agentes**

### ⚖️ **Supervisor**
- **Retórica**: Análise da força argumentativa
- **Psicologia**: Impacto persuasivo das mensagens  
- **Linguística**: Qualidade da comunicação
- **Lógica**: Consistência e coerência dos argumentos

### 🔴 **Flamengo**
- **Paixão**: Argumentos emocionais intensos
- **Dados**: Estatísticas de títulos e torcida
- **Provocação**: Inteligência nas provocações
- **Superioridade**: Foco em conquistas recentes

### 🟢 **Fluminense** 
- **Elegância**: Argumentação refinada e culta
- **Tradição**: História centenária do clube
- **Técnica**: Futebol-arte e qualidade
- **Classe**: Postura digna e respeitosa

### 📊 **Pesquisador**
- **Neutralidade**: Imparcialidade absoluta
- **Dados**: Estatísticas verificáveis
- **Fontes**: CBF, CONMEBOL, Datafolha
- **Rapidez**: Respostas ágeis às solicitações

## 📁 **Estrutura do Projeto**

```
FlaFludeAgentes/
├── 🤖 supervisor_agent/
│   ├── __init__.py
│   └── agent.py           # SupervisorAgent - Moderador neutro
├── 🤖 flamengo_agent/
│   ├── __init__.py  
│   └── agent.py           # FlamengoAgent - Torcedor rubro-negro
├── 🤖 fluminense_agent/
│   ├── __init__.py
│   └── agent.py           # FluminenseAgent - Torcedor tricolor
├── 🤖 researcher_agent/
│   ├── __init__.py
│   └── agent.py           # ResearcherAgent - Pesquisador neutro
├── 🚀 start_a2a_servers.py  # Inicia todos os servidores A2A
├── 📱 app.py                # Interface Streamlit principal
├── 🛠️ utils/
│   ├── __init__.py
│   ├── enhanced_logger.py   # Sistema de logging avançado
│   └── log_viewer.py        # Visualizador de logs
├── 📊 logs/                 # Logs do sistema A2A
├── 📋 prompts.py            # Prompts de referência
├── ⚙️ pyproject.toml        # Dependências UV
├── 📖 CLAUDE.md             # Instruções para Claude Code
└── 📄 README.md             # Documentação
```

## 🎯 **Critérios de Avaliação**

O supervisor analisa debates usando:

1. **Força dos Argumentos (40%)**
   - Lógica e coerência
   - Estrutura argumentativa
   - Base factual

2. **Evidências e Dados (30%)**
   - Uso de estatísticas
   - Fontes confiáveis  
   - Precisão das informações

3. **Persuasão e Retórica (20%)**
   - Impacto emocional
   - Técnicas persuasivas
   - Capacidade de convencimento

4. **Consistência Lógica (10%)**
   - Ausência de contradições
   - Fluxo argumentativo
   - Resposta aos oponentes

## 🔬 **Desenvolvimento e Testes**

```bash
# Teste do sistema de logging
uv run python test_logging_system.py

# Visualizar logs em tempo real
uv run python -m utils.log_viewer

# Verificar conectividade dos agentes A2A
curl http://localhost:8002/.well-known/agent.json
curl http://localhost:8003/.well-known/agent.json
curl http://localhost:8004/.well-known/agent.json
curl http://localhost:8005/.well-known/agent.json
```

## 🚀 **Recursos Avançados**

### 📊 **Sistema de Logging**
- **Enhanced Logger**: Sistema de logging estruturado
- **Separação por Categoria**: Logs de A2A, agentes e sistema
- **Rotação Diária**: Arquivos organizados por data
- **Log Viewer**: Visualização em tempo real

### 🔧 **Monitoramento**
- **Health Checks**: Status de cada agente A2A
- **Message Tracking**: Rastreamento de mensagens entre agentes
- **Performance Metrics**: Latência e throughput
- **Error Handling**: Tratamento robusto de erros

## 📊 **Exemplos de Uso**

### 🎬 **Debate Típico**
```
⚖️ Supervisor: "Debate de 5 minutos iniciado! Flamengo começa!"

🔴 Flamengo: "Somos o MAIOR do Brasil! 8 Brasileirões, maior torcida..."

🟢 Fluminense: "Tradição centenária! CAMPEÕES DA LIBERTADORES 2023!"

📊 Pesquisador: "Dados: Flamengo 8 títulos BR, Fluminense atual campeão..."

⚖️ Supervisor: "Análise final: Fluminense vence por uso superior de dados recentes!"
```

### 🔗 **Comunicação A2A**
```python
# Flamengo solicita pesquisa via A2A
POST http://localhost:8005/run
{
  "jsonrpc": "2.0",
  "method": "conduct_research",
  "params": {
    "query": "estatísticas de público no Maracanã",
    "requesting_agent": "flamengo_agent"
  },
  "id": "research_request_001"
}
```

### 🌐 **Agent Cards**
```json
# Exemplo: http://localhost:8003/.well-known/agent.json
{
  "agent_id": "flamengo_agent",
  "name": "Torcedor Flamengo",
  "description": "Agente especializado em defender o Flamengo",
  "capabilities": ["initial_argument", "counter_argument", "request_research"],
  "version": "1.0.0",
  "protocol": "A2A-v1.0"
}
```

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Add nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📜 **Licença**

Este projeto está sob a licença MIT. Veja `LICENSE` para detalhes.

## 🏆 **Funcionalidades Implementadas**

- ✅ **4 Agentes A2A Independentes** em servidores separados
- ✅ **Protocolo A2A v1.0** com Agent Cards e JSON-RPC 2.0
- ✅ **Google ADK** padrões oficiais implementados
- ✅ **Interface Streamlit** moderna e responsiva
- ✅ **Sistema de Logging** avançado com rotação diária
- ✅ **Agent Discovery** automático via HTTP
- ✅ **Monitoramento em Tempo Real** de status dos agentes
- ✅ **Research System** com tags `[PESQUISA]` integrado
- ✅ **Neutralidade do Supervisor** garantida

---

<div align="center">

**🔥 Fla-Flu Debate - Onde a tecnologia encontra a paixão! ⚽**

*Powered by Google Gemini AI | Built with ❤️ para os torcedores cariocas*

</div>