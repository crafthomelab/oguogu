CREATE TABLE challenges (
    hash VARCHAR PRIMARY KEY,
    id INTEGER,
    status VARCHAR NOT NULL,
    nonce INTEGER,
    challenger_address VARCHAR NOT NULL,
    reward_amount NUMERIC(78, 0) NOT NULL,
    title VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    minimum_activity_count INTEGER NOT NULL,
    payment_transaction VARCHAR,
    payment_reward INTEGER NOT NULL,
    complete_date TIMESTAMPTZ
);

CREATE INDEX idx_challenger_address ON challenges (challenger_address);
CREATE INDEX idx_start_date ON challenges (start_date);

CREATE TABLE challenge_activities (
    challenge_hash VARCHAR NOT NULL REFERENCES challenges(hash),
    activity_hash VARCHAR NOT NULL,
    activity_transaction VARCHAR,
    activity_date TIMESTAMPTZ,
    PRIMARY KEY (challenge_hash, activity_hash)
);

CREATE INDEX idx_challenge_hash ON challenge_activities (challenge_hash);