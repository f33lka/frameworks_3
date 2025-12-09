import os
import time
import random
from datetime import datetime, timezone

import psycopg2


def build_dsn() -> str:
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        return dsn
    host = os.getenv("PGHOST", "db")
    port = os.getenv("PGPORT", "5432")
    user = os.getenv("PGUSER", "monouser")
    password = os.getenv("PGPASSWORD", "monopass")
    dbname = os.getenv("PGDATABASE", "monolith")
    return f"postgres://{user}:{password}@{host}:{port}/{dbname}"


def log(msg: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    print(f"[telemetry-cli] {now} {msg}", flush=True)


def main() -> None:
    period = int(os.getenv("GEN_PERIOD_SEC", "300"))
    dsn = build_dsn()
    log(f"Starting telemetry CLI with period={period}s, dsn='{dsn}'")

    while True:
        try:
            conn = psycopg2.connect(dsn)
            conn.autocommit = True
            cur = conn.cursor()
            rows = []
            for _ in range(5):
                recorded_at = datetime.now(timezone.utc)
                voltage = round(random.uniform(12.0, 15.0), 2)
                temp = round(random.uniform(-20.0, 60.0), 2)
                source_file = "telemetry_cli"
                rows.append((recorded_at, voltage, temp, source_file))

            cur.executemany(
                "INSERT INTO telemetry_legacy (recorded_at, voltage, temp, source_file) "
                "VALUES (%s, %s, %s, %s)",
                rows,
            )
            log(f"Inserted {len(rows)} rows into telemetry_legacy")
            cur.close()
            conn.close()
        except Exception as e:
            log(f"ERROR: {e!r}")
        time.sleep(period)


if __name__ == "__main__":
    main()
