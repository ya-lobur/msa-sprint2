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

echo "4. Checking booking-service pods (should have 2 containers - app + istio-proxy)..."
kubectl get pods -l app=booking-service -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'
echo ""

echo "5. Checking if Envoy sidecars are injected..."
kubectl get pods -l app=booking-service -o jsonpath='{.items[0].spec.containers[?(@.name=="istio-proxy")].name}'
echo ""
echo ""

echo "=== Istio Check Complete ==="
