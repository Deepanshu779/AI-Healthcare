from safety import assess_safety


def test_normal_case_is_routine():
    result = assess_safety(symptoms=["mild cough"], spo2=98, temperature=36.8, age=20)
    assert result.level == "Routine"


def test_low_spo2_is_emergency():
    result = assess_safety(symptoms=["cough"], spo2=89, temperature=37.0, age=30)
    assert result.level == "Emergency"
    assert any("SpO2" in alert for alert in result.alerts)


def test_red_flag_is_emergency():
    result = assess_safety(symptoms=["chest pain", "difficulty breathing"], spo2=96, temperature=37, age=45)
    assert result.level == "Emergency"
