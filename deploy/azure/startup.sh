#!/usr/bin/env bash
set -euo pipefail
set -x

cd /home/site/wwwroot

echo "[startup] pwd=$(pwd)"
echo "[startup] PORT=${PORT:-unset}"

if [ -f "/home/site/wwwroot/antenv/bin/activate" ]; then
	echo "[startup] activating /home/site/wwwroot/antenv"
	# shellcheck disable=SC1091
	. /home/site/wwwroot/antenv/bin/activate
elif [ -f "/antenv/bin/activate" ]; then
	echo "[startup] activating /antenv"
	# shellcheck disable=SC1091
	. /antenv/bin/activate
else
	echo "[startup] no antenv virtual environment found"
fi

# Prefer python3 when available, fallback to python.
PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
	PYTHON_BIN="python"
fi

"$PYTHON_BIN" --version

"$PYTHON_BIN" manage.py collectstatic --noinput
"$PYTHON_BIN" manage.py migrate --noinput
# Nombre de workers : WEB_CONCURRENCY si défini, sinon 2×CPU+1 (min 3, max 8)
WORKERS=${WEB_CONCURRENCY:-$("$PYTHON_BIN" -c "import os; print(min(max(2*(os.cpu_count() or 1)+1, 3), 8))")}
echo "[startup] gunicorn workers: ${WORKERS}"

exec gunicorn croisicwebzine.wsgi:application \
    --bind=0.0.0.0:${PORT:-8000} \
    --workers=${WORKERS} \
    --timeout=60 \
    --max-requests=1000 \
    --max-requests-jitter=100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
