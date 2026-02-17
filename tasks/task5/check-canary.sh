#!/bin/bash

echo "=== Testing Canary Deployment (90% v1, 10% v2) ==="
echo ""

SERVICE_URL="http://$(kubectl get svc booking-service -o jsonpath='{.spec.clusterIP}')"
echo "Service URL: $SERVICE_URL"
echo ""

V1_COUNT=0
V2_COUNT=0
TOTAL_REQUESTS=100

echo "Sending $TOTAL_REQUESTS requests..."

for i in $(seq 1 $TOTAL_REQUESTS); do
  RESPONSE=$(kubectl exec -it deploy/booking-service-v1 -c booking-service -- curl -s $SERVICE_URL)
  
  if echo "$RESPONSE" | grep -q "v1"; then
    V1_COUNT=$((V1_COUNT + 1))
  elif echo "$RESPONSE" | grep -q "v2"; then
    V2_COUNT=$((V2_COUNT + 1))
  fi
  
  if [ $((i % 10)) -eq 0 ]; then
    echo "Progress: $i/$TOTAL_REQUESTS requests sent"
  fi
done

echo ""
echo "=== Results ==="
echo "V1 responses: $V1_COUNT (~$((V1_COUNT * 100 / TOTAL_REQUESTS))%)"
echo "V2 responses: $V2_COUNT (~$((V2_COUNT * 100 / TOTAL_REQUESTS))%)"
echo ""

if [ $V1_COUNT -gt 80 ] && [ $V2_COUNT -gt 5 ]; then
  echo "✓ Canary deployment is working correctly (expected ~90% v1, ~10% v2)"
else
  echo "✗ Canary deployment might not be configured correctly"
fi
