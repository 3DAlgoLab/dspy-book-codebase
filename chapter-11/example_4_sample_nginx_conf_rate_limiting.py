http {
    # Per-IP rate limiting: each unique IP gets its own bucket.
    # 10m = 10MB shared memory, enough for ~160,000 IP addresses.
    # 10r/s = 1 request every 100ms. Requests arriving faster queue up or get rejected.
    limit_req_zone $binary_remote_addr zone=per_user_zone:10m rate=10r/s;

    # Global rate limiting: ALL traffic shares one bucket regardless of source.
    # The static key "global" means every request increments the same counter.
    # This protects your backend from total overload even if individual IPs are under their limits.
    limit_req_zone "global" zone=global_zone:10m rate=100r/s;

    server {
        listen 80;
        server_name example.com;

        location / {
            # Limits stack: a request must pass BOTH checks to reach your backend.
            # Order matters—global limit is checked first, then per-IP.
            
            # burst=20 creates a queue for 20 excess requests during traffic spikes.
            # nodelay processes queued requests immediately instead of spacing them out.
            # Without nodelay, users experience artificial latency as nginx throttles delivery.
            limit_req zone=global_zone burst=20 nodelay;

            # Tighter per-IP limit prevents any single user from consuming the global quota.
            # burst=5 is smaller because individual abuse should be caught quickly.
            limit_req zone=per_user_zone burst=5 nodelay;

            proxy_pass http://my_backend;
        }

        # Return structured JSON instead of nginx's default HTML error page.
        # API clients can parse this and implement retry logic with backoff.
        error_page 503 @limit_hit;
        location @limit_hit {
            default_type application/json;
            return 503 '{"error": "Rate limit exceeded", "retry_after": "1s"}';
        }
    }
}
