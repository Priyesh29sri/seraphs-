"""
Agent 7: Oracle API
Main agent for external data integration.
"""

import json
from datetime import datetime
from typing import Dict, List
from agents.agent_7_oracle import tools


class OracleAgent:
    """
    Agent 7: Oracle API
    
    Integrates external regulatory data sources (OFAC, FATF, crypto regulations)
    with internal Agent 1 snapshots for comprehensive compliance coverage.
    """
    
    def __init__(self):
        print("[INFO] Agent 7 initialized (Oracle API)")
        print("  External sources: OFAC, FATF, Crypto Intelligence")
    
    def fetch_all_oracle_data(self) -> Dict:
        """
        Fetch all external oracle data sources.
        
        Returns:
            Consolidated oracle data
        """
        print(f"\n{'='*80}")
        print(f"AGENT 7: Oracle API - External Data Fetching")
        print(f"{'='*80}\n")
        
        oracle_data = {
            "agent": "agent-7-oracle",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sources": {}
        }
        
        # 1. Fetch OFAC sanctions
        try:
            ofac_data = tools.fetch_ofac_sanctions()
            validation = tools.validate_external_data(ofac_data, "OFAC")
            
            if validation["valid"]:
                oracle_data["sources"]["ofac"] = ofac_data
                print(f"✓ OFAC data validated (confidence: {validation['confidence']:.2f})\n")
            else:
                print(f"✗ OFAC validation failed: {validation['issues']}\n")
        except Exception as e:
            print(f"[ERROR] OFAC fetch failed: {e}\n")
        
        # 2. Fetch FATF lists
        try:
            fatf_data = tools.fetch_fatf_lists()
            validation = tools.validate_external_data(fatf_data, "FATF")
            
            if validation["valid"]:
                oracle_data["sources"]["fatf"] = fatf_data
                print(f"✓ FATF data validated (confidence: {validation['confidence']:.2f})\n")
            else:
                print(f"✗ FATF validation failed: {validation['issues']}\n")
        except Exception as e:
            print(f"[ERROR] FATF fetch failed: {e}\n")
        
        # 3. Fetch crypto regulations
        try:
            crypto_data = tools.fetch_crypto_regulations()
            validation = tools.validate_external_data(crypto_data, "Crypto")
            
            if validation["valid"]:
                oracle_data["sources"]["crypto"] = crypto_data
                print(f"✓ Crypto data validated (confidence: {validation['confidence']:.2f})\n")
            else:
                print(f"✗ Crypto validation failed: {validation['issues']}\n")
        except Exception as e:
            print(f"[ERROR] Crypto fetch failed: {e}\n")
        
        oracle_data["total_sources"] = len(oracle_data["sources"])
        
        print(f"[SUCCESS] Fetched {oracle_data['total_sources']} external sources")
        
        return oracle_data
    
    def integrate_with_agent1(self, oracle_data: Dict, agent1_snapshots: List[Dict]) -> Dict:
        """
        Integrate oracle data with Agent 1 snapshots.
        
        Args:
            oracle_data: External oracle data
            agent1_snapshots: Internal snapshots from Agent 1
            
        Returns:
            Integrated dataset
        """
        print(f"\n{'='*80}")
        print(f"INTEGRATING ORACLE DATA WITH AGENT 1")
        print(f"{'='*80}\n")
        
        # Merge datasets
        merged = tools.merge_with_snapshots(oracle_data, agent1_snapshots)
        
        # Trigger pipeline update
        trigger_result = tools.trigger_pipeline_update(oracle_data)
        
        merged["pipeline_triggered"] = trigger_result["success"]
        merged["event_id"] = trigger_result.get("event_id")
        
        return merged
