# 🔐 Security Architecture Documentation

## Security Layers

```mermaid
graph TB
    Client[Client Application]
    
    subgraph "API Gateway Security Layers"
        L1[Layer 1: Rate Limiting]
        L2[Layer 2: Authentication]
        L3[Layer 3: Authorization]
        L4[Layer 4: Input Validation]
        L5[Layer 5: Security Headers]
        L6[Layer 6: Logging & Monitoring]
    end
    
    Backend[Backend Services]
    
    Client -->|Request| L1
    L1 -->|Passed| L2
    L2 -->|Authenticated| L3
    L3 -->|Authorized| L4
    L4 -->|Validated| L5
    L5 -->|Secured| L6
    L6 -->|Forwarded| Backend
    
    L1 -.->|429 Too Many Requests| Client
    L2 -.->|401 Unauthorized| Client
    L3 -.->|403 Forbidden| Client
    L4 -.->|400 Bad Request| Client
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Auth
    participant Redis
    participant Backend
    
    Client->>Gateway: POST /auth/login
    Gateway->>Auth: Validate Credentials
    Auth->>Auth: Verify Password Hash
    
    alt Valid Credentials
        Auth->>Auth: Generate JWT
        Auth->>Redis: Store Refresh Token
        Auth-->>Gateway: Access + Refresh Tokens
        Gateway-->>Client: 200 OK + Tokens
    else Invalid Credentials
        Auth-->>Gateway: Invalid
        Gateway-->>Client: 401 Unauthorized
    end
    
    Note over Client: Store Tokens
    
    Client->>Gateway: GET /api/resource (+ JWT)
    Gateway->>Gateway: Validate JWT
    
    alt Valid JWT
        Gateway->>Backend: Forward Request
        Backend-->>Gateway: Response
        Gateway-->>Client: 200 OK + Data
    else Invalid/Expired JWT
        Gateway-->>Client: 401 Unauthorized
        Note over Client: Use Refresh Token
        Client->>Gateway: POST /auth/refresh
        Gateway->>Redis: Validate Refresh Token
        Redis-->>Gateway: Valid
        Gateway->>Auth: Generate New Access Token
        Auth-->>Gateway: New JWT
        Gateway-->>Client: 200 OK + New Token
    end
```

## Rate Limiting Strategy

```mermaid
stateDiagram-v2
    [*] --> CheckBucket: Request Arrives
    CheckBucket --> HasTokens: Check Token Bucket
    
    HasTokens --> AllowRequest: Tokens Available
    HasTokens --> RejectRequest: No Tokens
    
    AllowRequest --> ConsumeToken: Consume 1 Token
    ConsumeToken --> ProcessRequest: Forward Request
    ProcessRequest --> [*]: Return Response
    
    RejectRequest --> ReturnError: 429 Too Many Requests
    ReturnError --> [*]: Return Error
    
    note right of CheckBucket
        Token Bucket Algorithm
        - Capacity: 100 tokens
        - Refill: 10 tokens/sec
        - Per IP/User
    end note
```

## Circuit Breaker Pattern

```mermaid
stateDiagram-v2
    [*] --> Closed: Initial State
    
    Closed --> Open: Failure Threshold Reached
    Open --> HalfOpen: Timeout Elapsed
    HalfOpen --> Closed: Success
    HalfOpen --> Open: Failure
    
    Closed --> Closed: Success
    Closed --> Closed: Failure (< threshold)
    
    note right of Closed
        Normal Operation
        - Allow all requests
        - Track failures
    end note
    
    note right of Open
        Failure State
        - Reject all requests
        - Return 503 immediately
        - Wait for timeout
    end note
    
    note right of HalfOpen
        Testing State
        - Allow limited requests
        - Test if service recovered
    end note
```

## Security Components

### 1. JWT Authentication

```python
# JWT Structure
{
    "header": {
        "alg": "HS256",
        "typ": "JWT"
    },
    "payload": {
        "user_id": 123,
        "username": "john_doe",
        "role": "trader",
        "exp": 1699999999,
        "iat": 1699996399
    },
    "signature": "..."
}
```

**Token Lifecycle:**
- **Access Token**: 1 hour expiration
- **Refresh Token**: 7 days expiration
- **Rotation**: New refresh token on each refresh

### 2. Password Security

```python
# Bcrypt with salt
password_hash = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt(rounds=12)
)

# Verification
is_valid = bcrypt.checkpw(
    password.encode('utf-8'),
    stored_hash
)
```

**Password Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character

### 3. Rate Limiting

```python
# Token Bucket Algorithm
class TokenBucket:
    capacity = 100      # Maximum tokens
    refill_rate = 10    # Tokens per second
    tokens = 100        # Current tokens
    last_refill = now()
    
    def consume(self, tokens=1):
        self.refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
```

**Rate Limits:**
- **Anonymous**: 10 req/min
- **Authenticated**: 100 req/min
- **Premium**: 1000 req/min

### 4. Security Headers

```python
headers = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}
```

## OWASP Top 10 Mitigation

| Vulnerability | Mitigation | Implementation |
|---------------|------------|----------------|
| **A01: Broken Access Control** | RBAC + JWT | Role-based endpoints |
| **A02: Cryptographic Failures** | TLS 1.3 + Bcrypt | HTTPS only, password hashing |
| **A03: Injection** | Input validation | Pydantic models |
| **A04: Insecure Design** | Security by design | Multiple security layers |
| **A05: Security Misconfiguration** | Security headers | OWASP headers |
| **A06: Vulnerable Components** | Dependency scanning | Regular updates |
| **A07: Auth Failures** | JWT + MFA ready | Secure token management |
| **A08: Data Integrity Failures** | Request signing | HMAC verification |
| **A09: Logging Failures** | Comprehensive logging | All requests logged |
| **A10: SSRF** | URL validation | Whitelist approach |

## Request Flow with Security

```mermaid
flowchart TD
    A[Client Request] --> B{Rate Limit Check}
    B -->|Exceeded| C[429 Too Many Requests]
    B -->|OK| D{JWT Validation}
    D -->|Invalid| E[401 Unauthorized]
    D -->|Valid| F{Role Check}
    F -->|Forbidden| G[403 Forbidden]
    F -->|Authorized| H{Input Validation}
    H -->|Invalid| I[400 Bad Request]
    H -->|Valid| J{Circuit Breaker}
    J -->|Open| K[503 Service Unavailable]
    J -->|Closed| L[Forward to Backend]
    L --> M[Add Security Headers]
    M --> N[Log Request]
    N --> O[Return Response]
    
    style A fill:#e3f2fd
    style O fill:#e8f5e9
    style C fill:#ffebee
    style E fill:#ffebee
    style G fill:#ffebee
    style I fill:#ffebee
    style K fill:#ffebee
```

## Role-Based Access Control (RBAC)

```mermaid
graph TB
    subgraph "Roles"
        Admin[Admin]
        Trader[Trader]
        Viewer[Viewer]
    end
    
    subgraph "Permissions"
        P1[Read Users]
        P2[Write Users]
        P3[Read Orders]
        P4[Write Orders]
        P5[Read Positions]
        P6[Write Positions]
    end
    
    Admin --> P1
    Admin --> P2
    Admin --> P3
    Admin --> P4
    Admin --> P5
    Admin --> P6
    
    Trader --> P1
    Trader --> P3
    Trader --> P4
    Trader --> P5
    
    Viewer --> P1
    Viewer --> P3
    Viewer --> P5
```

## Endpoint Security Matrix

| Endpoint | Method | Auth Required | Rate Limit | Roles Allowed |
|----------|--------|---------------|------------|---------------|
| `/auth/register` | POST | No | 5/min | - |
| `/auth/login` | POST | No | 10/min | - |
| `/auth/refresh` | POST | Yes (Refresh) | 20/min | All |
| `/users/me` | GET | Yes | 100/min | All |
| `/users/{id}` | GET | Yes | 100/min | Admin |
| `/orders` | GET | Yes | 100/min | Trader, Admin |
| `/orders` | POST | Yes | 50/min | Trader, Admin |
| `/admin/users` | GET | Yes | 100/min | Admin |

## Monitoring & Alerts

### Security Metrics

```python
# Metrics to track
security_metrics = {
    "failed_login_attempts": Counter,
    "rate_limit_hits": Counter,
    "jwt_validation_failures": Counter,
    "circuit_breaker_opens": Counter,
    "suspicious_requests": Counter
}
```

### Alert Rules

```yaml
- alert: HighFailedLoginRate
  expr: rate(failed_login_attempts[5m]) > 10
  annotations:
    summary: "Possible brute force attack"
    
- alert: ExcessiveRateLimiting
  expr: rate(rate_limit_hits[5m]) > 100
  annotations:
    summary: "Possible DDoS attack"
    
- alert: CircuitBreakerOpen
  expr: circuit_breaker_state == 1
  for: 5m
  annotations:
    summary: "Backend service degraded"
```

## Security Best Practices

### 1. Token Management
```python
# ✅ Good: Store in httpOnly cookie
response.set_cookie(
    "access_token",
    token,
    httponly=True,
    secure=True,
    samesite="strict"
)

# ❌ Bad: Store in localStorage
localStorage.setItem("token", token)
```

### 2. Password Validation
```python
# ✅ Good: Strong password policy
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*]", password):
        return False
    return True
```

### 3. Input Sanitization
```python
# ✅ Good: Use Pydantic models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
```

## Incident Response

```mermaid
flowchart LR
    A[Security Event] --> B[Detection]
    B --> C[Analysis]
    C --> D[Containment]
    D --> E[Eradication]
    E --> F[Recovery]
    F --> G[Lessons Learned]
    
    style A fill:#ffebee
    style G fill:#e8f5e9
```

## Compliance

### GDPR
- Data encryption at rest and in transit
- Right to be forgotten (user deletion)
- Data portability
- Consent management

### PCI DSS (if handling payments)
- No storage of CVV
- Tokenization of card data
- Regular security audits
- Network segmentation

## Security Checklist

- [x] HTTPS only (TLS 1.3)
- [x] JWT authentication
- [x] Password hashing (bcrypt)
- [x] Rate limiting
- [x] Input validation
- [x] Security headers
- [x] CORS configuration
- [x] Circuit breaker
- [x] Request logging
- [x] Error handling (no sensitive data)
- [x] Dependency scanning
- [x] Regular updates
