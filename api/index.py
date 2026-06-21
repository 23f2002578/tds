from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import numpy as np
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.options("/api/latency")
async def options_handler():
    return Response(status_code=200)

TELEMETRY_DATA = json.loads("""
[
  {"region": "apac", "service": "payments", "latency_ms": 171.82, "uptime_pct": 97.43, "timestamp": 20250301},
  {"region": "apac", "service": "checkout", "latency_ms": 185.37, "uptime_pct": 97.29, "timestamp": 20250302},
  {"region": "apac", "service": "payments", "latency_ms": 224.98, "uptime_pct": 98.525, "timestamp": 20250303},
  {"region": "apac", "service": "catalog", "latency_ms": 171.16, "uptime_pct": 98.949, "timestamp": 20250304},
  {"region": "apac", "service": "payments", "latency_ms": 118.22, "uptime_pct": 97.79, "timestamp": 20250305},
  {"region": "apac", "service": "payments", "latency_ms": 124.61, "uptime_pct": 97.28, "timestamp": 20250306},
  {"region": "apac", "service": "checkout", "latency_ms": 214.04, "uptime_pct": 98.352, "timestamp": 20250307},
  {"region": "apac", "service": "support", "latency_ms": 155.36, "uptime_pct": 99.404, "timestamp": 20250308},
  {"region": "apac", "service": "support", "latency_ms": 115.02, "uptime_pct": 98.319, "timestamp": 20250309},
  {"region": "apac", "service": "payments", "latency_ms": 180.35, "uptime_pct": 97.784, "timestamp": 20250310},
  {"region": "apac", "service": "recommendations", "latency_ms": 174.19, "uptime_pct": 97.687, "timestamp": 20250311},
  {"region": "apac", "service": "recommendations", "latency_ms": 109.01, "uptime_pct": 98.829, "timestamp": 20250312},
  {"region": "emea", "service": "support", "latency_ms": 164.38, "uptime_pct": 99.352, "timestamp": 20250301},
  {"region": "emea", "service": "checkout", "latency_ms": 144.93, "uptime_pct": 99.225, "timestamp": 20250302},
  {"region": "emea", "service": "support", "latency_ms": 122.74, "uptime_pct": 98.564, "timestamp": 20250303},
  {"region": "emea", "service": "analytics", "latency_ms": 239.69, "uptime_pct": 98.456, "timestamp": 20250304},
  {"region": "emea", "service": "support", "latency_ms": 109.37, "uptime_pct": 99.024, "timestamp": 20250305},
  {"region": "emea", "service": "catalog", "latency_ms": 176.95, "uptime_pct": 97.608, "timestamp": 20250306},
  {"region": "emea", "service": "checkout", "latency_ms": 114.71, "uptime_pct": 97.11, "timestamp": 20250307},
  {"region": "emea", "service": "recommendations", "latency_ms": 112.97, "uptime_pct": 98.718, "timestamp": 20250308},
  {"region": "emea", "service": "recommendations", "latency_ms": 204.41, "uptime_pct": 97.799, "timestamp": 20250309},
  {"region": "emea", "service": "catalog", "latency_ms": 203.65, "uptime_pct": 98.394, "timestamp": 20250310},
  {"region": "emea", "service": "analytics", "latency_ms": 166.87, "uptime_pct": 99.223, "timestamp": 20250311},
  {"region": "emea", "service": "analytics", "latency_ms": 108.08, "uptime_pct": 97.468, "timestamp": 20250312},
  {"region": "amer", "service": "analytics", "latency_ms": 160.47, "uptime_pct": 97.241, "timestamp": 20250301},
  {"region": "amer", "service": "recommendations", "latency_ms": 201.37, "uptime_pct": 99.102, "timestamp": 20250302},
  {"region": "amer", "service": "payments", "latency_ms": 179.39, "uptime_pct": 97.848, "timestamp": 20250303},
  {"region": "amer", "service": "support", "latency_ms": 168.24, "uptime_pct": 99.212, "timestamp": 20250304},
  {"region": "amer", "service": "recommendations", "latency_ms": 217.44, "uptime_pct": 97.753, "timestamp": 20250305},
  {"region": "amer", "service": "payments", "latency_ms": 138.84, "uptime_pct": 97.399, "timestamp": 20250306},
  {"region": "amer", "service": "payments", "latency_ms": 182.96, "uptime_pct": 98.151, "timestamp": 20250307},
  {"region": "amer", "service": "catalog", "latency_ms": 127.83, "uptime_pct": 99.026, "timestamp": 20250308},
  {"region": "amer", "service": "checkout", "latency_ms": 186.83, "uptime_pct": 98.605, "timestamp": 20250309},
  {"region": "amer", "service": "payments", "latency_ms": 155.84, "uptime_pct": 97.533, "timestamp": 20250310},
  {"region": "amer", "service": "payments", "latency_ms": 183.01, "uptime_pct": 99.005, "timestamp": 20250311},
  {"region": "amer", "service": "recommendations", "latency_ms": 108.99, "uptime_pct": 97.837, "timestamp": 20250312}
]
""")

@app.post("/api/latency")
async def latency_analytics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold_ms = body.get("threshold_ms", 180)

    results = []
    for region in regions:
        records = [r for r in TELEMETRY_DATA if r["region"] == region]
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        results.append({
            "region": region,
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 3),
            "breaches": int(sum(1 for l in latencies if l > threshold_ms))
        })

    return {"regions": results}
