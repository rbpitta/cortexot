from app.domain.alarming.evaluate import evaluate_threshold_alarms


def test_evaluate_critical_temperature() -> None:
    alarms = evaluate_threshold_alarms("PUMP-01", "temperature", 96.0)
    assert len(alarms) == 1
    assert alarms[0].severity == "critical"


def test_evaluate_no_alarm_in_normal_band() -> None:
    assert evaluate_threshold_alarms("PUMP-01", "temperature", 70.0) == []
