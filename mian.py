import requests
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

# === CONFIG ===
API_TOKEN = os.getenv("cocapi")
PLAYER_TAG = "#9YLV0G0P9"
README_PATH = "README.md"

API_URL = f"https://api.clashofclans.com/v1/players/{PLAYER_TAG.replace('#', '%23')}"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}


def fetch_data():
    res = requests.get(API_URL, headers=HEADERS)
    if res.status_code != 200:
        raise Exception(f"API Error: {res.status_code} - {res.text}")
    return res.json()


def get_troop_icon(troop_name):
    """Get appropriate icon for each troop (PNG image or emoji fallback)"""
    # PNG images from your assets folder (you need to add these images)
    icon_map = {
        "Barbarian": "<img src='assets/troops/barbarian.png' width='50' height='50'>",
        "Archer": "<img src='assets/troops/archer.png' width='50' height='50'>",
        "Giant": "<img src='assets/troops/giant.png' width='50' height='50'>",
        "Goblin": "<img src='assets/troops/goblin.png' width='50' height='50'>",
        "Wall Breaker": "<img src='assets/troops/wallbreaker.png' width='50' height='50'>",
        "Balloon": "<img src='assets/troops/balloon.png' width='50' height='50'>",
        "Wizard": "<img src='assets/troops/wizard.png' width='50' height='50'>",
        "Healer": "<img src='assets/troops/healer.png' width='50' height='50'>",
        "Dragon": "<img src='assets/troops/dragon.png' width='50' height='50'>",
        "P.E.K.K.A": "<img src='assets/troops/pekka.png' width='50' height='50'>",
        "Minion": "<img src='assets/troops/minion.png' width='50' height='50'>",
        "Hog Rider": "<img src='assets/troops/hogrider.png' width='50' height='50'>",
        "Valkyrie": "<img src='assets/troops/valkyrie.png' width='50' height='50'>",
        "Golem": "<img src='assets/troops/golem.png' width='50' height='50'>",
        "Witch": "<img src='assets/troops/witch.png' width='50' height='50'>",
        "Lava Hound": "<img src='assets/troops/lavahound.png' width='50' height='50'>",
        "Bowler": "<img src='assets/troops/bowler.png' width='50' height='50'>",
        "Baby Dragon": "<img src='assets/troops/babydragon.png' width='50' height='50'>",
        "Miner": "<img src='assets/troops/miner.png' width='50' height='50'>",
        "Electro Dragon": "<img src='assets/troops/electrodragon.png' width='50' height='50'>",
        "Yeti": "<img src='assets/troops/yeti.png' width='50' height='50'>",
        "Dragon Rider": "<img src='assets/troops/dragonrider.png' width='50' height='50'>",
        "Apprentice Warden": "<img src='assets/troops/apprenticewarden.png' width='50' height='50'>"
    }
    return icon_map.get(troop_name, "⚔️")

def get_hero_icon(hero_name):
    """Get appropriate icon for each hero (PNG image or emoji fallback)"""
    icon_map = {
        "Barbarian King": "<img src='assets/heroes/barbarianking.png' width='50' height='50'>",
        "Archer Queen": "<img src='assets/heroes/archerqueen.png' width='50' height='50'>",
        "Grand Warden": "<img src='assets/heroes/grandwarden.png' width='50' height='50'>",
        "Royal Champion": "<img src='assets/heroes/royalchampion.png' width='50' height='50'>",
        "Battle Machine": "<img src='assets/heroes/battlemachine.png' width='50' height='50'>",
        "Battle Copter": "<img src='assets/heroes/battlecopter.png' width='50' height='50'>",
        "Minion Prince": "<img src='assets/heroes/minionprince.png' width='50' height='50'>"
    }
    return icon_map.get(hero_name, "👤")

def get_spell_icon(spell_name):
    """Get appropriate icon for each spell (PNG image or emoji fallback)"""
    icon_map = {
        "Lightning Spell": "<img src='assets/spells/lightning.png' width='50' height='50'>",
        "Healing Spell": "<img src='assets/spells/healing.png' width='50' height='50'>",
        "Rage Spell": "<img src='assets/spells/rage.png' width='50' height='50'>",
        "Jump Spell": "<img src='assets/spells/jump.png' width='50' height='50'>",
        "Freeze Spell": "<img src='assets/spells/freeze.png' width='50' height='50'>",
        "Clone Spell": "<img src='assets/spells/clone.png' width='50' height='50'>",
        "Invisibility Spell": "<img src='assets/spells/invisibility.png' width='50' height='50'>",
        "Poison Spell": "<img src='assets/spells/poison.png' width='50' height='50'>",
        "Earthquake Spell": "<img src='assets/spells/earthquake.png' width='50' height='50'>",
        "Haste Spell": "<img src='assets/spells/haste.png' width='50' height='50'>",
        "Skeleton Spell": "<img src='assets/spells/skeleton.png' width='50' height='50'>",
        "Bat Spell": "<img src='assets/spells/bat.png' width='50' height='50'>",
        "Recall Spell": "<img src='assets/spells/recall.png' width='50' height='50'>",
        "Overgrowth Spell": "<img src='assets/spells/overgrowth.png' width='50' height='50'>"

    }
    return icon_map.get(spell_name, "🪄")


def build_readme(data):
    name = data.get("name", "Unknown")
    trophies = data.get("trophies", 0)
    bestTrophies = data.get("bestTrophies", 0)
    expLevel = data.get("expLevel", 0)
    clan = data.get("clan", {}).get("name", "No Clan")
    clanLevel = data.get("clan", {}).get("clanLevel", 0)
    warStars = data.get("warStars", 0)
    attackWins = data.get("attackWins", 0)
    defenseWins = data.get("defenseWins", 0)
    builderHallLevel = data.get("builderHallLevel", 0)
    builderBaseTrophies = data.get("builderBaseTrophies", 0)
    role = data.get("role", "Member").title()
    townHallLevel = data.get("townHallLevel", 0)
    league = data.get("league", {}).get("name", "Unranked")
    clanCapitalContributions = data.get("clanCapitalContributions", 0)
    
    # Additional data fields
    achievements = data.get("achievements", [])
    labels = data.get("labels", [])
    troops = data.get("troops", [])
    heroes = data.get("heroes", [])
    spells = data.get("spells", [])
    
    # Calculate additional stats
    totalTroops = len([t for t in troops if t.get("village") == "home"])
    maxedTroops = len([t for t in troops if t.get("village") == "home" and t.get("level", 0) == t.get("maxLevel", 0)])
    totalHeroes = len([h for h in heroes if h.get("village") == "home"])
    maxedHeroes = len([h for h in heroes if h.get("village") == "home" and h.get("level", 0) == h.get("maxLevel", 0)])
    totalSpells = len(spells)
    maxedSpells = len([s for s in spells if s.get("level", 0) == s.get("maxLevel", 0)])
    
    # Filter and sort troops (only home village, level 5+)
    home_troops = [t for t in troops if t.get("village") == "home" and t.get("level", 0) >= 5]
    home_troops.sort(key=lambda x: x.get("level", 0), reverse=True)
    
    # Filter heroes (only home village)
    home_heroes = [h for h in heroes if h.get("village") == "home"]
    home_heroes.sort(key=lambda x: x.get("level", 0), reverse=True)
    
    # Sort spells by level
    spells.sort(key=lambda x: x.get("level", 0), reverse=True)
    
    # Get top achievements
    top_achievements = sorted(achievements, key=lambda x: x.get("stars", 0), reverse=True)[:5]
    
    # Calculate progress percentages
    troop_progress = (maxedTroops / totalTroops * 100) if totalTroops > 0 else 0
    hero_progress = (maxedHeroes / totalHeroes * 100) if totalHeroes > 0 else 0
    spell_progress = (maxedSpells / totalSpells * 100) if totalSpells > 0 else 0

    readme = f"""<div align="center">

# 🏰 {name} - Clash of Clans Profile

![Trophies](https://img.shields.io/badge/Trophies-{trophies:,}-gold?style=for-the-badge&logo=clash-of-clans)
![Town Hall](https://img.shields.io/badge/Town%20Hall-{townHallLevel}-orange?style=for-the-badge)
![Experience](https://img.shields.io/badge/Experience-{expLevel}-green?style=for-the-badge)
![Clan](https://img.shields.io/badge/Clan-{clan.replace(' ', '%20')}-blue?style=for-the-badge)

</div>

---

## 📊 **Player Overview**

<table>
<tr>
<td><b>🏆 Current Trophies</b></td><td>{trophies:,}</td>
<td><b>🥇 Best Trophies</b></td><td>{bestTrophies:,}</td>
</tr>
<tr>
<td><b>⭐ War Stars</b></td><td>{warStars}</td>
<td><b>⚔️ Attack Wins</b></td><td>{attackWins}</td>
</tr>
<tr>
<td><b>🛡️ Defense Wins</b></td><td>{defenseWins}</td>
<td><b>🏗️ Builder Hall</b></td><td>{builderHallLevel}</td>
</tr>
<tr>
<td><b>🏛️ Clan Capital</b></td><td>{clanCapitalContributions:,}</td>
<td><b>🥽 League</b></td><td>{league}</td>
</tr>
</table>

## 🏰 **Clan Information**

<table>
<tr>
<td><b>🦅 Clan Name</b></td><td>{clan}</td>
<td><b>📊 Clan Level</b></td><td>{clanLevel}</td>
<td><b>👤 Your Role</b></td><td>{role}</td>
</tr>
</table>

### 🏆 **War & Battle Statistics**

<table>
<tr>
<td><b>⚔️ Total Attack Wins</b></td><td>{attackWins:,}</td>
<td><b>🛡️ Total Defense Wins</b></td><td>{defenseWins:,}</td>
</tr>
<tr>
<td><b>⭐ War Stars Earned</b></td><td>{warStars}</td>
<td><b>🏛️ Clan Capital Contributions</b></td><td>{clanCapitalContributions:,}</td>
</tr>
</table>

## 📈 **Progress Overview**

<table>
<tr>
<td><b>⚔️ Troops Progress</b></td><td>{maxedTroops}/{totalTroops} Maxed</td><td><b>📊</b></td><td>{troop_progress:.1f}%</td>
</tr>
<tr>
<td><b>👑 Heroes Progress</b></td><td>{maxedHeroes}/{totalHeroes} Maxed</td><td><b>📊</b></td><td>{hero_progress:.1f}%</td>
</tr>
<tr>
<td><b>🪄 Spells Progress</b></td><td>{maxedSpells}/{totalSpells} Maxed</td><td><b>📊</b></td><td>{spell_progress:.1f}%</td>
</tr>
</table>

### 🎯 **Progress Visualization**

<div align="center">

#### ⚔️ **Troops Progress**
```
{'█' * int(troop_progress / 5)}{'░' * (20 - int(troop_progress / 5))} {troop_progress:.1f}%
```

#### 👑 **Heroes Progress**
```
{'█' * int(hero_progress / 5)}{'░' * (20 - int(hero_progress / 5))} {hero_progress:.1f}%
```

#### 🪄 **Spells Progress**
```
{'█' * int(spell_progress / 5)}{'░' * (20 - int(spell_progress / 5))} {spell_progress:.1f}%
```

</div>

## ⚔️ **Top Troops** (Level 5+)

<table>
"""

    # Add troops in rows of 3
    for i in range(0, len(home_troops), 3):
        readme += "<tr>\n"
        for j in range(3):
            if i + j < len(home_troops):
                troop = home_troops[i + j]
                icon = get_troop_icon(troop.get('name', ''))
                level = troop.get('level', 0)
                max_level = troop.get('maxLevel', 0)
                progress_bar = "█" * (level // 2) + "░" * ((max_level - level) // 2)
                readme += f"<td><b>{icon} {troop.get('name', '')}</b><br>{level}/{max_level}<br><code>{progress_bar}</code></td>\n"
            else:
                readme += "<td></td>\n"
        readme += "</tr>\n"

    readme += """</table>

## 👑 **Heroes Progress**

<table>
<tr>
"""

    # Add heroes horizontally with progress bars
    for hero in home_heroes:
        icon = get_hero_icon(hero.get('name', ''))
        level = hero.get('level', 0)
        max_level = hero.get('maxLevel', 0)
        progress_bar = "█" * (level // 2) + "░" * ((max_level - level) // 2)
        readme += f"<td align=\"center\"><b>{icon}<br>{hero.get('name', '')}</b><br>{level}/{max_level}<br><code>{progress_bar}</code></td>\n"

    readme += """</tr>
</table>

## 🪄 **Spells Progress**

<table>
"""

    # Add spells in rows of 4 with progress bars
    for i in range(0, len(spells), 4):
        readme += "<tr>\n"
        for j in range(4):
            if i + j < len(spells):
                spell = spells[i + j]
                icon = get_spell_icon(spell.get('name', ''))
                level = spell.get('level', 0)
                max_level = spell.get('maxLevel', 0)
                progress_bar = "█" * (level // 2) + "░" * ((max_level - level) // 2)
                readme += f"<td><b>{icon} {spell.get('name', '').replace(' Spell', '')}</b><br>{level}/{max_level}<br><code>{progress_bar}</code></td>\n"
            else:
                readme += "<td></td>\n"
        readme += "</tr>\n"

    readme += """</table>

## 🏆 **Top Achievements**

<table>
"""

    # Add top achievements
    for achievement in top_achievements:
        name = achievement.get('name', 'Unknown')
        stars = achievement.get('stars', 0)
        value = achievement.get('value', 0)
        target = achievement.get('target', 0)
        readme += f"<tr><td><b>🏅 {name}</b></td><td>{stars}⭐</td><td>{value:,}/{target:,}</td></tr>\n"

    readme += """</table>

## 🏷️ **Player Labels**

<div align="center">
"""

    # Add player labels
    for label in labels[:8]:  # Show first 8 labels
        name = label.get('name', 'Unknown')
        icon_url = label.get('iconUrls', {}).get('small', '')
        if icon_url:
            readme += f"<img src='{icon_url}' alt='{name}' width='50' height='50' style='margin: 5px;'>\n"
        else:
            readme += f"<span style='background: #f0f0f0; padding: 5px 10px; border-radius: 15px; margin: 5px; display: inline-block;'>{name}</span>\n"

    readme += """</div>

## 🎯 **Seasonal Challenges & Events**

<div align="center">

### 🏆 **Current Season Status**
![Season Pass](https://img.shields.io/badge/Season%20Pass-Active-brightgreen?style=for-the-badge)
![Clan Games](https://img.shields.io/badge/Clan%20Games-Participating-blue?style=for-the-badge)
![War League](https://img.shields.io/badge/War%20League-Competing-orange?style=for-the-badge)

</div>

## 📊 **Detailed Statistics**

<details>
<summary><b>🔍 Click to view detailed stats</b></summary>

### 🏠 **Home Village Stats**
- **Town Hall Level**: {townHallLevel}
- **Experience Level**: {expLevel}
- **Current Trophies**: {trophies:,}
- **Best Trophies**: {bestTrophies:,}
- **War Stars**: {warStars}
- **Attack Wins**: {attackWins:,}
- **Defense Wins**: {defenseWins:,}

### 🏗️ **Builder Base Stats**
- **Builder Hall Level**: {builderHallLevel}
- **Builder Base Trophies**: {builderBaseTrophies:,}

### 🏛️ **Clan Stats**
- **Clan Name**: {clan}
- **Clan Level**: {clanLevel}
- **Your Role**: {role}
- **Clan Capital Contributions**: {clanCapitalContributions:,}

### 📈 **Progress Metrics**
- **Troops**: {maxedTroops}/{totalTroops} maxed ({troop_progress:.1f}%)
- **Heroes**: {maxedHeroes}/{totalHeroes} maxed ({hero_progress:.1f}%)
- **Spells**: {maxedSpells}/{totalSpells} maxed ({spell_progress:.1f}%)

### 🎮 **Game Activity**
- **Total Troops**: {totalTroops}
- **Total Heroes**: {totalHeroes}
- **Total Spells**: {totalSpells}
- **Achievement Stars**: {sum([a.get('stars', 0) for a in achievements])}

</details>

---

<div align="center">

### 🔄 **Last Updated**: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}

![Clash of Clans](https://img.shields.io/badge/Clash%20of%20Clans-Active%20Player-brightgreen?style=for-the-badge&logo=supercell)
![GitHub](https://img.shields.io/badge/GitHub-Auto%20Updated-blue?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![API](https://img.shields.io/badge/API-Clash%20of%20Clans%20v1-red?style=for-the-badge)

---

### 📊 **Profile Statistics**
![Total Troops](https://img.shields.io/badge/Total%20Troops-{totalTroops}-blue?style=flat-square)
![Total Heroes](https://img.shields.io/badge/Total%20Heroes-{totalHeroes}-purple?style=flat-square)
![Total Spells](https://img.shields.io/badge/Total%20Spells-{totalSpells}-green?style=flat-square)
![War Stars](https://img.shields.io/badge/War%20Stars-{warStars}-gold?style=flat-square)

*📡 Auto-generated from the Clash of Clans API*

</div>"""

    return readme


def save_readme(content):
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)


def git_commit_push():
    subprocess.run(["git", "add", README_PATH], check=True)
    subprocess.run(["git", "commit", "-m", f"🔄 Auto-update Clash of Clans stats - {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
    subprocess.run(["git", "push"], check=True)


if __name__ == "__main__":
    print(" Fetching Clash of Clans data...")
    player_data = fetch_data()

    print(" Building colorful README.md...")
    readme_content = build_readme(player_data)
    save_readme(readme_content)

    print(" Committing and pushing changes...")
    git_commit_push()

    print(" Done! README.md updated and pushed.")
    print(f" Current trophies: {player_data.get('trophies', 0)}")
    
    