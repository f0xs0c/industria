import os
import time
import csv
import random
from datetime import datetime, timezone

# Paramètres via env vars
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/data/dataset.csv")
INTERVAL_SEC = float(os.getenv("INTERVAL_SEC", "1"))
SEED = int(os.getenv("SEED", "42"))
BATCH_STARTUP_ROWS = int(os.getenv("BATCH_STARTUP_ROWS", "100"))

random.seed(SEED)

HEADER = ["timestamp","temperature","pressure","flow","yield"]

# Relations simples et réalistes :
# - La pression suit (grossièrement) la température (P ≈ a*T + bruit)
# - Le débit peut varier indépendamment mais corrélé faiblement à T
# - Le rendement (yield) dépend non-linéairement de T, P, flow (avec bruit)

def generate_row():
    # Température autour de 70°C (±10)
    temperature = random.gauss(70, 6)
    # Pression en bar corrélée à T (ex: 1.2 + 0.03*T) + bruit
    pressure = 1.2 + 0.03*temperature + random.gauss(0, 0.2)
    # Débit en L/min (moyenne 50, ±8) avec légère corrélation à T
    flow = random.gauss(50 + 0.05*(temperature-70), 6)

    # Rendement en % (0-100) via fonction non linéaire + bruit
    base = 60 + 0.3*(temperature-70) + 3*(pressure-3) + 0.1*(flow-50)
    nonlinear = -0.02*(temperature-75)**2 - 0.5*(pressure-3.5)**2
    y = base + nonlinear + random.gauss(0, 1.5)
    y = max(0, min(100, y))

    ts = datetime.now(timezone.utc).isoformat()
    return [ts, round(temperature, 3), round(pressure, 3), round(flow, 3), round(y, 3)]

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Créer le fichier & header si absent
if not os.path.exists(OUTPUT_PATH):
    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)

# Batch initial pour démarrer avec des données
with open(OUTPUT_PATH, "a", newline="") as f:
    writer = csv.writer(f)
    for _ in range(BATCH_STARTUP_ROWS):
        writer.writerow(generate_row())

# Boucle temps réel
while True:
    with open(OUTPUT_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(generate_row())
    time.sleep(INTERVAL_SEC)
