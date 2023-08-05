FROM ml_model_server:core

# Install inference_engine (runtime/backend)
RUN pip install --no-cache-dir \
    torch==1.8.1+cpu \
    torchvision==0.9.1+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html
