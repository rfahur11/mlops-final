FROM tensorflow/serving:2.12.0

# Salin model ke dalam container
COPY ./model /models/ecommerce_churn/1

# Environment variables
ENV MODEL_NAME=ecommerce_churn
ENV PORT=8501

# Expose ports
EXPOSE 8500
EXPOSE 8501

# Jalankan TF Serving
ENTRYPOINT ["tensorflow_model_server", \
  "--rest_api_port=8501", \
  "--model_name=ecommerce_churn", \
  "--model_base_path=/models/ecommerce_churn"]
