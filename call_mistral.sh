#!/usr/bin/env bash
curl -X POST http://localhost:11435/api/generate \
     -H "Content-Type: application/json" \
     -d '{
       "model":"mistral",
       "prompt":"Explique-moi le fonctionnement de FAISS."
     }' | jq .
