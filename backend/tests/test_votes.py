import pytest


class TestVoteAPI:
    """투표 API 테스트"""

    def test_create_vote_success(self, client, sample_poll):
        """정상 투표"""
        response = client.post(
            "/api/v1/polls/1/votes",
            json={"choice": "A셰프"},
            headers={"X-Fingerprint": "test-fingerprint-123"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["choice"] == "A셰프"

    def test_create_vote_duplicate(self, client, sample_poll):
        """중복 투표 방지"""
        # 첫 번째 투표
        client.post(
            "/api/v1/polls/1/votes",
            json={"choice": "A셰프"},
            headers={"X-Fingerprint": "test-fingerprint-123"}
        )

        # 두 번째 투표 (중복)
        response = client.post(
            "/api/v1/polls/1/votes",
            json={"choice": "B셰프"},
            headers={"X-Fingerprint": "test-fingerprint-123"}
        )

        assert response.status_code == 409
        data = response.json()
        assert data["detail"]["error"] == "ALREADY_VOTED"

    def test_create_vote_invalid_choice(self, client, sample_poll):
        """잘못된 선택지"""
        response = client.post(
            "/api/v1/polls/1/votes",
            json={"choice": "없는셰프"},
            headers={"X-Fingerprint": "test-fingerprint-123"}
        )

        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error"] == "INVALID_CHOICE"

    def test_create_vote_poll_not_found(self, client):
        """존재하지 않는 투표"""
        response = client.post(
            "/api/v1/polls/999/votes",
            json={"choice": "A셰프"},
            headers={"X-Fingerprint": "test-fingerprint-123"}
        )

        assert response.status_code == 404
        data = response.json()
        assert data["detail"]["error"] == "POLL_NOT_FOUND"
