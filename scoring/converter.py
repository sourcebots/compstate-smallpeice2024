from sr.comp.scorer import Converter as BaseConverter


class Converter(BaseConverter):
    def form_to_score(self, match, form):
        score = super().form_to_score(match, form)
        del score['arena_zones']
        return score

    def form_team_to_score(self, form, zone_id):
        actions = form.get(f'robot_actions_{zone_id}') or ''
        return {
            **super().form_team_to_score(form, zone_id),
            'actions': actions,
        }

    def score_to_form(self, score):
        form = super().score_to_form(score)

        for info in score['teams'].values():
            zone_id = info['zone']
            form[f'robot_actions_{zone_id}'] = info.get('actions', '')

        return form

    def match_to_form(self, match):
        form = super().match_to_form(match)
        for zone_id, tla in enumerate(match.teams):
            if tla:
                form[f'robot_actions_{zone_id}'] = ''

        return form
