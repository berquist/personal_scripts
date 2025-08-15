from pathlib import Path
from typing import Dict, List, Tuple
from unittest.mock import mock_open, patch

import pytest
from your_module import (
    ValidationResult,
    parse_git_blame_ignore_revs,
    run_git_command,
    validate_commit_hashes,
    validate_git_blame_ignore_revs,
    validate_pre_commit_ci_commits,
)


@pytest.fixture
def mock_git_blame_ignore_revs_file():
    return """
# This is a comment
1234567890abcdef1234567890abcdef12345678
# Another comment
abcdef1234567890abcdef1234567890abcdef12
invalid_hash
"""


@pytest.fixture
def valid_hashes():
    return {
        2: "1234567890abcdef1234567890abcdef12345678",
        4: "abcdef1234567890abcdef1234567890abcdef12",
    }


@pytest.fixture
def lines(mock_git_blame_ignore_revs_file):
    return mock_git_blame_ignore_revs_file.strip().split("\n")


def test_parse_git_blame_ignore_revs(mock_git_blame_ignore_revs_file, valid_hashes):
    with patch("builtins.open", mock_open(read_data=mock_git_blame_ignore_revs_file)):
        lines, hashes = parse_git_blame_ignore_revs("dummy_path")
        assert hashes == valid_hashes
        assert len(lines) == 4


def test_run_git_command_success():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "output"
        result = run_git_command(["git", "status"])
        assert result == "output"


def test_run_git_command_failure():
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="git status", stderr="error"
        )
        with pytest.raises(RuntimeError, match="Git command failed"):
            run_git_command(["git", "status"])


def test_validate_commit_hashes(lines, valid_hashes):
    with patch("your_module.run_git_command") as mock_run_git_command:
        mock_run_git_command.return_value = "Commit message"
        strict_comment_errors, comment_diffs = validate_commit_hashes(
            valid_hashes, lines, strict_comments=True, strict_comments_git=True
        )
        assert strict_comment_errors == {2: "1234567890abcdef1234567890abcdef12345678"}
        assert comment_diffs == {4: ("Another comment", "Commit message")}


def test_validate_pre_commit_ci_commits(lines, valid_hashes):
    with patch("your_module.run_git_command") as mock_run_git_command:
        mock_run_git_command.return_value = (
            "abcdef1234567890abcdef1234567890abcdef12 Commit message"
        )
        missing_commits = validate_pre_commit_ci_commits(
            valid_hashes, lines, strict_comments=True, strict_comments_git=True
        )
        assert missing_commits == {}


def test_validate_git_blame_ignore_revs(lines, valid_hashes):
    with patch("your_module.parse_git_blame_ignore_revs") as mock_parse:
        mock_parse.return_value = (lines, valid_hashes)
        with patch("your_module.run_git_command") as mock_run_git_command:
            mock_run_git_command.return_value = "Commit message"
            result = validate_git_blame_ignore_revs(
                "dummy_path",
                call_git=True,
                strict_comments=True,
                strict_comments_git=True,
                pre_commit_ci=True,
            )
            assert isinstance(result, ValidationResult)
            assert result["valid_hashes"] == valid_hashes
            assert result["errors"] == {3: "invalid_hash"}
            assert result["strict_comment_errors"] == {
                2: "1234567890abcdef1234567890abcdef12345678"
            }
            assert result["comment_diffs"] == {4: ("Another comment", "Commit message")}
            assert result["missing_pre_commit_ci_commits"] == {}


def test_validate_git_blame_ignore_revs_file_not_found():
    with pytest.raises(FileNotFoundError):
        validate_git_blame_ignore_revs("non_existent_path")
