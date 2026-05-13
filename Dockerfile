FROM rocm/dev-ubuntu-22.04:6.0
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY zkforge/ zkforge/
COPY configs/ configs/
EXPOSE 9090
CMD ["python", "-m", "zkforge.cli"]
