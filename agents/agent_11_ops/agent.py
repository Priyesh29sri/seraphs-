"""
Agent 11: AgentOps
Operational monitoring and observability.
"""

import json
from datetime import datetime
from typing import Dict, List
import os


class AgentOpsMonitor:
    """
    Agent 11: AgentOps
    
    Monitors all agents, tracks performance, costs, and errors.
    """
    
    def __init__(self):
        self.metrics = {
            "agents": {},
            "llm_costs": [],
            "pipeline_runs": [],
            "errors": []
        }
        print("[INFO] Agent 11 initialized (AgentOps)")
    
    def track_agent_performance(self, agent_id: str, execution_time: float, success: bool):
        """Track agent execution metrics"""
        if agent_id not in self.metrics["agents"]:
            self.metrics["agents"][agent_id] = {
                "total_runs": 0,
                "successes": 0,
                "failures": 0,
                "total_time": 0,
                "avg_time": 0
            }
        
        stats = self.metrics["agents"][agent_id]
        stats["total_runs"] += 1
        stats["total_time"] += execution_time
        stats["avg_time"] = stats["total_time"] / stats["total_runs"]
        
        if success:
            stats["successes"] += 1
        else:
            stats["failures"] += 1
        
        print(f"[OPS] {agent_id}: {execution_time:.2f}s ({'✓' if success else '✗'})")
    
    def monitor_llm_costs(self, model: str, tokens: Dict, cost: float):
        """Monitor LLM usage and costs"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model": model,
            "tokens_input": tokens.get("input", 0),
            "tokens_output": tokens.get("output", 0),
            "cost": cost
        }
        
        self.metrics["llm_costs"].append(entry)
        
        print(f"[OPS] LLM: {model} - ${cost:.4f}")
    
    def generate_alerts(self, alert_type: str, message: str, severity: str = "INFO"):
        """Generate alerts for critical events"""
        alert = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": alert_type,
            "message": message,
            "severity": severity
        }
        
        print(f"[OPS] ALERT [{severity}]: {message}")
        
        # In production: Send to Slack, email, etc.
        return alert
    
    def get_metrics_summary(self) -> Dict:
        """Get comprehensive metrics summary"""
        total_llm_cost = sum(e["cost"] for e in self.metrics["llm_costs"])
        total_runs = sum(a["total_runs"] for a in self.metrics["agents"].values())
        
        return {
            "total_pipeline_runs": total_runs,
            "total_llm_cost": round(total_llm_cost, 2),
            "agents_monitored": len(self.metrics["agents"]),
            "uptime": "24h",
            "health_status": "healthy"
        }
    
    def health_check(self) -> Dict:
        """System health check"""
        health = {
            "status": "healthy",
            "agents": {},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        for agent_id, stats in self.metrics["agents"].items():
            success_rate = stats["successes"] / stats["total_runs"] if stats["total_runs"] > 0 else 1.0
            health["agents"][agent_id] = {
                "status": "healthy" if success_rate > 0.9 else "degraded",
                "success_rate": round(success_rate, 2)
            }
        
        return health


# Global instance
_ops_monitor = None

def get_ops_monitor() -> AgentOpsMonitor:
    """Get singleton ops monitor"""
    global _ops_monitor
    if _ops_monitor is None:
        _ops_monitor = AgentOpsMonitor()
    return _ops_monitor
