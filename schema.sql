CREATE TABLE form_schemas (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    schema_json TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schema_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    computed_fields TEXT NOT NULL,
    status TEXT NOT NULL,
    client_ip TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (schema_id) REFERENCES form_schemas(id)
);

CREATE TABLE verification_otps (
    transaction_id TEXT PRIMARY KEY,
    otp_code TEXT NOT NULL,
    email TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    verified BOOLEAN DEFAULT FALSE
);