FROM tensorflow/serving:2.12.0

# Salin model dari serving_model/ 
# Path ini adalah relative ke context (root repo)
COPY ./serving_model/rfahrur6045-pipeline /models/ecommerce_churn

# Environment variables
ENV MODEL_NAME=ecommerce_churn
ENV PORT=8501

# Expose ports (8501 untuk REST, 8500 untuk gRPC)
EXPOSE 8500
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/v1/models/ecommerce_churn/metadata || exit 1

# Jalankan TensorFlow Serving
# - rest_api_port: REST API pada port 8501
# - grpc_port: gRPC pada port 8500
# - enable_batching: Enable request batching untuk better throughput
ENTRYPOINT ["tensorflow_model_server", \
  "--rest_api_port=8501", \
  "--grpc_port=8500", \
  "--model_name=ecommerce_churn", \
  "--model_base_path=/models/ecommerce_churn", \
  "--enable_batching=true"]
