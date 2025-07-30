# 🔥 Fla-Flu Debate: Sistema Multi-Agente A2A

Sistema inteligente de debate entre torcedores usando **4 agentes independentes** que se comunicam via **protocolo A2A** (Agent-to-Agent) baseado no **Google ADK**.

## 🎯 **Visão Geral**

Este projeto implementa um sistema de debate automatizado entre Flamengo e Fluminense, onde 4 agentes especializados interagem de forma autônoma para criar debates dinâmicos e informativos.

### 🤖 **Os 4 Agentes**

1. **⚖️ Supervisor**: Coordena o debate, divide o tempo (50% para cada time) e analisa o vencedor baseado em critérios de retórica, psicologia e linguística
2. **🔴 Torcedor Flamengo**: Defende o Flamengo com paixão, dados e argumentos demolidores
3. **🟢 Torcedor Fluminense**: Argumenta com elegância sobre a tradição e superioridade tricolor
4. **📊 Pesquisador**: Busca dados objetivos na internet para embasar os argumentos dos torcedores

## 🛠️ **Tecnologias**

- **Google ADK**: Padrões oficiais do Agent Development Kit
- **Protocolo A2A v1.0**: Comunicação Agent-to-Agent padronizada
- **Google Gemini AI**: LLM para processamento de linguagem natural
- **Streamlit**: Interface web interativa moderna
- **Python 3.12+**: Backend do sistema
- **UV**: Gerenciamento de dependências

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
# Python 3.12+
# UV package manager
# Google API Key (Gemini)
```

### 🔧 **Instalação**
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/FlaFludeAgentes.git
cd FlaFludeAgentes

# 2. Configure a API Key no arquivo .env
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env

# 3. Instale dependências com UV
uv sync

# 4. Execute o sistema
uv run streamlit run app.py
```

### 🌐 **Acesso**
Abra http://localhost:8501 no navegador e:

1. **Clique em "Inicializar Sistema"**
2. **Configure duração do debate** (2-10 minutos)
3. **Clique em "Iniciar Debate"**
4. **Acompanhe o debate em tempo real**
5. **Veja a análise final do supervisor**

## 🔗 **Protocolo A2A**

O sistema implementa comunicação Agent-to-Agent seguindo padrões:

```python
# Exemplo de mensagem A2A
{
    "from": "flamengo",
    "to": "researcher", 
    "message": "PESQUISADOR: busque dados sobre títulos recentes",
    "context": {"debate_topic": "superioridade", "timestamp": 1640995200},
    "protocol": "A2A-v1.0"
}
```

### 📊 **Métricas A2A**
- Mensagens trocadas entre agentes
- Latência de resposta
- Taxa de sucesso das comunicações
- Status de cada agente em tempo real

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
├── agents.py              # 4 agentes independentes + A2A
├── app.py                 # Interface Streamlit avançada
├── test_system.py         # Testes dos agentes
├── .env                   # Configuração da API
├── .env.example           # Template de configuração
├── pyproject.toml         # Dependências UV
├── README.md              # Documentação
├── debate_system/         # Sistema ADK-compatible
│   ├── __init__.py
│   └── agent.py
├── tests/                 # Testes unitários
│   └── test_agents.py
├── eval/                  # Sistema de avaliação
│   └── debate_evaluation.py
└── deployment/            # Deploy Vertex AI
    └── vertex_ai_deploy.py
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

## 🔬 **Testes**

```bash
# Teste rápido dos agentes
uv run python test_system.py

# Testes unitários completos
uv run pytest tests/ -v

# Teste da avaliação
uv run python eval/debate_evaluation.py
```

## 🚀 **Deploy**

### 🌐 **Vertex AI**
```bash
# Configure credenciais
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# Deploy para Vertex AI Agent Engine
uv run python deployment/vertex_ai_deploy.py
```

### 🐳 **Docker**
```bash
# Build da imagem
docker build -t flaflu-debate .

# Execução
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key flaflu-debate
```

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
# Flamengo solicita pesquisa
debate_system.send_message(
    from_agent="flamengo",
    to_agent="researcher", 
    message="PESQUISADOR: estatísticas de público no Maracanã",
    context={"urgency": "high"}
)
```

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Add nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📜 **Licença**

Este projeto está sob a licença MIT. Veja `LICENSE` para detalhes.

## 🏆 **Conquistas**

- ✅ **4 Agentes Independentes** funcionais
- ✅ **Protocolo A2A** implementado  
- ✅ **Google ADK** compatível
- ✅ **Interface Moderna** com Streamlit
- ✅ **Análise Especializada** em tempo real
- ✅ **Sistema de Pesquisa** integrado
- ✅ **Deploy Ready** para produção

---

<div align="center">

**🔥 Fla-Flu Debate - Onde a tecnologia encontra a paixão! ⚽**

*Powered by Google Gemini AI | Built with ❤️ para os torcedores cariocas*

</div>