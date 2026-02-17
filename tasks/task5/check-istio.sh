#!/bin/bash

echo "=== Checking Istio Installation ==="
echo ""

echo "1. Checking Istio system pods..."
kubectl get pods -n istio-system
echo ""

echo "2. Checking Istio version..."
istioctl version
echo ""

echo "3. Checking namespace injection..."
kubectl get namespace default -o jsonpath='{.metadata.labels.istio-injection}'
echo ""
echo ""

echo "4. Checking booking-service pods (should have 2/2 READY - app + istio-proxy)..."
kubectl get pods -l app=booking-service
echo ""

echo "5. Checking if Envoy sidecars are injected..."
if kubectl get pods -l app=booking-service -o jsonpath='{.items[0].spec.initContainers[?(@.name=="istio-proxy")].name}' | grep -q "istio-proxy"; then
  echo "✓ istio-proxy sidecar is injected (runs as init container in Istio 1.29)"
else
  echo "✗ istio-proxy sidecar not found"
fi
echo ""

echo "=== Istio Check Complete ==="
