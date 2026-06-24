from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.importers.wc_importer import load_tournament_data
from backend.tournament import calculate_group_standings
tournament_data = load_tournament_data()
real_teams = tournament_data["teams"]
real_matches = tournament_data["matches"]



app = FastAPI(
    title="World Cup Prediction Engine",
    description="Tournament engine starter API",
    version="0.1.0",
)


class ScoreUpdate(BaseModel):
    home_score: int
    away_score: int


@app.get("/")
def home():
    return {
        "message": "World Cup Prediction Engine API is running"
    }


@app.get("/teams")
def get_teams():
    return real_teams


@app.get("/groups")
def get_groups():
    groups = {}

    for team in real_teams:
        group_name = team["group"]

        if group_name not in groups:
            groups[group_name] = []

        groups[group_name].append(team)

    return groups

@app.get("/matches")
def get_matches():
    return {
        "total_matches": len(real_matches),
        "matches": real_matches,
    }

@app.post("/matches/{match_id}/score")
def update_match_score(match_id: int, score: ScoreUpdate):
    if score.home_score < 0 or score.away_score < 0:
        raise HTTPException(
            status_code=400,
            detail="Scores cannot be negative"
        )

    for match in real_matches:
        if match["match_id"] == match_id:
            match["home_score"] = score.home_score
            match["away_score"] = score.away_score
            match["status"] = "completed"
            match["time_elapsed"] = "finished"

            return {
                "message": "Match score updated successfully",
                "match": match,
            }

    raise HTTPException(status_code=404, detail="Match not found")


@app.get("/standings/{group_name}")
def get_group_standings(group_name: str):
    group_name = group_name.upper()

    valid_groups = {
        team["group"].upper()
        for team in real_teams
    }

    if group_name not in valid_groups:
        raise HTTPException(
            status_code=404,
            detail=f"Group {group_name} not found"
        )

    standings = calculate_group_standings(
        group_name,
        real_teams,
        real_matches
    )

    return {
        "group": group_name,
        "standings": standings,
    }
    
# @app.get("/api/world-cup/fixtures")
# def world_cup_fixtures():
#     try:
#         data = get_world_cup_fixtures()

#         return {
#             "results_found": data.get("results", 0),
#             "fixtures": data.get("response", [])
#         }

#     except Exception as error:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Could not fetch football data: {str(error)}"
#         )
        
@app.get("/api/tournament/teams")
def get_real_teams():
    return {
        "total_teams": len(real_teams),
        "teams": real_teams,
    }


@app.get("/api/tournament/groups")
def get_real_groups():
    groups = {}

    for team in real_teams:
        group_name = team["group"]

        if group_name not in groups:
            groups[group_name] = []

        groups[group_name].append(team)

    return {
        "total_groups": len(groups),
        "groups": groups,
    }


@app.get("/api/tournament/matches")
def get_real_matches():
    return {
        "total_matches": len(real_matches),
        "matches": real_matches,
    }