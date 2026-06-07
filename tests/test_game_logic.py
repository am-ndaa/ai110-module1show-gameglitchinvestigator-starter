import sys
from pathlib import Path

# Add parent directory to path to import logic_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import check_guess, get_range_for_difficulty


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "📈 Go HIGHER!")


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "📉 Go LOWER!")


class TestGetRangeForDifficulty:
    """Test the difficulty range logic - catches backwards Hard/Normal bug."""

    def test_easy_range(self):
        """Easy should be the smallest range (1-20)."""
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20

    def test_normal_range(self):
        """Normal should be medium difficulty (1-100)."""
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100

    def test_hard_range_is_harder_than_normal(self):
        """CRITICAL: Hard difficulty should have a SMALLER range than Normal."""
        easy_low, easy_high = get_range_for_difficulty("Easy")
        normal_low, normal_high = get_range_for_difficulty("Normal")
        hard_low, hard_high = get_range_for_difficulty("Hard")

        easy_size = easy_high - easy_low
        normal_size = normal_high - normal_low
        hard_size = hard_high - hard_low

        # This test catches the bug where Hard returned (1, 50) - same size as Normal!
        # Correct ordering: Easy < Hard < Normal (by difficulty/range size)
        assert (
            easy_size < hard_size < normal_size
        ), (
            f"Bug detected: Difficulty ranges backwards!\n"
            f"Easy range size: {easy_size}, Hard range size: {hard_size}, Normal range size: {normal_size}\n"
            f"Hard should be smaller (harder) than Normal."
        )

    def test_unknown_difficulty_defaults_to_normal(self):
        """Unknown difficulty should default to Normal range."""
        low, high = get_range_for_difficulty("Unknown")
        assert low == 1
        assert high == 100
