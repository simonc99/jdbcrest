## Run a REST jdbc server
# Layout...
app/
├── main.py
├── config.py
├── database.py
├── models.py
├── auth.py
├── certs/
│   ├── server.crt
│   └── server.key
├── jdbc/
│   └── yourdriver.jar
└── requirements.txt

# To run the application...
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8443 \
  --ssl-keyfile certs/server.key \
  --ssl-certfile certs/server.crt

# Test fetch...
curl -k \
-u restuser:restpassword \
"https://server:8443/query/1?filter_value=12345"

# Test insert...
curl -k \
-u restuser:restpassword \
-H "Content-Type: application/json" \
-X POST \
https://server:8443/insert \
-d '{
      "reference_number":"REF12345",
      "entry_date":"2026-06-01",
      "marker":"IMPORT",
      "status":"NEW"
    }'

