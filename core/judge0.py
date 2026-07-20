import os
import time
import base64
import requests

JUDGE0_HOST = os.environ.get('JUDGE0_API_HOST', '')
JUDGE0_KEY = os.environ.get('JUDGE0_API_KEY', '')
PYTHON_LANGUAGE_ID = 71
POLL_INTERVAL = 1.5  # seconds between polls
MAX_WAIT = 15  # seconds before timeout


def build_source(user_code: str, tests_json: dict) -> str:
    """Concatenate user code with test assertions from the tests JSONField."""
    test_code = tests_json.get('test_code', '')
    return f"{user_code}\n\n{test_code}"


def submit_to_judge0(source: str) -> str:
    """Submit source code to Judge0 and return the submission token."""
    url = f"https://{JUDGE0_HOST}/submissions?base64_encoded=true"
    headers = {
        'X-RapidAPI-Key': JUDGE0_KEY,
        'X-RapidAPI-Host': JUDGE0_HOST,
        'Content-Type': 'application/json',
    }
    payload = {
        'language_id': PYTHON_LANGUAGE_ID,
        'source_code': base64.b64encode(source.encode()).decode(),
        'stdin': '',
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()['token']
    except requests.Timeout:
        raise TimeoutError('Judge0 submission timed out.')
    except requests.RequestException as e:
        raise ConnectionError(f'Judge0 submission failed: {e}')


def poll_result(token: str) -> dict:
    """Poll Judge0 until the submission is processed. Returns result dict."""
    url = f"https://{JUDGE0_HOST}/submissions/{token}"
    headers = {
        'X-RapidAPI-Key': JUDGE0_KEY,
        'X-RapidAPI-Host': JUDGE0_HOST,
    }
    params = {'base64_encoded': 'true', 'fields': 'status,stdout,stderr,status_id'}

    start = time.time()
    while True:
        if time.time() - start > MAX_WAIT:
            raise TimeoutError('Judge0 result polling timed out.')
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.Timeout:
            raise TimeoutError('Judge0 polling timed out.')
        except requests.RequestException as e:
            raise ConnectionError(f'Judge0 polling failed: {e}')

        status_id = data.get('status_id')
        # status_id 1 = In Queue, 2 = Processing — keep polling
        if status_id in (1, 2):
            time.sleep(POLL_INTERVAL)
            continue

        # Decode base64 output fields
        def decode(value):
            if value:
                return base64.b64decode(value).decode('utf-8', errors='replace')
            return ''

        stdout = decode(data.get('stdout'))
        stderr = decode(data.get('stderr'))
        # status_id 3 = Accepted (all good). Anything else = failure.
        passed = status_id == 3

        return {
            'passed': passed,
            'stdout': stdout,
            'stderr': stderr,
            'status_id': status_id,
        }
