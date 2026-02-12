from skilllint.core.policy import should_fail, DEFAULT_POLICY


def test_should_fail_on_critical():
    by_sev = {"critical": 1, "high": 0}
    assert should_fail(by_sev, ["critical", "high"]) is True


def test_should_pass_when_clean():
    by_sev = {"medium": 2, "low": 1}
    assert should_fail(by_sev, ["critical", "high"]) is False


def test_default_policy_structure():
    assert "quality" in DEFAULT_POLICY
    assert "security" in DEFAULT_POLICY
    assert "readability_min" in DEFAULT_POLICY["quality"]
    assert "fail_on" in DEFAULT_POLICY["security"]
