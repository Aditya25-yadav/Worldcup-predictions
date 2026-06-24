from pathlib import Path
import csv


# This file is inside backend/importers/
# parents[0] = importers
# parents[1] = backend
# parents[2] = project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "datasets" / "raw" / "worldcup2026"

TEAMS_FILE = DATA_FOLDER / "worldcup2026.teams.csv"
GAMES_FILE = DATA_FOLDER / "worldcup2026.games.csv"


def to_int(value):
    """
    Converts CSV values such as '1' into integer 1.
    Returns None for empty values.
    """
    if value is None or value == "":
        return None

    return int(value)


def to_bool(value):
    """
    CSV may store booleans as True/False strings.
    """
    return str(value).strip().lower() == "true"


def load_teams():
    """
    Reads the 48 teams from worldcup2026.teams.csv.
    Returns a list of clean team dictionaries.
    """

    teams = []

    with open(TEAMS_FILE, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            team = {
                "team_id": to_int(row["id"]),
                "name": row["name_en"],
                "fifa_code": row["fifa_code"],
                "iso2": row["iso2"],
                "group": row["groups"],
                "flag_url": row["flag"],
            }

            teams.append(team)

    return teams


def create_team_lookup(teams):
    """
    Makes it easy to find a team using its ID.

    Example:
    lookup[1] -> Mexico team dictionary
    """

    lookup = {}

    for team in teams:
        lookup[team["team_id"]] = team

    return lookup


def load_group_matches():
    """
    Reads all 72 group-stage fixtures from worldcup2026.games.csv.

    Important:
    The dataset uses 0-0 before a match begins.
    We convert that to None because 0-0 is not a real result
    until finished == True.
    """

    teams = load_teams()
    team_lookup = create_team_lookup(teams)

    matches = []

    with open(GAMES_FILE, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Ignore non-group games if the dataset adds knockout matches later
            if row["type"].strip().lower() != "group":
                continue

            home_team_id = to_int(row["home_team_id"])
            away_team_id = to_int(row["away_team_id"])

            home_team = team_lookup.get(home_team_id)
            away_team = team_lookup.get(away_team_id)

            # Skip a row if team IDs do not match the teams dataset
            if home_team is None or away_team is None:
                continue

            is_finished = to_bool(row["finished"])

            if is_finished:
                home_score = to_int(row["home_score"])
                away_score = to_int(row["away_score"])
                status = "completed"
            else:
                home_score = None
                away_score = None
                status = "scheduled"

            match = {
                "match_id": to_int(row["id"]),
                "stage": "GROUP",
                "group": row["group"],
                "matchday": to_int(row["matchday"]),
                "kickoff_utc": row["date"],
                "local_date": row["local_date"],
                "stadium_id": to_int(row["stadium_id"]),
                "home_team_id": home_team_id,
                "home_team": home_team["name"],
                "home_fifa_code": home_team["fifa_code"],
                "away_team_id": away_team_id,
                "away_team": away_team["name"],
                "away_fifa_code": away_team["fifa_code"],
                "home_score": home_score,
                "away_score": away_score,
                "status": status,
                "time_elapsed": row["time_elapsed"],
            }

            matches.append(match)

    return matches


def load_tournament_data():
    """
    Main function for the rest of your backend.

    Returns:
    {
        "teams": [...48 teams...],
        "matches": [...72 group matches...]
    }
    """

    return {
        "teams": load_teams(),
        "matches": load_group_matches(),
    }