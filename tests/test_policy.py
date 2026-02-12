from skilllint.core.policy import DEFAULT_POLICY


def test_default_policy_structure():
    assert "quality" in DEFAULT_POLICY
    assert "readability_min" in DEFAULT_POLICY["quality"]
    assert "complexity_max" in DEFAULT_POLICY["quality"]
