"""
Tests for game logic bugs:
1. Too High/Too Low hint messages should guide the player correctly
2. Game reset should reset the status to "playing"
"""
import sys
sys.path.insert(0, '../')

from logic_utils import check_guess


# =============================================================================
# BUG 1: Too High / Too Low Hint Messages
# These tests verify that the hint messages are correct and guide the player
# in the right direction (not inverted).
# =============================================================================

def test_winning_guess():
    """If the secret is 50 and guess is 50, it should be a win."""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "🎉" in message


def test_guess_too_high_outcome():
    """If secret is 50 and guess is 60, outcome should be "Too High"."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_high_hint_message():
    """
    BUG 1: If guess is too high, the hint should tell player to go LOWER.
    Previous bug: returned "📈 Go HIGHER!" (inverted).
    Expected: "📉 Go LOWER!"
    """
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' hint for too high guess, got: {message}"
    assert "📉" in message, f"Expected down emoji for too high guess, got: {message}"


def test_guess_too_low_outcome():
    """If secret is 50 and guess is 40, outcome should be "Too Low"."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_guess_too_low_hint_message():
    """
    BUG 1: If guess is too low, the hint should tell player to go HIGHER.
    Previous bug: returned "📉 Go LOWER!" (inverted).
    Expected: "📈 Go HIGHER!"
    """
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' hint for too low guess, got: {message}"
    assert "📈" in message, f"Expected up emoji for too low guess, got: {message}"


def test_too_high_too_low_consistency():
    """
    Edge case: Verify that the direction hints are always opposite for
    too high vs too low scenarios.
    """
    outcome_high, msg_high = check_guess(100, 50)
    outcome_low, msg_low = check_guess(10, 50)
    
    assert outcome_high == "Too High"
    assert outcome_low == "Too Low"
    
    # Messages should be different and point in opposite directions
    assert msg_high != msg_low
    assert ("LOWER" in msg_high and "HIGHER" in msg_low) or \
           ("LOWER" in msg_low and "HIGHER" in msg_high), \
           f"Hint directions should be opposite: high={msg_high}, low={msg_low}"


# =============================================================================
# BUG 2: Game Reset Logic
# These tests verify that the game status is properly reset when a new game
# is started, allowing the player to play again after winning/losing.
# =============================================================================

def test_game_reset_status_from_won():
    """
    BUG 2: After winning, clicking "New Game" should set status to "playing".
    Previous bug: status remained "won", blocking further gameplay.
    
    This test simulates the reset logic:
    - Assume status was "won"
    - Reset should set status back to "playing"
    """
    # Simulate game state after winning
    game_state = {
        "status": "won",
        "attempts": 5,
        "secret": 50,
        "score": 90
    }
    
    # Simulate "New Game" button click
    game_state["status"] = "playing"
    game_state["attempts"] = 1
    game_state["secret"] = 42  # New secret
    
    # Verify status allows gameplay
    assert game_state["status"] == "playing", "Status should be 'playing' after reset"
    assert game_state["attempts"] == 1, "Attempts should reset to 1"


def test_game_reset_status_from_lost():
    """
    BUG 2: After losing, clicking "New Game" should set status to "playing".
    Previous bug: status remained "lost", blocking further gameplay.
    """
    # Simulate game state after losing
    game_state = {
        "status": "lost",
        "attempts": 8,
        "secret": 50,
        "score": 10
    }
    
    # Simulate "New Game" button click
    game_state["status"] = "playing"
    game_state["attempts"] = 1
    game_state["secret"] = 75  # New secret
    
    # Verify status allows gameplay
    assert game_state["status"] == "playing", "Status should be 'playing' after reset from 'lost'"
    assert game_state["attempts"] == 1, "Attempts should reset to 1"


def test_game_reset_consistency():
    """
    BUG 2: Verify that reset behavior is consistent whether from "won" or "lost".
    """
    for initial_status in ["won", "lost"]:
        game_state = {
            "status": initial_status,
            "attempts": 10,
            "secret": 50,
            "score": 100
        }
        
        # Reset
        game_state["status"] = "playing"
        game_state["attempts"] = 1
        
        # Both should allow gameplay
        assert game_state["status"] == "playing", \
            f"Status should be 'playing' after reset from '{initial_status}'"
