import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("finops-policy-as-code-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="FinOps Policy as Code API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/policies")
def get_policies():
    return [
        {"id": "POL-001", "name": "Stop Idle Dev VMs", "engine": "OPA", "status": "Enforced"},
        {"id": "POL-002", "name": "Require CostCenter Tag", "engine": "Azure Policy", "status": "Enforced"},
        {"id": "POL-003", "name": "Block Unapproved Instance Types", "engine": "AWS SCP", "status": "Audit"}
    ]

@app.post("/policies/evaluate")
def evaluate_policy(resource_id: str, policy_id: str):
    logger.info(f"Evaluating policy {policy_id} for resource {resource_id}")
    return {"status": "COMPLIANT", "score": 1.0, "resource_id": resource_id}

@app.post("/remediation/run")
def run_remediation(resource_id: str, action: str):
    logger.info(f"Running remediation action {action} on {resource_id}")
    return {"status": "SUCCESS", "operation_id": f"rem_{int(time.time())}"}

@app.get("/billing/summary")
def get_billing_summary():
    return {
        "monthly_spend": 850000.0,
        "governed_spend": 780000.0,
        "savings_realized": 45000.0,
        "active_anomalies": 1
    }

@app.get("/savings/summary")
def get_savings_summary():
    return {
        "total_savings": 125000.0,
        "orphan_cleanup": 32000.0,
        "idle_shutdown": 54000.0,
        "rightsizing": 39000.0
    }

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "overall_compliance": 0.88,
        "preventive_score": 0.92,
        "detective_score": 0.84,
        "remediation_efficiency": 0.95
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_policies": 156,
        "active_scans": 4,
        "remediations_today": 12,
        "maestro_status": "READY"
    }
