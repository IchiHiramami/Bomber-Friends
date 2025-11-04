import keyboard
import random
import asyncio
from Refactored_Bomb_Friend_Game import board_movement, bomb_cell
from Refactored_Bomb_Friend_Game import Grid, PlayableEntity, SkillInstance, raygun_skill
from typing import Any
from time import sleep
from os import system
from os import name as operating_system_type

def choose_ability(player_label: str) -> str:
    prompt = f"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                            CHOOSE YOUR ABILITY    [{player_label}]                                                          ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║        RAYGUN [1]                         SPEEDBOOST [2]                   QUICKHAND  [3]                RANDOM   [4]         ║
║                                                                                                                               ║
║  ░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓►        ╔═╗                                  ( )                                ╔════╗            ║
║                                     ╚═╬═╦═╦═╦═╦═╦═╦═╦═╦═╦═╦═►            ( )>───[💥]                        ║ ?  ║            ║
║  A focused beam of light           Dash forward with speed             Toss explosive surprises            Let fate decide    ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""
    while True:
        system('cls' if operating_system_type =='nt' else 'clear')
        choice = input(prompt).strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        sleep(5)

# game_initialization
def board_generation(game_board : Grid):
    global occupied_cell
    #breakable blocks
    while len(occupied_cell) < 15:
        cell_coord = (random.randint(0,9), random.randint(0,9))
        if cell_coord not in occupied_cell:
            occupied_cell.add(cell_coord)
            cell = game_board.return_cell(cell_coord)
            cell.property_update('isPassable', False)
            cell.property_update('isBreakable', False)
    
    #unbreakable blocks
    while len(occupied_cell) < 25:
        cell_coord = (random.randint(0,9), random.randint(0,9))
        if cell_coord not in occupied_cell:
            occupied_cell.add(cell_coord)
            cell = game_board.return_cell(cell_coord)
            cell.property_update('isPassable', False)
            cell.property_update('isBreakable', True)

    #skill point adder cells
    while len(occupied_cell) < 30:
        cell_coord = (random.randint(0,9), random.randint(0,9))
        if cell_coord not in occupied_cell:
            occupied_cell.add(cell_coord)
            cell = game_board.return_cell(cell_coord)
            cell.property_update('isAddSkill', True)
            
    game_board.draw_board()


def game_init() -> Any | None:

    global occupied_cell
    skill_set = ['speed_boost', 'quick_hand', 'master_of_rayguns']
    skill_map : dict[str, str]= {
        '1': 'master_of_rayguns',
        '2': 'speed_boost',
        '3': 'quick_hand',
        '4': random.choice(skill_set)
    }

    input("""
╔════════════════════════════════════════════════════╗
║                                                    ║
║        ██████╗  █████╗ ███╗   ███╗███████╗         ║
║       ██╔════╝ ██╔══██╗████╗ ████║██╔════╝         ║
║       ██║  ███╗███████║██╔████╔██║█████╗           ║
║       ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝           ║
║       ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗         ║
║        ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝         ║
║                                                    ║
║        Welcome to the Ultimate Grid Bomber!        ║
║                                                    ║
║        Player 1 Controls:                          ║
║          Move: W A S D                             ║
║          Place Bomb: E                             ║
║          Special Skill: Q                          ║
║                                                    ║
║        Player 2 Controls:                          ║
║          Move: Arrow Keys                          ║
║          Place Bomb: P                             ║
║          Special Bomb: O                           ║
║                                                    ║
║        Objective:                                  ║
║          Outsmart your opponent. Bomb wisely.      ║
║          Break through blocks. Stay alive.         ║
║                                                    ║
║        Press any key to begin...                   ║
╚════════════════════════════════════════════════════╝
""")
    
    while True:
        gameplay_mode = input('=======================\nBOMBER FRIENDS! IN CLI!\n[s] - single player\n[m] - 2 player\n=======================\n>>>')
        gameplay_mode = gameplay_mode.strip()
        if gameplay_mode in ['s', 'm']:
            break
        print("Invalid choice. Please only choose between [s] - single player and [m] - multiplayer.")

    game_board = Grid()
    global occupied_cell

    match gameplay_mode.lower():
        case 'm':
            skill_input_1 = choose_ability("PLAYER 1!")
            skill_input_2 = choose_ability("PLAYER 2!")

            skill_1 = skill_map.get(skill_input_1, random.choice(skill_set))
            skill_2 = skill_map.get(skill_input_2, random.choice(skill_set))

            max_skill_1 = SkillInstance(skill_1)
            player_1 = PlayableEntity(skill_1)
            player_1_coords = player_1.get_coordinate()
            player_1_cell = game_board.return_cell(player_1_coords)
            player_1_cell.property_update('isPlayer', True)
            occupied_cell.add(player_1_coords)

            max_skill_2 = SkillInstance(skill_2)
            player_2 = PlayableEntity(skill_2, entity='player_2')
            player_2_coords = player_2.get_coordinate()
            player_2_cell = game_board.return_cell(player_2_coords)
            player_2_cell.property_update('isEnemy', True)
            occupied_cell.add(player_2_coords)

            print(f"PLAYER 1 Skill: {skill_1}\nPLAYER 2 Skill: {skill_2}")
            sleep(5)

            board_generation(game_board)

            tasks = [
                asyncio.create_task(player_movement_handling(game_board, player_1_coords, skill_1, max_skill_1)),
                asyncio.create_task(player_movement_handling_2(game_board, player_2_coords, skill_2, max_skill_2))
            ]

        case 's':

            skill_input_1 = choose_ability("PLAYER 1!")

            skill_1 = skill_map.get(skill_input_1, random.choice(skill_set))
            skill_2 = random.choice(skill_set)

            max_skill_1 = SkillInstance(skill_1, max = 3 if skill_1 == 'master_of_rayguns' else 20)
            player_1 = PlayableEntity(skill_1)
            player_1_coords = player_1.get_coordinate()
            player_1_cell = game_board.return_cell(player_1_coords)
            player_1_cell.property_update('isPlayer', True)
            occupied_cell.add(player_1_coords)

            max_skill_2 = SkillInstance(skill_2, max = 3 if skill_2 == 'master_of_rayguns' else 20)
            player_2 = PlayableEntity(skill_2, entity='player_2')
            player_2_coords = player_2.get_coordinate()
            player_2_cell = game_board.return_cell(player_2_coords)
            player_2_cell.property_update('isEnemy', True)
            occupied_cell.add(player_2_coords)

            print(skill_1, '\n', skill_2)
            sleep(5)

            board_generation(game_board)
            cache : list[str] = []
            tasks = [
                asyncio.create_task(player_movement_handling(game_board, player_1_coords, skill_1, max_skill_1)),
                asyncio.create_task(enemy_AI_handling(game_board, player_2_coords, cache, skill_2, max_skill_2))
            ]

        case _:
            print('Invalid game mode was selected')
            return
    
    return (game_board, tasks)

async def player_movement_handling(grid : Grid, coords: tuple[int, int], skill: str, max_count : SkillInstance):
    while not grid.game_over:
        if keyboard.is_pressed('w'):
            coords = board_movement(grid, 'isPlayer', coords, 'w', skill, max_count)
            await asyncio.sleep(0.3)
    
        elif keyboard.is_pressed('a'):
            coords = board_movement(grid, 'isPlayer', coords, 'a', skill, max_count)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('s'):
            coords = board_movement(grid, 'isPlayer', coords, 's', skill, max_count)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('d'):
            coords = board_movement(grid, 'isPlayer', coords, 'd', skill, max_count)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('q'):
            if max_count.name == 'quick_hand':
                if max_count.count > 0:
                    await bomb_cell(grid, coords, skill)
                    max_count.decrement()
                    print(f"Quick Hand uses left: {max_count.count}")
            elif max_count.name == 'master_of_rayguns':
                if max_count.count > 0:
                    await raygun_skill(grid, coords)
                    max_count.decrement()
                    print(f"Raygun uses left: {max_count.count}")
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('e'):
            await bomb_cell(grid, coords)
            await asyncio.sleep(0.3)

        await asyncio.sleep(0.05)

async def player_movement_handling_2(grid : Grid, coords: tuple[int, int], skill: str, max_count : SkillInstance):
    while not grid.game_over:
        if keyboard.is_pressed('up'):
            coords = board_movement(grid, 'isEnemy', coords, 'up', skill, max_count)
            await asyncio.sleep(0.3)        

        elif keyboard.is_pressed('left'):
            coords = board_movement(grid, 'isEnemy', coords, 'left', skill, max_count)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('down'):
            coords = board_movement(grid, 'isEnemy', coords, 'down', skill, max_count)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('right'):
            coords = board_movement(grid, 'isEnemy', coords, 'right', skill, max_count)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('o'):
            if max_count.name == 'quick_hand':
                if max_count.count > 0:
                    await bomb_cell(grid, coords, skill)
                    max_count.decrement()
                    print(f"Quick Hand uses left: {max_count.count}")
            elif max_count.name == 'master_of_rayguns':
                if max_count.count > 0:
                    await raygun_skill(grid, coords)
                    max_count.decrement()
                    print(f"Raygun uses left: {max_count.count}")
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('p'):
            await bomb_cell(grid, coords)
            await asyncio.sleep(0.3)
        
        await asyncio.sleep(0.05)

async def enemy_AI_handling(game_board : Grid, AI_coordinate : tuple[int,int] , cache : list[str],  skill : str, max_count : SkillInstance):
    options : list[str] = ['up', 'down', 'left', 'right', 'p', 'o']
    while not game_board.game_over:
        filtered : list[str] = options.copy()

        choice : str = random.choice(filtered)
        if choice == 'p':
            await bomb_cell(game_board , AI_coordinate, skill)
        elif choice == 'o':
            if max_count.name == 'quick_hand':
                if max_count.count > 0:
                    await bomb_cell(game_board, AI_coordinate, skill)
                    max_count.decrement()
            elif max_count.name == 'master_of_rayguns':
                if max_count.count > 0:
                    await raygun_skill(game_board, AI_coordinate)
            await asyncio.sleep(0.3)
        else:
            temp_coord = board_movement(game_board, 'isEnemy', AI_coordinate, choice, skill , max_count)
            if AI_coordinate != temp_coord:
                AI_coordinate = temp_coord
                await asyncio.sleep(0.25)

        cache.append(choice)
        if len(cache) > 10:
            cache.pop(0)

        await asyncio.sleep(0.3)

async def main():
    result = game_init()
    if not result:
        return
    grid, tasks = result

    while not grid.game_over:
        await asyncio.sleep(0.1)

    for task in tasks:
        task.cancel()

    print("Game Over.")

if __name__ == '__main__':
    occupied_cell : set[tuple[int,int]] = set()
    asyncio.run(main())