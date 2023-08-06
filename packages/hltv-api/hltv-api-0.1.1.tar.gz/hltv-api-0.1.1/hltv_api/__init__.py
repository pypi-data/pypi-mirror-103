__version__ = '0.1.0'

from datetime import datetime

import pytz

from hltv_api.client import fetch

# Must be set to server time
CURRENT_TIMEZONE = pytz.timezone('America/New_York')


def timestamp_to_utc(timestamp: str) -> datetime:
    naive = datetime.fromtimestamp(int(timestamp) / 1000)
    return CURRENT_TIMEZONE.localize(naive)


async def get_team_id(name: str):
    pass


async def get_upcoming_matches(parsed_page):
    r = parsed_page
    match_tables = r.find_all("table", {"class": "match-table"})

    # No upcoming matches
    if match_tables and len(match_tables) == 1:
        return []

    output = []
    upcoming_matches = match_tables[0].find_all("tr", {"class": "team-row"})
    for match in upcoming_matches:
        output.append({
            "time": timestamp_to_utc(match.find("span")["data-unix"]).isoformat(),
            "team_1": match.find("a", {"class": "team-name team-1"}).text,
            "team_2": match.find("a", {"class": "team-name team-2"}).text,
            "match_page": match.find("a", {"class": "matchpage-button"})["href"]
        })
    return output


async def get_team_info(team_id: int):
    r = await fetch(f"https://www.hltv.org/team/{team_id}/teamid={team_id}")

    name = r.select_one("body > div.bgPadding > div > div.colCon > div.contentCol > div.teamProfile > "
                        "div.standard-box.profileTopBox.clearfix > div.flex > div.profile-team-container"
                        ".text-ellipsis > div.profile-team-info > h1").text

    ranking = r.select_one("#infoBox > div.relative > div.chart-container.core-chart-container "
                           "> div > div.ranking-info > div.wrap > span.value").text.replace("#", "")

    twitter = r.select_one("body > div.bgPadding > div > div.colCon > div.contentCol > "
                           "div.teamProfile > div.standard-box.profileTopBox.clearfix > "
                           "div.flex > div.socialMediaButtons > a")["href"]

    average_player_age = r.select_one("body > div.bgPadding > div > div.colCon > div.contentCol > "
                                      "div.teamProfile > div.standard-box.profileTopBox.clearfix > "
                                      "div.profile-team-stats-container > div:nth-child(3) > span").text

    coach = r.select_one("body > div.bgPadding > div > div.colCon > div.contentCol > div.teamProfile > "
                         "div.standard-box.profileTopBox.clearfix > div.profile-team-stats-container > "
                         "div:nth-child(4) > a").text

    logo_url = r.select_one("body > div.bgPadding > div > div.colCon > div.contentCol > div.teamProfile > "
                            "div.standard-box.profileTopBox.clearfix > div.flex > div.profile-team-container"
                            ".text-ellipsis > div.profile-team-logo-container > img")["src"]

    region = r.select_one("body > div.bgPadding > div > div.colCon > div.contentCol > div.teamProfile "
                          "> div.standard-box.profileTopBox.clearfix > div.flex > div.profile-team-container"
                          ".text-ellipsis > div.profile-team-info > div > img")
    region_name = region["title"]
    region_flag_url = region["src"]

    # Get Roster
    roster = map(lambda p: {
        "full_name": p.td.a.div.img["title"],
        "photo": p.td.a.div.img["src"],
        "nick": p.select_one("a > div.players-cell.playersBox-playernick.text-ellipsis").div.text.strip(),
        "country": p.select_one("a > div.players-cell.playersBox-playernick.text-ellipsis").img["title"],
        "flag_url": p.select_one("a > div.players-cell.playersBox-playernick.text-ellipsis").img["src"],
        "status": p.select_one("div.players-cell.status-cell").text.strip(),
        "rating": p.select_one("div.players-cell.rating-cell").text.strip(),
    }, r.select("#rosterBox > div.playersBox-wrapper > table > tbody > tr"))

    return {
        "name": name,
        "region_name": region_name,
        "region_flag_url": region_flag_url,
        "logo_url": logo_url,
        "ranking": ranking,
        "twitter": twitter,
        "average_player_age": average_player_age,
        "coach": coach,
        "active_roster": list(roster),
        "upcoming_matches": await get_upcoming_matches(r)
    }
