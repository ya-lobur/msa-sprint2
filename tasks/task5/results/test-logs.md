# Test logs

## check-istio
```text
❯ sh check-istio.sh       
=== Checking Istio Installation ===

1. Checking Istio system pods...
NAME                                   READY   STATUS    RESTARTS   AGE
istio-egressgateway-f7fc5b56c-bh8bw    1/1     Running   0          35m
istio-ingressgateway-8d7447659-7pgz7   1/1     Running   0          35m
istiod-7c4fbc86db-ws4lw                1/1     Running   0          35m

2. Checking Istio version...
client version: 1.29.0
control plane version: 1.29.0
data plane version: 1.29.0 (5 proxies)

3. Checking namespace injection...
enabled

4. Checking booking-service pods (should have 2 containers - app + istio-proxy)...
booking-service-v1-56fd5df77-6g26l      booking-service
booking-service-v1-56fd5df77-fgprz      booking-service
booking-service-v2-95c58cd5b-mzcz2      booking-service

5. Checking if Envoy sidecars are injected...


=== Istio Check Complete ===
```

## check-canary

```text
❯ sh check-canary.sh  
=== Testing Canary Deployment (90% v1, 10% v2) ===

Service URL: http://10.106.170.172

Sending 100 requests...
Progress: 10/100 requests sent
Progress: 20/100 requests sent
Progress: 30/100 requests sent
Progress: 40/100 requests sent
Progress: 50/100 requests sent
Progress: 60/100 requests sent
Progress: 70/100 requests sent
Progress: 80/100 requests sent
Progress: 90/100 requests sent
Progress: 100/100 requests sent

=== Results ===
V1 responses: 94 (~94%)
V2 responses: 6 (~6%)

✓ Canary deployment is working correctly (expected ~90% v1, ~10% v2)
```

## check-fallback
```text
❯ sh check-fallback.sh
=== Testing Fallback Route ===

Before killing v1 pod, testing normal operation...
Sending 5 test requests...
Response 1: Response from booking-service v1
Response 2: Response from booking-service v1
Response 3: Response from booking-service v1
Response 4: Response from booking-service v1
Response 5: Response from booking-service v1

Now scale down v1 to 0 replicas to test fallback...
deployment.apps/booking-service-v1 scaled
Waiting for v1 pods to terminate...

Testing requests after v1 is down (should route to v2)...
Response 1: no healthy upstream
Response 2: no healthy upstream
Response 3: Response from booking-service v2 with new features!
  ✓ Successfully routed to v2
Response 4: Response from booking-service v2 with new features!
  ✓ Successfully routed to v2
Response 5: no healthy upstream

Restoring v1 deployment...
deployment.apps/booking-service-v1 scaled
=== Fallback Test Complete ===
```

## check-feature-flag

```text
❯ sh check-feature-flag.sh 
=== Testing Feature Flag Routing ===

Service URL: http://10.106.170.172

1. Testing without feature flag header (should use canary routing)...
Response 1: Response from booking-service v1
Response 2: Response from booking-service v1
Response 3: Response from booking-service v1
Response 4: Response from booking-service v1
Response 5: Response from booking-service v1

2. Testing with X-Feature-Enabled: true header (should always route to v2)...
Response 1: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 2: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 3: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 4: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 5: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 6: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 7: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 8: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 9: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag
Response 10: Response from booking-service v2 with new features!
  ✓ Correctly routed to v2 with feature flag

=== Feature Flag Test Complete ===
```