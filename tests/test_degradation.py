from simulator.degradation_scenarios import DegradationState, ScenarioName, apply_bearing_degradation


def test_bearing_degradation_increases_vibration_after_ramp() -> None:
    base = {
        "temperature": 70.0,
        "pressure": 7.0,
        "vibration": 3.0,
        "current": 17.0,
        "rpm": 1750.0,
    }
    unchanged = apply_bearing_degradation(base, elapsed_min=3.0)
    assert unchanged["vibration"] == 3.0

    degraded = apply_bearing_degradation(base, elapsed_min=10.0)
    assert float(degraded["vibration"]) > 3.0
    assert float(degraded["current"]) > 17.0


def test_degradation_state_tracks_scenario() -> None:
    state = DegradationState()
    state.start(ScenarioName.BEARING_DEGRADATION)
    assert state.active
    assert state.scenario == ScenarioName.BEARING_DEGRADATION
    state.stop()
    assert not state.active
