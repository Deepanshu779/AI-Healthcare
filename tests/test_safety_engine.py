from safety_engine import assess_safety


def test_normal_assessment_is_routine():
    result = assess_safety(symptoms=["headache"], temperature="37", spo2="98", severity="Mild")
    assert result["level"] == "Routine"


def test_low_oxygen_is_emergency():
    result = assess_safety(symptoms=["fatigue"], temperature="37", spo2="91", severity="Mild")
    assert result["level"] == "Emergency"


def test_red_flag_is_emergency():
    result = assess_safety(symptoms=["difficulty breathing"], temperature="37", spo2="98", severity="Mild")
    assert result["level"] == "Emergency"


def test_high_fever_is_urgent():
    result = assess_safety(symptoms=["fever"], temperature="39", spo2="98", severity="Mild")
    assert result["level"] == "Urgent"
