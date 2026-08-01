import os, random, time, logging, sys
from flask import Flask
import requests

ROLE = os.environ.get("ROLE", "frontend")
DOWNSTREAM = os.environ.get("DOWNSTREAM", "")
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s level=%(levelname)s service=' + ROLE + ' %(message)s')
# suppress werkzeug's access log (it prints client IPs) — we emit clean structured logs only
logging.getLogger("werkzeug").setLevel(logging.ERROR)
log = logging.getLogger(ROLE)
app = Flask(__name__)

@app.get("/")
def handle():
    if ROLE == "payment":
        if random.random() < 0.30:            # the deliberate bug — the ONLY failure
            time.sleep(0.15)
            log.error('msg="payment declined" status=503')   # ERROR so it shows red
            return "payment declined\n", 503
        log.info('msg="payment processed" status=200')
        return "paid\n", 200
    # frontend & checkout orchestrate and stay healthy (200); the failure is
    # isolated to payment, so only payment lights up red in logs and traces.
    try:
        requests.get(f"http://{DOWNSTREAM}/", timeout=2)
    except Exception:
        pass
    log.info(f'msg="request handled" downstream={DOWNSTREAM} status=200')
    return f"{ROLE} ok\n", 200

@app.get("/healthz")
def health():
    return "ok\n", 200
