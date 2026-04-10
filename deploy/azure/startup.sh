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
"$PYTHON_BIN" -m pip --version
"$PYTHON_BIN" -m pip show django gunicorn whitenoise dj-database-url || true
"$PYTHON_BIN" manage.py check --deploy || true

"$PYTHON_BIN" manage.py collectstatic --noinput
"$PYTHON_BIN" manage.py migrate --noinput
exec gunicorn croisicwebzine.wsgi:application --bind=0.0.0.0:${PORT:-8000}
