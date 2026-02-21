#!/bin/bash

echo "=== Testing Fallback Route ==="
echo ""

echo "Before killing v1 pod, testing normal operation..."
SERVICE_URL="http://booking-service/ping"

echo "Sending 5 test requests..."
for i in $(seq 1 5); do
  RESPONSE=$(kubectl exec deploy/booking-service-v1 -c istio-proxy -- curl -s $SERVICE_URL)
  echo "Response $i: $RESPONSE"
done

echo ""
echo "Now scale down v1 to 0 replicas to test fallback..."
kubectl scale deployment booking-service-v1 --replicas=0

echo "Waiting for v1 pods to terminate..."
sleep 10

echo ""
echo "Testing requests after v1 is down (should route to v2)..."
for i in $(seq 1 5); do
  RESPONSE=$(kubectl exec deploy/booking-service-v2 -c istio-proxy -- curl -s $SERVICE_URL)
  echo "Response $i: $RESPONSE"
  
  if echo "$RESPONSE" | grep -q "v2"; then
    echo "  ✓ Successfully routed to v2"
  fi
done

echo ""
echo "Restoring v1 deployment..."
kubectl scale deployment booking-service-v1 --replicas=2

echo "=== Fallback Test Complete ==="
