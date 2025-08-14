#!/usr/bin/env python3

import requests
import subprocess
import json
from datetime import datetime

# Clash of Clans API Configuration
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjJjYTJmOTNmLTYxNzItNGRhYS1hOThjLTcyNTA4ZjgzYWU5YSIsImlhdCI6MTc1NTE3OTczOCwic3ViIjoiZGV2ZWxvcGVyL2Y0ODExZDMwLWM4MTUtZTY1NS1hMGJjLTBkYjRkMmFiZTQzMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwMy4xNjAuMTk3LjEwOCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.kpIiUvTBSio7k7KFA1fnHSDT8fKgoyuXMuUMBLpndHdL_6UnTpmnq2ubR7fY8azewyz1AmwCilJYjMjvUm8--g"
PLAYER_TAG = "#9YLV0G0P9"  # Your player tag
API_URL = f"https://api.clashofclans.com/v1/players/{PLAYER_TAG.replace('#', '%23')}"

def run_git(command):
    """Run git command"""
    result = subprocess.run(f"git {command}", shell=True, capture_output=True, text=True)
    return result.returncode == 0

def get_clash_data():
    """Fetch player data from Clash of Clans API"""
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def format_number(num):
    """Format numbers with commas"""
    return f"{num:,}"

def get_achievement_stars(achievements, name):
    """Get stars for a specific achievement"""
    for achievement in achievements:
        if achievement['name'] == name:
            return achievement['stars'], achievement.get('value', 0), achievement.get('target', 0)
    return 0, 0, 0

def generate_readme(data):
    """Generate README content from API data"""
    
    # Basic player info
    name = data['name']
    tag = data['tag']
    th_level = data['townHallLevel']
    exp_level = data['expLevel']
    trophies = data['trophies']
    best_trophies = data['bestTrophies']
    war_stars = data['warStars']
    attack_wins = data['attackWins']
    defense_wins = data['defenseWins']
    
    # Builder base info
    bh_level = data['builderHallLevel']
    bb_trophies = data['builderBaseTrophies']
    best_bb_trophies = data['bestBuilderBaseTrophies']
    
    # Clan info
    clan = data['clan']
    clan_name = clan['name']
    clan_tag = clan['tag']
    clan_level = clan['clanLevel']
    
    # League info
    league = data['league']['name'] if 'league' in data else "Unranked"
    bb_league = data['builderBaseLeague']['name'] if 'builderBaseLeague' in data else "Unranked"
    
    # Role and preferences
    role = data.get('role', 'member').title()
    war_pref = "Opted In ✅" if data.get('warPreference') == 'in' else "Opted Out ❌"
    clan_capital_contrib = data.get('clanCapitalContributions', 0)
    
    # Get key achievements
    achievements = data.get('achievements', [])
    gold_stars, gold_value, _ = get_achievement_stars(achievements, 'Gold Grab')
    elixir_stars, elixir_value, _ = get_achievement_stars(achievements, 'Elixir Escapade')
    de_stars, de_value, _ = get_achievement_stars(achievements, 'Heroic Heist')
    obstacles_stars, obstacles_value, _ = get_achievement_stars(achievements, 'Nice and Tidy')
    walls_stars, walls_value, _ = get_achievement_stars(achievements, 'Wall Buster')
    
    # Heroes
    heroes = data.get('heroes', [])
    
    # Get top troops (home village only, level 5+)
    troops = [t for t in data.get('troops', []) if t['village'] == 'home' and t['level'] >= 5]
    troops.sort(key=lambda x: x['level'], reverse=True)
    
    # Get top spells
    spells = data.get('spells', [])
    spells.sort(key=lambda x: x['level'], reverse=True)
    
    # Labels
    labels = [label['name'] for label in data.get('labels', [])]
    
    readme_content = f"""# 🏰 Clash of Clans Player Profile - {name}

<div align="center">

[![Player Tag](https://img.shields.io/badge/Player%20Tag-{tag.replace('#', '%23')}-blue?style=for-the-badge)](https://link.clashofclans.com/en?action=OpenPlayerProfile&tag={tag.replace('#', '')})
[![Town Hall](https://img.shields.io/badge/Town%20Hall-Level%20{th_level}-orange?style=for-the-badge)](https://clashofclans.com)
[![Trophies](https://img.shields.io/badge/Trophies-{trophies}-yellow?style=for-the-badge)](https://clashofclans.com)
[![Experience](https://img.shields.io/badge/Experience-Level%20{exp_level}-green?style=for-the-badge)](https://clashofclans.com)

</div>

---

## 🎯 Player Overview

| **Stat** | **Value** |
|----------|-----------|
| **Name** | {name} |
| **Tag** | {tag} |
| **Town Hall Level** | {th_level} |
| **Experience Level** | {exp_level} |
| **Current Trophies** | {format_number(trophies)} 🏆 |
| **Best Trophies** | {format_number(best_trophies)} 🏆 |
| **War Stars** | {war_stars} ⭐ |
| **Attack Wins** | {attack_wins} ⚔️ |
| **Defense Wins** | {defense_wins} 🛡️ |

## 🏘️ Builder Base Stats

| **Stat** | **Value** |
|----------|-----------|
| **Builder Hall Level** | {bh_level} |
| **Builder Base Trophies** | {format_number(bb_trophies)} 🏆 |
| **Best Builder Base Trophies** | {format_number(best_bb_trophies)} 🏆 |

## 🏰 Clan Information

| **Detail** | **Value** |
|------------|-----------|
| **Clan Name** | {clan_name} 🦅 |
| **Clan Tag** | {clan_tag} |
| **Clan Level** | {clan_level} |
| **Role** | {role} |
| **War Preference** | {war_pref} |
| **Clan Capital Contributions** | {format_number(clan_capital_contrib)} 💰 |

## 🏆 League Status

| **League Type** | **League** |
|-----------------|------------|
| **Home Village** | {league} |
| **Builder Base** | {bb_league} |

## 🏅 Key Achievements

| **Achievement** | **Progress** | **Status** |
|-----------------|--------------|------------|
| **Gold Grab** | {format_number(gold_value)} Gold | {"🌟" * gold_stars}{"⭐" * (3-gold_stars)} |
| **Elixir Escapade** | {format_number(elixir_value)} Elixir | {"🌟" * elixir_stars}{"⭐" * (3-elixir_stars)} |
| **Heroic Heist** | {format_number(de_value)} Dark Elixir | {"🌟" * de_stars}{"⭐" * (3-de_stars)} |
| **Nice and Tidy** | {format_number(obstacles_value)} Obstacles | {"🌟" * obstacles_stars}{"⭐" * (3-obstacles_stars)} |
| **Wall Buster** | {format_number(walls_value)} Walls | {"🌟" * walls_stars}{"⭐" * (3-walls_stars)} |

## ⚔️ Heroes"""

    # Add heroes section
    if heroes:
        readme_content += "\n\n| **Hero** | **Level** | **Equipment** |\n|----------|-----------|---------------|\n"
        for hero in heroes:
            equipment_text = ""
            if 'equipment' in hero and hero['equipment']:
                equipment_text = ", ".join([f"{eq['name']} (Lv.{eq['level']})" for eq in hero['equipment']])
            readme_content += f"| **{hero['name']}** | {hero['level']}/{hero['maxLevel']} | {equipment_text} |\n"

    # Add troops section
    if troops:
        readme_content += "\n## ⚔️ Top Troops\n\n| **Troop** | **Level** | **Max Level** |\n|-----------|-----------|---------------|\n"
        for troop in troops[:10]:  # Top 10 troops
            readme_content += f"| {troop['name']} | {troop['level']}/{troop['maxLevel']} | {'🗡️' if 'Barbarian' in troop['name'] else '🏹' if 'Archer' in troop['name'] else '🐉' if 'Dragon' in troop['name'] else '⚔️'} |\n"

    # Add spells section
    if spells:
        readme_content += "\n## 🪄 Spells\n\n| **Spell** | **Level** | **Max Level** |\n|-----------|-----------|---------------|\n"
        for spell in spells[:8]:  # Top 8 spells
            readme_content += f"| {spell['name']} | {spell['level']}/{spell['maxLevel']} | {'⚡' if 'Lightning' in spell['name'] else '💚' if 'Healing' in spell['name'] else '😤' if 'Rage' in spell['name'] else '🪄'} |\n"

    # Add labels section
    if labels:
        readme_content += "\n## 🎮 Player Labels\n\n"
        label_emojis = {"Base Designing": "🎨", "Farming": "🌾", "Competitive": "🏆", "Friendly": "😊", "Talkative": "💬"}
        for label in labels:
            emoji = label_emojis.get(label, "🏷️")
            readme_content += f"- {emoji} **{label}**\n"

    # Footer
    readme_content += f"""

---

<div align="center">

**Last Updated**: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}  
**War Preference**: {war_pref}  
**Status**: Active Player

[![Clash of Clans](https://img.shields.io/badge/Clash%20of%20Clans-Player-blue?style=for-the-badge&logo=supercell)](https://clashofclans.com)

</div>"""

    return readme_content

def main():
    print("🤖 Fetching latest Clash of Clans stats...")
    
    # Get data from API
    clash_data = get_clash_data()
    if not clash_data:
        print("❌ Failed to fetch Clash data")
        return
    
    print(f"✅ Successfully fetched data for {clash_data['name']}")
    
    # Generate README content
    readme_content = generate_readme(clash_data)
    
    # Write to README file
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("📝 README.md updated successfully!")
    
    # Git operations
    print("📤 Staging changes...")
    if not run_git("add README.md"):
        print("❌ Failed to stage changes")
        return
    
    # Check if there are changes to commit
    result = subprocess.run("git diff --staged --quiet", shell=True)
    if result.returncode == 0:
        print("ℹ️ No changes to commit")
        return
    
    # Commit changes
    commit_msg = f"Update Clash of Clans stats - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    print(f"💾 Committing: {commit_msg}")
    if not run_git(f'commit -m "{commit_msg}"'):
        print("❌ Failed to commit changes")
        return
    
    # Push changes
    print("🚀 Pushing to remote...")
    if not run_git("push"):
        print("❌ Failed to push changes")
        return
    
    print("✅ Successfully updated and pushed Clash of Clans stats!")
    print(f"🏆 Current trophies: {clash_data['trophies']}")
    print(f"🏰 Town Hall: {clash_data['townHallLevel']}")

if __name__ == "__main__":
    main()