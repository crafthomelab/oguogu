CREATE TABLE challenges (
    hash VARCHAR PRIMARY KEY,
    id INTEGER,
    status VARCHAR NOT NULL,
    challenger_address VARCHAR NOT NULL,
    reward_amount NUMERIC(78, 0) NOT NULL,
    title VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    minimum_proof_count INTEGER NOT NULL,
    receipent_address VARCHAR NOT NULL,
    payment_transaction VARCHAR,
    payment_reward INTEGER NOT NULL,
    complete_date TIMESTAMPTZ
);

CREATE INDEX idx_challenger_address ON challenges (challenger_address);
CREATE INDEX idx_start_date ON challenges (start_date);

CREATE TABLE challenge_proofs (
    proof_hash VARCHAR PRIMARY KEY,
    challenge_hash VARCHAR NOT NULL REFERENCES challenges(hash),
    content JSON NOT NULL,
    proof_date TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_challenge_hash ON challenge_proofs (challenge_hash);