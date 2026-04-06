"""
State machine transition tests — most critical test file.
Covers every valid and invalid transition as defined in VALID_TRANSITIONS.
"""
from .conftest import register_user, login_user, auth_headers, create_application


def _setup(client):
    register_user(client)
    token = login_user(client)
    app_id = create_application(client, token).get_json()['data']['id']
    return token, app_id


def _transition(client, token, app_id, new_stage):
    return client.patch(
        f'/api/applications/{app_id}/stage',
        json={'stage': new_stage},
        headers=auth_headers(token),
    )


# ── From APPLIED ─────────────────────────────────────────────────────────────

def test_applied_to_screening_valid(client):
    token, app_id = _setup(client)
    assert _transition(client, token, app_id, 'SCREENING').status_code == 200


def test_applied_to_rejected_valid(client):
    token, app_id = _setup(client)
    assert _transition(client, token, app_id, 'REJECTED').status_code == 200


def test_applied_to_withdrawn_valid(client):
    token, app_id = _setup(client)
    assert _transition(client, token, app_id, 'WITHDRAWN').status_code == 200


def test_applied_to_interview_invalid(client):
    token, app_id = _setup(client)
    assert _transition(client, token, app_id, 'INTERVIEW').status_code == 422


def test_applied_to_offer_invalid(client):
    token, app_id = _setup(client)
    assert _transition(client, token, app_id, 'OFFER').status_code == 422


def test_applied_to_applied_invalid(client):
    token, app_id = _setup(client)
    assert _transition(client, token, app_id, 'APPLIED').status_code == 422


# ── From SCREENING ───────────────────────────────────────────────────────────

def test_screening_to_interview_valid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    assert _transition(client, token, app_id, 'INTERVIEW').status_code == 200


def test_screening_to_rejected_valid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    assert _transition(client, token, app_id, 'REJECTED').status_code == 200


def test_screening_to_withdrawn_valid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    assert _transition(client, token, app_id, 'WITHDRAWN').status_code == 200


def test_screening_to_applied_invalid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    assert _transition(client, token, app_id, 'APPLIED').status_code == 422


def test_screening_to_offer_invalid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    assert _transition(client, token, app_id, 'OFFER').status_code == 422


# ── From INTERVIEW ───────────────────────────────────────────────────────────

def test_interview_to_offer_valid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    _transition(client, token, app_id, 'INTERVIEW')
    assert _transition(client, token, app_id, 'OFFER').status_code == 200


def test_interview_to_rejected_valid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    _transition(client, token, app_id, 'INTERVIEW')
    assert _transition(client, token, app_id, 'REJECTED').status_code == 200


def test_interview_to_applied_invalid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    _transition(client, token, app_id, 'INTERVIEW')
    assert _transition(client, token, app_id, 'APPLIED').status_code == 422


# ── From OFFER ───────────────────────────────────────────────────────────────

def test_offer_to_rejected_valid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    _transition(client, token, app_id, 'INTERVIEW')
    _transition(client, token, app_id, 'OFFER')
    assert _transition(client, token, app_id, 'REJECTED').status_code == 200


def test_offer_to_withdrawn_valid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    _transition(client, token, app_id, 'INTERVIEW')
    _transition(client, token, app_id, 'OFFER')
    assert _transition(client, token, app_id, 'WITHDRAWN').status_code == 200


def test_offer_to_interview_invalid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'SCREENING')
    _transition(client, token, app_id, 'INTERVIEW')
    _transition(client, token, app_id, 'OFFER')
    assert _transition(client, token, app_id, 'INTERVIEW').status_code == 422


# ── Terminal: REJECTED ────────────────────────────────────────────────────────

def test_rejected_to_anything_invalid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'REJECTED')
    for stage in ['APPLIED', 'SCREENING', 'INTERVIEW', 'OFFER', 'WITHDRAWN']:
        resp = _transition(client, token, app_id, stage)
        assert resp.status_code == 422, f'Expected 422 for REJECTED → {stage}'


# ── Terminal: WITHDRAWN ───────────────────────────────────────────────────────

def test_withdrawn_to_anything_invalid(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'WITHDRAWN')
    for stage in ['APPLIED', 'SCREENING', 'INTERVIEW', 'OFFER', 'REJECTED']:
        resp = _transition(client, token, app_id, stage)
        assert resp.status_code == 422, f'Expected 422 for WITHDRAWN → {stage}'


# ── Error message quality ─────────────────────────────────────────────────────

def test_invalid_transition_error_message_lists_valid_stages(client):
    token, app_id = _setup(client)
    resp = _transition(client, token, app_id, 'INTERVIEW')
    assert resp.status_code == 422
    error = resp.get_json()['error']
    assert 'SCREENING' in error or 'REJECTED' in error or 'WITHDRAWN' in error


def test_terminal_stage_error_message(client):
    token, app_id = _setup(client)
    _transition(client, token, app_id, 'REJECTED')
    resp = _transition(client, token, app_id, 'SCREENING')
    assert resp.status_code == 422
    assert 'terminal' in resp.get_json()['error'].lower()
