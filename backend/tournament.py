def get_team_name(team_id: int, teams: list) -> str:
    """
    Find a team name using the team_id from the imported CSV dataset.
    """

    for team in teams:
        if team["team_id"] == team_id:
            return team["name"]

    return "Unknown Team"


def calculate_group_standings(group_name: str, teams: list, matches: list):
    """
    Calculates standings for one group using the real 48-team dataset.
    """

    group_name = group_name.upper()

    group_teams = [
        team for team in teams
        if team["group"].upper() == group_name
    ]

    standings = {}

    for team in group_teams:
        standings[team["team_id"]] = {
            "team_id": team["team_id"],
            "team_name": team["name"],
            "fifa_code": team["fifa_code"],
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
        }

    completed_matches = [
        match for match in matches
        if match["group"].upper() == group_name
        and match["status"] == "completed"
    ]

    for match in completed_matches:
        home_team_id = match["home_team_id"]
        away_team_id = match["away_team_id"]

        home = standings[home_team_id]
        away = standings[away_team_id]

        home_score = match["home_score"]
        away_score = match["away_score"]

        home["played"] += 1
        away["played"] += 1

        home["goals_for"] += home_score
        home["goals_against"] += away_score

        away["goals_for"] += away_score
        away["goals_against"] += home_score

        if home_score > away_score:
            home["wins"] += 1
            home["points"] += 3
            away["losses"] += 1

        elif away_score > home_score:
            away["wins"] += 1
            away["points"] += 3
            home["losses"] += 1

        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    for team in standings.values():
        team["goal_difference"] = team["goals_for"] - team["goals_against"]

    return sorted(
        standings.values(),
        key=lambda team: (
            team["points"],
            team["goal_difference"],
            team["goals_for"],
            team["team_name"],
        ),
        reverse=True,
    )