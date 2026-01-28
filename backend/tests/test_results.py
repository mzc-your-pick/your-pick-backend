import pytest


class TestResultAPI:
    """결과 조회 API 테스트"""

    def test_get_results_empty(self, client, sample_poll):
        """투표가 없을 때 결과 조회"""
        response = client.get("/api/v1/polls/1/results")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["public_votes"]["total"] == 0

    def test_get_results_with_votes(self, client, sample_poll):
        """투표 후 결과 조회"""
        # 여러 투표 생성 (서로 다른 fingerprint)
        for i in range(3):
            client.post(
                "/api/v1/polls/1/votes",
                json={"choice": "A셰프"},
                headers={"X-Fingerprint": f"fingerprint-{i}"}
            )

        for i in range(2):
            client.post(
                "/api/v1/polls/1/votes",
                json={"choice": "B셰프"},
                headers={"X-Fingerprint": f"fingerprint-b-{i}"}
            )

        response = client.get("/api/v1/polls/1/results")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["public_votes"]["total"] == 5
        assert data["data"]["public_votes"]["results"]["A셰프"]["count"] == 3
        assert data["data"]["public_votes"]["results"]["B셰프"]["count"] == 2

    def test_get_results_with_comparison(self, client, sample_poll):
        """패널 vs 대중 비교"""
        # A셰프에게 투표 (대중)
        client.post(
            "/api/v1/polls/1/votes",
            json={"choice": "A셰프"},
            headers={"X-Fingerprint": "fp-1"}
        )

        response = client.get("/api/v1/polls/1/results")
        data = response.json()

        # 비교 분석 확인
        assert data["data"]["comparison"] is not None
        assert data["data"]["panel_result"]["A셰프"] == 70

    def test_get_results_not_found(self, client):
        """존재하지 않는 투표 결과 조회"""
        response = client.get("/api/v1/polls/999/results")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"]["error"] == "POLL_NOT_FOUND"
