import hashlib


def generate_voter_id(ip: str, fingerprint: str, poll_id: int) -> str:
    """
    IP + 브라우저 fingerprint + poll_id로 고유 voter_id 생성

    중복투표 방지용 - 같은 IP + 같은 브라우저에서 같은 투표에 중복 불가

    Args:
        ip: 클라이언트 IP 주소
        fingerprint: 브라우저 fingerprint (프론트에서 생성)
        poll_id: 투표 ID

    Returns:
        64자리 SHA256 해시 문자열
    """
    raw = f"{ip}:{fingerprint}:{poll_id}"
    return hashlib.sha256(raw.encode()).hexdigest()
