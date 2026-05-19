FROM prom/prometheus:latest

# Salin konfigurasi Prometheus ke dalam container
COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY alert_rules.yml /etc/prometheus/alert_rules.yml

# Expose port Prometheus
EXPOSE 9090

# Jalankan Prometheus
CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.enable-lifecycle"]
