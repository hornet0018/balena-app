FROM balenalib/jetson-nano-ubuntu:bionic-run-20221215

# Don't prompt with any configuration questions
ENV DEBIAN_FRONTEND noninteractive

# Install basic packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

ENV UDEV=1

WORKDIR /app

# Upgrade pip and setuptools first
RUN pip3 install --upgrade pip setuptools wheel

# Copy application files
COPY requirements.txt .
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Default: set FAN_PERCENT to 50 (can be overridden at runtime)
ENV FAN_PERCENT=50

# Add a robust fan control script
RUN echo '#!/bin/bash' > /usr/local/bin/set-fan.sh && \
    echo 'set -euo pipefail' >> /usr/local/bin/set-fan.sh && \
    echo '' >> /usr/local/bin/set-fan.sh && \
    echo 'PERCENT="${FAN_PERCENT:-50}"' >> /usr/local/bin/set-fan.sh && \
    echo 'echo "[set-fan] setting fan to ${PERCENT}%"' >> /usr/local/bin/set-fan.sh && \
    echo '' >> /usr/local/bin/set-fan.sh && \
    echo 'candidates=(' >> /usr/local/bin/set-fan.sh && \
    echo '  /sys/devices/pwm-fan/target_pwm' >> /usr/local/bin/set-fan.sh && \
    echo '  /sys/devices/pwm-fan/pwm1' >> /usr/local/bin/set-fan.sh && \
    echo '  /sys/devices/virtual/pwm-fan/target_pwm' >> /usr/local/bin/set-fan.sh && \
    echo '  /sys/devices/virtual/pwm-fan/pwm1' >> /usr/local/bin/set-fan.sh && \
    echo ')' >> /usr/local/bin/set-fan.sh && \
    echo '' >> /usr/local/bin/set-fan.sh && \
    echo 'for p in /sys/class/hwmon/hwmon*/pwm*; do' >> /usr/local/bin/set-fan.sh && \
    echo '  candidates+=("$p")' >> /usr/local/bin/set-fan.sh && \
    echo 'done' >> /usr/local/bin/set-fan.sh && \
    echo '' >> /usr/local/bin/set-fan.sh && \
    echo 'found=0' >> /usr/local/bin/set-fan.sh && \
    echo 'for fileglob in "${candidates[@]}"; do' >> /usr/local/bin/set-fan.sh && \
    echo '  for file in $fileglob; do' >> /usr/local/bin/set-fan.sh && \
    echo '    if [ -e "$file" ]; then' >> /usr/local/bin/set-fan.sh && \
    echo '      dir=$(dirname "$file")' >> /usr/local/bin/set-fan.sh && \
    echo '      max=255' >> /usr/local/bin/set-fan.sh && \
    echo '      if [ -f "$dir/pwm1_max" ]; then' >> /usr/local/bin/set-fan.sh && \
    echo '        max=$(cat "$dir/pwm1_max")' >> /usr/local/bin/set-fan.sh && \
    echo '      elif [ -f "$dir/max" ]; then' >> /usr/local/bin/set-fan.sh && \
    echo '        max=$(cat "$dir/max")' >> /usr/local/bin/set-fan.sh && \
    echo '      elif [ -f "$dir/pwm_max" ]; then' >> /usr/local/bin/set-fan.sh && \
    echo '        max=$(cat "$dir/pwm_max")' >> /usr/local/bin/set-fan.sh && \
    echo '      fi' >> /usr/local/bin/set-fan.sh && \
    echo '      val=$(( ( PERCENT * max + 50 ) / 100 ))' >> /usr/local/bin/set-fan.sh && \
    echo '      if echo "$val" > "$file" 2>/dev/null; then' >> /usr/local/bin/set-fan.sh && \
    echo '        echo "[set-fan] wrote $val to $file (max=$max) for ${PERCENT}%"' >> /usr/local/bin/set-fan.sh && \
    echo '        found=1' >> /usr/local/bin/set-fan.sh && \
    echo '        break 2' >> /usr/local/bin/set-fan.sh && \
    echo '      else' >> /usr/local/bin/set-fan.sh && \
    echo '        echo "[set-fan] failed to write $val to $file, trying next..." >&2' >> /usr/local/bin/set-fan.sh && \
    echo '      fi' >> /usr/local/bin/set-fan.sh && \
    echo '    fi' >> /usr/local/bin/set-fan.sh && \
    echo '  done' >> /usr/local/bin/set-fan.sh && \
    echo 'done' >> /usr/local/bin/set-fan.sh && \
    echo '' >> /usr/local/bin/set-fan.sh && \
    echo 'if [ "$found" -eq 0 ]; then' >> /usr/local/bin/set-fan.sh && \
    echo '  echo "[set-fan] WARNING: no fan control sysfs file found." >&2' >> /usr/local/bin/set-fan.sh && \
    echo 'fi' >> /usr/local/bin/set-fan.sh && \
    echo '' >> /usr/local/bin/set-fan.sh && \
    echo 'exec "$@"' >> /usr/local/bin/set-fan.sh && \
    chmod +x /usr/local/bin/set-fan.sh

# Run the fan script at container start and then run the requested CMD.
ENTRYPOINT ["/usr/local/bin/set-fan.sh"]
CMD ["python3", "-u", "app.py"]
