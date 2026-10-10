import base64
from backend.app import app, fetch_media_from_url_or_payload

def test_payloads():
    print("--- Testing Media URL & Payload Scanner Backend ---")

    # Test 1: Relative sample path
    b1, fn1, ct1, dom1 = fetch_media_from_url_or_payload('samples/sample_authentic_human.wav')
    print(f"Test 1 (Relative Path): {fn1} | {ct1} | {dom1} | Bytes: {len(b1)}")

    # Test 2: HTML Audio Tag with Base64 payload
    payload_tag = '<audio controls src="data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="></audio>'
    b2, fn2, ct2, dom2 = fetch_media_from_url_or_payload(payload_tag)
    print(f"Test 2 (Embedded HTML Tag): {fn2} | {ct2} | {dom2} | Bytes: {len(b2)}")

    # Test 3: Flask Endpoint Test
    with app.test_client() as client:
        res = client.post('/api/analyze-url', json={'url': 'samples/sample_ai_clone_scam.wav'})
        print(f"Test 3 (/api/analyze-url): Status {res.status_code} | Success: {res.json.get('success')} | Verdict: {res.json.get('results', {}).get('verdict_title')}")

if __name__ == "__main__":
    test_payloads()
