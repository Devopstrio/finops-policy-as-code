import logging
import uuid
import time
import pandas as pd
import numpy as np

class FinOpsPolicyEngine:
    def __init__(self):
        self.logger = logging.getLogger("finops-policy-engine")

    def evaluate_cost_limit(self, current_spend: float, threshold: float):
        """
        Evaluates if current spend exceeds institutional thresholds.
        """
        status = "VIOLATION" if current_spend > threshold else "COMPLIANT"
        severity = "CRITICAL" if current_spend > (threshold * 1.2) else "WARNING" if status == "VIOLATION" else "NONE"
        
        return {
            "status": status,
            "severity": severity,
            "drift_pct": round(((current_spend - threshold) / threshold) * 100, 2) if threshold > 0 else 0
        }

    def analyze_resource_idle(self, cpu_avg: float, network_avg: float, threshold: float = 5.0):
        """
        Identifies if a resource is idle based on CPU and network telemetry.
        """
        is_idle = cpu_avg < threshold and network_avg < (threshold * 1024) # threshold in % and network in bytes
        
        return {
            "is_idle": is_idle,
            "remediation_action": "STOP" if is_idle else "NONE",
            "confidence": 0.95 if cpu_avg < 1.0 else 0.75
        }

    def check_tagging_compliance(self, tags: dict, required_keys: list):
        """
        Validates resource tags against institutional metadata standards.
        """
        missing = [key for key in required_keys if key not in tags]
        
        return {
            "is_compliant": len(missing) == 0,
            "missing_tags": missing,
            "remediation_action": "TAG_OR_NUDGE" if len(missing) > 0 else "NONE"
        }

    def calculate_governance_score(self, total_resources: int, non_compliant: int):
        """
        Calculates the institutional governance score (0-100).
        """
        if total_resources == 0:
            return 100.0
            
        score = (1 - (non_compliant / total_resources)) * 100
        return round(score, 1)

if __name__ == "__main__":
    engine = FinOpsPolicyEngine()
    
    # 1. Cost Limit
    print("Cost Check:", engine.evaluate_cost_limit(1200, 1000))
    
    # 2. Idle Detection
    print("Idle Check:", engine.analyze_resource_idle(0.5, 100))
    
    # 3. Tagging Compliance
    current_tags = {"Environment": "Prod", "Owner": "TeamA"}
    required = ["Environment", "Owner", "CostCenter"]
    print("Tagging Check:", engine.check_tagging_compliance(current_tags, required))
    
    # 4. Governance Score
    print("Governance Score:", engine.calculate_governance_score(1000, 120))
