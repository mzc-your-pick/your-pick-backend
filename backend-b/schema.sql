-- =====================================================
-- Survival Vote DB Schema (v2)
-- 새 구조: programs, topics, votes, participant_images, comments
-- =====================================================

CREATE TABLE IF NOT EXISTS programs (
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT '프로그램 고유 식별 번호',
    title           VARCHAR(255) NOT NULL COMMENT '프로그램 이름 (예: 흑백요리사)',
    description     TEXT COMMENT '프로그램 상세 설명',
    status          VARCHAR(50) NOT NULL COMMENT '방영 상태 (방영중/방영예정/종영)',
    image_url       VARCHAR(512) COMMENT '프로그램 대표 이미지 URL',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '데이터 등록 일시'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS topics (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '주제 고유 식별 번호',
    program_id      INT NOT NULL COMMENT '프로그램 ID (외래 키)',
    topic_title     VARCHAR(255) NOT NULL COMMENT '대결 제목 (예: 최강록 VS 요리괴물)',
    episode         INT COMMENT '회차 번호',
    match_type      VARCHAR(100) COMMENT '대결 형식 (1대1, 다대다 등)',
    participants    TEXT COMMENT '참여자 명단',
    video_url       VARCHAR(512) COMMENT '관련 영상 URL',
    vote_type       INT NOT NULL COMMENT '투표 방식 (1:합불, 2:1대1, 3:다인원)',
    actual_result   INT COMMENT '실제 방송 결과값',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '주제 생성 일시',
    FOREIGN KEY (program_id) REFERENCES programs(id),
    INDEX idx_program (program_id),
    INDEX idx_episode (program_id, episode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS participant_images (
    id                  INT AUTO_INCREMENT PRIMARY KEY COMMENT '이미지 고유 식별 번호',
    topic_id            BIGINT NOT NULL COMMENT '주제 ID (FK)',
    participant_name    VARCHAR(100) NOT NULL COMMENT '참가자 이름',
    image_url           VARCHAR(512) NOT NULL COMMENT '참가자 이미지 URL',
    FOREIGN KEY (topic_id) REFERENCES topics(id),
    INDEX idx_topic (topic_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS votes (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '투표 기록 고유 식별 번호',
    topic_id        BIGINT NOT NULL COMMENT '주제 ID (FK)',
    vote_choice     INT NOT NULL COMMENT '사용자가 선택한 번호',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '투표 일시',
    FOREIGN KEY (topic_id) REFERENCES topics(id),
    INDEX idx_topic_choice (topic_id, vote_choice)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS comments (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '댓글 고유 식별 번호',
    vote_id             BIGINT NOT NULL COMMENT '투표 ID (FK)',
    content             TEXT NOT NULL COMMENT '댓글 내용',
    comment_user_name   VARCHAR(100) NOT NULL COMMENT '작성자 이름',
    comment_password    VARCHAR(255) NOT NULL COMMENT '댓글 비밀번호 (수정/삭제용)',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '댓글 작성 시간',
    FOREIGN KEY (vote_id) REFERENCES votes(id),
    INDEX idx_vote (vote_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 샘플 데이터 (테스트용)
-- =====================================================

INSERT INTO programs (id, title, description, status) VALUES
(1, '흑백요리사', '넷플릭스 요리 서바이벌', '방영중');

INSERT INTO topics (id, program_id, topic_title, episode, match_type, participants, vote_type, actual_result) VALUES
(1, 1, '최강록 VS 요리괴물', 1, '1대1', '최강록, 요리괴물', 2, 1);

INSERT INTO participant_images (topic_id, participant_name, image_url) VALUES
(1, '최강록', 'https://example.com/chef1.jpg'),
(1, '요리괴물', 'https://example.com/chef2.jpg');
