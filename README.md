# ASKiT - Automated Search & Knowledge integration Tool
Upload PDF documents and build your own RAG-powered chatbot in no time. 

project/
├── app/
│   └── streamlit_app.py          # Entry point for the Streamlit UI.
├── agent/
│   ├── __init__.py               # Makes the folder a package.
│   ├── rag_agent.py              # Contains the state graph, nodes, and RAG logic.
│   ├── retrieval.py              # (Optional) Specific retrieval logic if you want to isolate it.
│   └── config.py                 # Configuration settings (e.g., provider selection, API key handling).
├── utils/
│   ├── __init__.py
│   └── helpers.py                # Helper functions (e.g., logging, formatting).
├── tests/
│   └── test_agent.py             # Unit tests for your agent logic.
├── .env                        # Environment variables (API keys, provider flags, etc.)
├── requirements.txt            # Dependencies for the project.
└── README.md                   # Project documentation and instructions.