from pathlib import Path

from skilllint.core.intel import load_intel_bundle, resolve_intel_config


def test_intel_defaults_force_offline_safety():
    policy = {"security": {"intel": {"mode": "bundled", "ai_assisted": True, "allow_remote": True}}}
    cfg = resolve_intel_config(policy)
    assert cfg.mode == "bundled"
    assert cfg.ai_assisted is False
    assert cfg.allow_remote is False


def test_intel_file_mode_loads_custom_signatures(tmp_path: Path):
    sig_file = tmp_path / "custom.yaml"
    sig_file.write_text(
        """
version: 1
patterns:
  injection:
    - id: custom-rule
      regex: "ignore all safeguards"
      severity: high
""".strip(),
        encoding="utf-8",
    )
    policy = {"security": {"intel": {"mode": "file", "file": str(sig_file)}}}
    cfg = resolve_intel_config(policy)
    bundle = load_intel_bundle(cfg)
    assert "injection" in bundle.patterns
    assert any(x["id"] == "custom-rule" for x in bundle.patterns["injection"])


def test_intel_disabled_returns_empty():
    cfg = resolve_intel_config({"security": {"intel": {"mode": "disabled"}}})
    bundle = load_intel_bundle(cfg)
    assert bundle.patterns == {}
