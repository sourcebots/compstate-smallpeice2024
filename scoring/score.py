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
        line_deficit = 0
        accumulated_score = 0
        touched_can = False
        lines_crossed = 0

        for action in actions.upper():
            if action == 'C':  # Touch can
                touched_can = True
            elif action == 'X':  # Reverse over line
                line_deficit += 1
            elif action == 'I':  # Forward over line
                if line_deficit > 0:
                    # If we have a line deficit, decrease it by one - we've just gone back
                    # forward over a line
                    line_deficit -= 1
                else:
                    # This is a new line passed; first, give points
                    accumulated_score += 2

                    # Then, if a can hasn't been touched, award another point
                    if not touched_can and lines_crossed != 0:
                        accumulated_score += 1

                    lines_crossed += 1

                    # Reset can touch
                    touched_can = False
            else:
                raise InvalidScoresheetException(f'Invalid action {action!r}')

        return accumulated_score


if __name__ == '__main__':
    # Test the scorer
    import sys

    test_cases = [
        ('', 0),
        ('I', 2),
        ('IX', 2),
        ('XI', 0),
        ('ICXI', 2),
        ('ICXII', 4),
        ('ICII', 7),
        ('ICCII', 7),
        ('ICICI', 6),
        ('I' * 5, 14),
        ('I' * 6, 17),
        ('I' * 7, 3 * 7 - 1),  # 1 full lap
        ('IIIIIICI', 19),
        ('I' * 13, 3 * 13 - 1),
        ('I' * 14, 3 * 14 - 1),  # 2 full laps
        ('IIIXXXIIIXXXI', 8),
        ('IXCII', 4)
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
