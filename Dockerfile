# Grafana container for balena
FROM grafana/grafana:latest

# Environment variables for Grafana
ENV GF_SECURITY_ADMIN_PASSWORD=admin
ENV GF_USERS_ALLOW_SIGN_UP=false
ENV GF_PLUGINS_PREINSTALL=grafana-clock-panel,grafana-simple-json-datasource
ENV GF_SECURITY_ALLOW_EMBEDDING=true

# Create necessary directories
USER root
RUN mkdir -p /var/lib/grafana/dashboards
RUN mkdir -p /etc/grafana/provisioning/dashboards
RUN mkdir -p /etc/grafana/provisioning/datasources

# Copy configuration files if they exist
COPY grafana.ini /etc/grafana/grafana.ini
COPY provisioning/ /etc/grafana/provisioning/

# Set proper ownership (using numeric IDs to avoid user lookup issues)
RUN chown -R 472:0 /var/lib/grafana
RUN chown -R 472:0 /etc/grafana
RUN chmod -R 755 /etc/grafana

# Switch back to grafana user
USER 472

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

# Start Grafana
CMD ["grafana-server", "--config=/etc/grafana/grafana.ini", "--homepath=/usr/share/grafana"]