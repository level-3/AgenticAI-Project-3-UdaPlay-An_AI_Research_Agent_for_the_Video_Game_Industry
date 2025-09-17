# UdaPlay - AI Research Agent for the Video Game Industry

An intelligent AI research assistant specialized in video game industry knowledge, built with advanced RAG (Retrieval-Augmented Generation) capabilities and web search integration.

## 🎮 Overview

UdaPlay is a sophisticated AI agent designed to answer questions about video games, platforms, and industry trends. The agent combines local knowledge from a vector database with real-time web search capabilities to provide accurate and comprehensive responses.

### Key Features

- **Hybrid Knowledge System**: Combines internal vector database knowledge with web search
- **Intelligent Retrieval Evaluation**: Automatically assesses whether retrieved information is sufficient
- **Conversation Memory**: Maintains context across multiple interactions
- **Structured Outputs**: Returns well-formatted, reliable responses
- **Fallback Mechanisms**: Searches the web when local knowledge is insufficient

## 🏗️ Architecture

The agent uses a state machine architecture with the following components:

1. **Message Preparation**: Formats user queries and conversation history
2. **LLM Processing**: Processes queries using GPT models with tool integration
3. **Tool Execution**: Executes retrieval, evaluation, and search tools as needed
4. **Memory Management**: Maintains conversation state and session history

### Tools

#### 1. Retrieve Game Tool
- **Purpose**: Semantic search through the video game vector database
- **Input**: Natural language query about games
- **Output**: Relevant game information including name, platform, release year, genre, and description

#### 2. Evaluate Retrieval Tool
- **Purpose**: Assesses whether retrieved documents are sufficient to answer the user's question
- **Input**: Original question and retrieved documents
- **Output**: Boolean usefulness assessment with detailed explanation

#### 3. Web Search Tool
- **Purpose**: Searches the web when local knowledge is insufficient
- **Input**: Search query
- **Output**: Web search results with answers and source links

## 🛠️ Technology Stack

- **Python 3.10+** with modern syntax features
- **OpenAI GPT-4** for language understanding and generation
- **ChromaDB** for vector storage and semantic search
- **Tavily API** for web search capabilities
- **Pydantic V2** for data validation and parsing
- **Custom State Machine** for agent workflow management

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Tavily API key
- ChromaDB database with video game data

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd udaplay-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with the following:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   CHROMA_OPENAI_API_KEY=your_chroma_openai_api_key
   ```

4. **Prepare the vector database**
   Ensure you have a ChromaDB collection named "udaplay" with video game data

## 💻 Usage

### Basic Example

```python
from lib.agents import Agent
from lib.llm import LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the agent
agent = MemoryAgent(
    model_name="gpt-4o-mini",
    instructions="""
    You are UdaPlay, an AI research assistant specialized in the video game industry.
    Your role is to help users find accurate and relevant information about video games, 
    platforms, and industry trends.
    """,
    tools=[retrieve_game, evaluate_retrieval, web_search],
    temperature=0.3,
)

# Ask a question
response = agent.invoke("When was Super Mario 64 released?")
print(response.get_final_state()["messages"][-1].content)
```

### Advanced Usage with Session Management

```python
# Use sessions to maintain conversation context
session_id = "gaming_research_session"

questions = [
    "When was Pokémon Gold and Silver released?",
    "Which was the first 3D Mario platformer?",
    "Was Mortal Kombat X released for PlayStation 5?"
]

for question in questions:
    run = agent.invoke(question, session_id)
    final_message = run.get_final_state()["messages"][-1]
    print(f"Q: {question}")
    print(f"A: {final_message.content}\n")

# Retrieve conversation history
conversation_history = agent.get_session_runs(session_id)
```

## 📊 Example Interactions

### Question 1: Release Date Query
**Input**: "When was Pokémon Gold and Silver released?"
**Output**: "Pokémon Gold and Silver was released in 1999."

### Question 2: Historical Gaming Question
**Input**: "Which one was the first 3D platformer Mario game?"
**Output**: "The first 3D platformer Mario game is **Super Mario 64**, which was released in 1996. It is considered a groundbreaking title that set new standards for the genre."

### Question 3: Platform Availability
**Input**: "Was Mortal Kombat X released for PlayStation 5?"
**Output**: "Mortal Kombat X was released for PlayStation 4 in 2015, but it is not natively available on PlayStation 5. However, players can still play it on PS5 with compatibility updates."

## 🔧 Configuration

### Agent Settings

```python
agent = MemoryAgent(
    model_name="gpt-4o-mini",        # LLM model to use
    instructions="<system_prompt>",   # Agent instructions
    tools=[...],                     # Available tools
    temperature=0.3,                 # Response creativity (0.0-1.0)
)
```

### Tool Configuration

Each tool can be configured independently:

- **retrieve_game**: Configure ChromaDB collection and search parameters
- **evaluate_retrieval**: Adjust evaluation criteria and thresholds
- **web_search**: Set search depth and result limits

## 🧪 Testing

The project includes comprehensive testing capabilities:

```python
# Test individual tools
evaluation_question = "Best selling game of all time"
games_list = retrieve_game(evaluation_question)
evaluation = evaluate_retrieval(evaluation_question, games_list)

# Test complete agent workflow
test_questions = [
    "What is the highest-rated game of 2023?",
    "Which console has the most exclusive titles?",
    "When was the Nintendo Switch released?"
]

for question in test_questions:
    response = agent.invoke(question)
    # Validate response quality
```

## 📁 Project Structure

```
udaplay-agent/
├── lib/
│   ├── agents.py          # Agent implementations
│   ├── llm.py            # LLM wrapper classes
│   ├── messages.py       # Message type definitions
│   ├── tooling.py        # Tool framework
│   ├── parsers.py        # Response parsers
│   ├── state_machine.py  # State machine implementation
│   └── memory.py         # Memory management
├── chromadb/             # Vector database storage
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── Udaplay_02_starter_project.ipynb  # Main notebook
└── README.md            # This file
```

## 🔍 How It Works

1. **Query Processing**: User submits a question about video games
2. **Retrieval**: Agent searches the vector database for relevant information
3. **Evaluation**: Agent assesses if retrieved information is sufficient
4. **Web Search**: If needed, agent searches the web for additional information
5. **Response Generation**: Agent synthesizes information into a coherent answer
6. **Memory Storage**: Conversation context is saved for future interactions

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Submit a pull request with a clear description

## 📄 License

This project is part of the Udacity Agentic AI course materials.

## 🆘 Support

For questions or issues:
1. Check the existing documentation
2. Review the Jupyter notebook examples
3. Open an issue on GitHub

## 🔮 Future Enhancements

- [ ] Advanced filtering and search capabilities
- [ ] Integration with additional gaming databases
- [ ] Real-time gaming news integration
- [ ] Enhanced conversation context management
- [ ] Multi-language support for international gaming markets

---

**Note**: This project is designed for educational purposes as part of the Udacity Agentic AI program. It demonstrates practical implementation of RAG systems, tool integration, and conversational AI agents.
