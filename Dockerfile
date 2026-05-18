FROM python:3.12.2

RUN apt-get update && \
    apt-get install -y --no-install-recommends libmediainfo0v5 ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip --root-user-action=ignore && \
    pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY . .

RUN chmod +x update.sh

CMD ["sh", "update.sh"]

