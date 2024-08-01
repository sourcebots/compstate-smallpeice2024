from __future__ import annotations


class InvalidScoresheetException(Exception):
    pass


class Scorer:
    def __init__(self, teams_data, arena_data):
        self.teams_data = teams_data
        self.arena_data = arena_data

    def calculate_scores(self) -> dict[str, int]:
        return {
            team_tla: self.calculate_score(team_data['actions'])
            for team_tla, team_data in self.teams_data.items()
        }

    def validate(self, other_data):
        pass

    @staticmethod
    def calculate_score(actions: str) -> int:
        lines_passed = 0
        line_deficit = 0
        num_cans = 0
        accumulated_score = 0

        for action in actions:
            action = action.upper()
            if action == 'A':  # Pick up can
                num_cans += 1
            elif action == 'V':  # Drop can
                if num_cans == 0:
                    raise InvalidScoresheetException('Cannot drop a can if there are no cans')
                num_cans -= 1
            elif action == 'X':  # Reverse over line
                line_deficit += 1
            elif action == 'I':  # Forward over line
                if line_deficit > 0:
                    # If we have a line deficit, decrease it by one - we've just gone back
                    # forward over a line
                    line_deficit -= 1
                else:
                    # This is a new line passed; first, we score 2^can_count points directly.
                    accumulated_score += 2 ** num_cans
                    # Then, we increase the number of lines passed by one
                    lines_passed += 1
                    # And if it's a full lap, that is, a multiple of 6 lines, we get 4 bonus
                    # points
                    if lines_passed % 6 == 0:
                        accumulated_score += 4
            else:
                raise InvalidScoresheetException(f'Invalid action {action!r}')

        # At the end, we get two bonus points for each can we still have
        accumulated_score += 2 * num_cans

        return accumulated_score


if __name__ == '__main__':
    # Test the scorer
    import sys

    test_cases = [
        ('', 0),
        ('A', 2),
        ('I', 1),
        ('AI', 4),
        ('IA', 3),
        ('AVI', 1),
        ('XAIV', 0),
        ('AAAI', 14),
        ('AAAIVVV', 8),
        ('IIIII', 5),
        ('IIIIII', 10),
        ('IIIIIXI', 5),
        ('IIIIIXII', 10),
        ('IIIIIIXI', 10),
        ('IIIIIIX', 10),
        ('IIIIIIXII', 11),
        ('I' * 6 * 2, 6 * 2 + 4 * 2),
    ]

    failures = 0

    for test_case, expected in test_cases:
        actual = Scorer.calculate_score(test_case)
        if actual != expected:
            print(f'Test case {test_case!r} failed. Expected {expected}, got {actual}', file=sys.stderr)
            failures += 1

    if failures:
        print(f'{failures} test cases failed', file=sys.stderr)
        sys.exit(1)
    else:
        print('All test cases passed', file=sys.stderr)
        sys.exit(0)
