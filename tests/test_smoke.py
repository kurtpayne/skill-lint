from pathlib import Path
from skilllint.core.file_handler import iter_candidate_files


def test_iter_candidate_files_single_file(tmp_path: Path) -> None:
    p = tmp_path / "skill.yaml"
    p.write_text("name: demo")
    files = list(iter_candidate_files(p))
    assert files == [p]
