import random
from pyscript import document  # type: ignore

# --- Variables & Data Types ---
MAX_HP = 100
player_hp = MAX_HP
enemy_hp = MAX_HP
is_game_over = False

# --- Lists (ท่าของศัตรู) ---
enemy_attacks = ["Sniper Shot", "Counter Ambush", "Poison Dart"]

# --- Functions ---
def update_ui(message):
    player_pct = max((player_hp / MAX_HP) * 100, 0)
    enemy_pct = max((enemy_hp / MAX_HP) * 100, 0)
    
    document.querySelector("#player-bar").style.width = f"{player_pct}%"
    document.querySelector("#enemy-bar").style.width = f"{enemy_pct}%"
    
    document.querySelector("#player-hp-text").innerText = f"{player_hp} / {MAX_HP}"
    document.querySelector("#enemy-hp-text").innerText = f"{enemy_hp} / {MAX_HP}"
    document.querySelector("#game-log").innerHTML = message

def check_game_over():
    global is_game_over
    
    if player_hp <= 0:
        is_game_over = True
        toggle_buttons(True)
        return '<i class="fa-solid fa-skull"></i> Mission Failed. Agent Down.'
    elif enemy_hp <= 0:
        is_game_over = True
        toggle_buttons(True)
        return '<i class="fa-solid fa-check-double"></i> Mission Accomplished. Target Eliminated.'
    
    return ""

def toggle_buttons(game_ended):
    attack_btn = document.querySelector("#btn-attack")
    heal_btn = document.querySelector("#btn-heal")
    reset_btn = document.querySelector("#btn-reset")
    
    if game_ended:
        attack_btn.classList.add("hidden")
        heal_btn.classList.add("hidden")
        reset_btn.classList.remove("hidden")
    else:
        attack_btn.classList.remove("hidden")
        heal_btn.classList.remove("hidden")
        reset_btn.classList.add("hidden")

def enemy_turn(current_log):
    global player_hp
    
    attack_name = random.choice(enemy_attacks)
    damage = random.randint(10, 20)
    
    player_hp -= damage
    if player_hp < 0:
        player_hp = 0
        
    log = f"{current_log} <br><i class='fa-solid fa-triangle-exclamation'></i> The Syndicate used <b>{attack_name}</b>, you taking <span class='text-red'>{damage} HP</span>."
    
    game_over_msg = check_game_over()
    if game_over_msg:
        log += f"<br><br><span class='text-dark'>{game_over_msg}</span>"
        
    update_ui(log)

# --- Event Handlers ---
def attack(event):
    global enemy_hp
    if is_game_over: return
    
    damage = random.randint(15, 25)
    enemy_hp -= damage
    if enemy_hp < 0:
        enemy_hp = 0
        
    log = f"<i class='fa-solid fa-crosshairs'></i> You strike the target for <span class='text-red'>{damage} DMG</span>."
    
    game_over_msg = check_game_over()
    if game_over_msg:
        update_ui(f"{log} <br><br><span class='text-dark'>{game_over_msg}</span>")
    else:
        enemy_turn(log)

def heal(event):
    global player_hp
    if is_game_over: return
    
    heal_amount = random.randint(20, 30)
    player_hp += heal_amount
    if player_hp > MAX_HP:
        player_hp = MAX_HP
        
    log = f"<i class='fa-solid fa-medkit'></i> Tactical recovery applied. Restored <span class='text-dark'>{heal_amount} HP</span>."
    enemy_turn(log)

def reset_game(event):
    global player_hp, enemy_hp, is_game_over
    player_hp = MAX_HP
    enemy_hp = MAX_HP
    is_game_over = False
    
    toggle_buttons(False)
    update_ui("<i class='fa-solid fa-satellite-dish'></i> Systems online. Awaiting your command.")