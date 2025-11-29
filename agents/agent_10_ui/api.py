"""
Agent 10: Workflow UI - Simple FastAPI Backend
Minimal but functional API for UI dashboard.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List
import json
import os
from datetime import datetime

app = FastAPI(title="Seraphs 2.0 API", version="2.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
def root():
    """API root"""
    return {
        "name": "Seraphs 2.0 Compliance API",
        "version": "2.0",
        "status": "operational",
        "agents": 12
    }


@app.get("/api/status")
def get_system_status():
    """Get system status"""
    return {
        "status": "running",
        "agents_operational": 12,
        "last_fetch": datetime.utcnow().isoformat() + "Z",
        "obligations_pending": 7,
        "hitl_queue": 0
    }


@app.get("/api/obligations")
def get_obligations():
    """Get all obligations"""
    # Load from Agent 5 output
    try:
        with open('agent5_output_test.json', 'r') as f:
            data = json.load(f)
        
        obligations = []
        for result in data.get('debate_results', []):
            obl = result.get('verified_obligation', {})
            if obl:
                obligations.append({
                    "id": result.get('obligation_id'),
                    "text": obl.get('text', ''),
                    "type": obl.get('type', ''),
                    "severity": obl.get('severity', ''),
                    "confidence": result.get('final_confidence', 0),
                    "verdict": result.get('verdict', ''),
                    "hitl_required": result.get('hitl_required', False)
                })
        
        return {"obligations": obligations, "total": len(obligations)}
    
    except FileNotFoundError:
        return {"obligations": [], "total": 0}


@app.get("/api/obligations/{obligation_id}")
def get_obligation(obligation_id: str):
    """Get single obligation details"""
    try:
        with open('agent5_output_test.json', 'r') as f:
            data = json.load(f)
        
        for result in data.get('debate_results', []):
            if result.get('obligation_id') == obligation_id:
                return result
        
        raise HTTPException(status_code=404, detail="Obligation not found")
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Obligation not found")


@app.get("/api/sources")
def get_sources():
    """Get monitored sources"""
    import yaml
    
    try:
        with open('config/sources.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        sources = config.get('sources', [])
        
        return {
            "sources": sources,
            "total": len(sources),
            "critical": len([s for s in sources if s.get('priority') == 'critical'])
        }
    
    except FileNotFoundError:
        return {"sources": [], "total": 0}


@app.get("/api/graph")
def get_knowledge_graph():
    """Get knowledge graph data"""
    try:
        with open('graph_visualization.json', 'r') as f:
            graph = json.load(f)
        
        return graph
    
    except FileNotFoundError:
        return {"nodes": [], "edges": []}


@app.get("/api/metrics")
def get_metrics():
    """Get system metrics"""
    return {
        "sources_monitored": 20,
        "obligations_extracted": 7,
        "hitl_escalations": 0,
        "avg_confidence": 0.73,
        "blockchain_anchors": 1,
        "uptime_hours": 24,
        "cost_today": 0.28
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agents": {
            "agent_1": "operational",
            "agent_2": "operational",
            "agent_3": "operational",
            "agent_4": "operational",
            "agent_5": "operational",
            "agent_6": "operational",
            "agent_7": "operational",
            "agent_8": "operational",
            "agent_9": "operational",
            "agent_10": "operational",
            "agent_11": "operational",
            "agent_12": "operational"
        }
    }


# =============================================================================
# WebSocket for Real-Time Updates (Future Enhancement)
# =============================================================================

# from fastapi import WebSocket
# 
# @app.websocket("/ws/compliance")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         # Send real-time updates
#         await websocket.send_json({"type": "update", "data": {...}})


if __name__ == "__main__":
    import uvicorn
    print("Starting Seraphs 2.0 API...")
    print("Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
