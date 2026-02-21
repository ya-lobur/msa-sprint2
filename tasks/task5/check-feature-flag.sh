#!/bin/bash

echo "=== Testing Feature Flag Routing ==="
echo ""

SERVICE_URL="http://booking-service/ping"
echo "Service URL: $SERVICE_URL"
echo ""

echo "1. Testing without feature flag header (should use canary routing)..."
for i in $(seq 1 5); do
  RESPONSE=$(kubectl exec deploy/booking-service-v1 -c istio-proxy -- curl -s $SERVICE_URL)
  echo "Response $i: $RESPONSE"
done

echo ""
echo "2. Testing with X-Feature-Enabled: true header (should always route to v2)..."
for i in $(seq 1 10); do
  RESPONSE=$(kubectl exec deploy/booking-service-v1 -c istio-proxy -- curl -s -H "X-Feature-Enabled: true" $SERVICE_URL)
  echo "Response $i: $RESPONSE"
  
  if echo "$RESPONSE" | grep -q "v2"; then
    echo "  ✓ Correctly routed to v2 with feature flag"
  else
    echo "  ✗ Failed to route to v2 with feature flag"
  fi
done

echo ""
echo "=== Feature Flag Test Complete ==="
