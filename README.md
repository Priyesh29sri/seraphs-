# Seraphs - Multi-Agent Compliance Intelligence System 

**Revolutionary AI-powered regulatory compliance monitoring system with 12 cooperating agents**

Seraphs 2.0 is a distributed, multi-agent system that automatically monitors global regulatory changes, verifies authenticity, detects obligations, and generates compliance action plans with 95%+ accuracy.


**Built for IBW Hackathon** | **Powered by LangGraph, Anthropic Claude, Cardano & Midnight**



----
How to Set Up and Run Seraphs

1. Clone the repository and enter the project folder
git clone <your-repo-url> seraphs_3.0
cd seraphs_3.0

2. Create and activate a Python virtual environment
python -m venv venv
On Windows: venv\Scripts\activate
On Mac/Linux: source venv/bin/activate

3. Install all required Python dependencies
pip install -r requirements.txt

4. Start Redis locally so the agents can communicate
Run redis-server (or start Redis from your installed Redis application).

5. Run the end-to-end demo pipeline
python run_pipeline_demo.py

This will execute the full Seraphs 3.0 multi-agent pipeline locally and print each stage (ingestion, authenticity checks, change detection, obligation extraction, verification, and simulated blockchain anchoring) in the terminal.
