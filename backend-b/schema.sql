-- =====================================================
-- Survival Vote DB Schema
-- 백엔드 B 담당: votes 테이블
-- =====================================================

-- 백엔드 A가 관리하는 테이블 (참조용, 실제 생성은 백엔드 A에서)
-- =====================================================

CREATE TABLE IF NOT EXISTS programs (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS episodes (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    program_id      BIGINT NOT NULL,
    episode_number  INT NOT NULL,
    title           VARCHAR(100),
    aired_at        DATE,
    FOREIGN KEY (program_id) REFERENCES programs(id)
);

CREATE TABLE IF NOT EXISTS matchups (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    episode_id      BIGINT NOT NULL,
    name            VARCHAR(100) NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episodes(id)
);

CREATE TABLE IF NOT EXISTS polls (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    matchup_id      BIGINT NOT NULL,
    title           VARCHAR(200) NOT NULL,
    poll_type       VARCHAR(20) NOT NULL COMMENT 'VS | PASS_FAIL | MULTI',
    options         JSON NOT NULL COMMENT '["A셰프", "B셰프", "C셰프"]',
    status          VARCHAR(20) DEFAULT 'OPEN' COMMENT 'OPEN | CLOSED',
    panel_result    JSON COMMENT '{"A셰프": 70, "B셰프": 30}',
    result_revealed BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at       TIMESTAMP NULL,
    FOREIGN KEY (matchup_id) REFERENCES matchups(id)
);

-- =====================================================
-- 백엔드 B 담당 테이블
-- =====================================================

CREATE TABLE IF NOT EXISTS votes (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    poll_id         BIGINT NOT NULL,
    voter_id        VARCHAR(64) NOT NULL COMMENT 'SHA256(IP + fingerprint + poll_id)',
    choice          VARCHAR(100) NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 중복투표 방지
    UNIQUE KEY unique_vote (poll_id, voter_id),

    -- 집계 쿼리 최적화
    INDEX idx_poll_choice (poll_id, choice),

    FOREIGN KEY (poll_id) REFERENCES polls(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 샘플 데이터 (테스트용)
-- =====================================================

-- 프로그램
INSERT INTO programs (id, name) VALUES (1, '흑백요리사');

-- 에피소드
INSERT INTO episodes (id, program_id, episode_number, title) VALUES (1, 1, 1, '1회차');

-- 매치업
INSERT INTO matchups (id, episode_id, name) VALUES (1, 1, '두부지옥 대결');

-- 투표
INSERT INTO polls (id, matchup_id, title, poll_type, options, status, panel_result)
VALUES (
    1,
    1,
    'A셰프 vs B셰프',
    'VS',
    '["A셰프", "B셰프"]',
    'OPEN',
    '{"A셰프": 70, "B셰프": 30}'
);
