from os import system
from os import name as operating_system_type
from typing import Any
import asyncio
import random

class Cell:
    def __init__(self, x: int, y: int):
        self.properties = {
            'x-coord' : x,
            'y-coord' : y,
            'isPlayer' : False,
            'isEnemy' : False,
            'isBreakable' : True,
            'isPassable' : True,
            'isExplosive': False,
            'isAddSkill' : False,
            'isHighlight' : False
        }

    def property_update(self, key: str, value: Any):
        self.properties[key] = value

    def __repr__(self):
        # ray gun skill used, show board highlight
        if self.properties['isHighlight']:
            return '[#]'
        
        # if cell is the player or the enemy (or player2 in multiplayer)        
        elif self.properties['isPlayer']:
            return '[\u263a]'
        elif self.properties['isEnemy']:
            return '[\u263b]'
        
        # if cell contains a bomb
        elif self.properties['isExplosive']:
            return '[\u25ce]' 
        
        # Skill add cells
        elif self.properties['isAddSkill']:
            return '[\u2605]'
        
        # breakable and non-breakable cells
        elif not self.properties['isPassable'] and self.properties['isBreakable']:
            return '[☒]'     
        elif not self.properties['isPassable'] and not self.properties['isBreakable']:
            return '[\u25a3]'

        # else case
        else:
            return '[ ]'

class PlayableEntity:
    def __init__(self, skill_grant : str, entity : str = 'player_1'):
        """Initializes the player entity and stores a tuple indicating its initial position"""

        match skill_grant:
            case 'speed_boost':
                self.skills : dict[str, Any] = {
                    'speed_boost' : True,   
                    'quick_hand' : False,
                    'master_of_rayguns' : False
                    }
            case 'quick_hand':
                self.skills : dict[str, Any] = {
                    'speed_boost' : False,   
                    'quick_hand' : True,
                    'master_of_rayguns' : False
                    }
            case 'master_of_rayguns':
                self.skills : dict[str, Any] = {
                    'speed_boost' : False,   
                    'quick_hand' : False,
                    'master_of_rayguns' : True
                    }
            case _:
                self.skills : dict[str, Any] = {
                    'speed_boost' : False,   
                    'quick_hand' : False,
                    'master_of_rayguns' : False
                    }
        
        self.current_coordinate = (random.randint(0,5), random.randint(0,5)) if entity == 'player_1' else (random.randint(5,9), random.randint(5,9))
        
    def get_coordinate(self) -> tuple[int, int]:
        return self.current_coordinate
    
class SkillInstance:
    def __init__(self, name : str,max : int = 20):
        self.count = max
        self.name = name

    def decrement(self):
        if self.count > 0:
            self.count -= 1

    def increment(self):
        self.count += 1

class Grid:
    def __init__(self, length : int = 10):
        self.cell_grid = [[Cell(row_size, column_size) for column_size in range(length)] for row_size in range(length)]
        self.game_over = False

    def return_cell(self, coordinate : tuple[int, int]):
        row, column = coordinate
        return self.cell_grid[row][column]

    def draw_board(self):
        system('cls' if operating_system_type =='nt' else 'clear')
        for row in self.cell_grid:
            print(*row)
        message_out = self.living_entities_check()
        
        if self.game_over:
            print(message_out)

    def living_entities_check(self) -> str | None:
        playerFound = False
        enemyFound = False
        for _, cell_row  in enumerate(self.cell_grid):
            for _, cell in enumerate(cell_row):
                if cell.properties.get('isPlayer', True):
                    playerFound = True
                if cell.properties.get('isEnemy', True):
                    enemyFound = True

        message = ''

        if not playerFound:
            message = 'Player lost!'
            self.game_over = True
        if not enemyFound:
            message = 'Player won!'
            self.game_over = True        
        
        return message if message else None
        
def board_movement(grid: Grid, entity: str, entity_coordinate: tuple[int, int], action_type: str, skill_grant: str, skill_count: SkillInstance) -> tuple[int, int]:
    """Entity movement within the board. Returns the new position of said entity after input"""
    row, column = entity_coordinate
    row_offset, column_offset = 0, 0

    match action_type:
        case 'w' | 'up':
            row_offset -= 1
        case 's' | 'down':
            row_offset += 1
        case 'a' | 'left':
            column_offset -= 1
        case 'd' | 'right':
            column_offset += 1
        case _:
            return entity_coordinate

    def is_valid_move(test_row : int, test_column : int):
        if test_row not in range(len(grid.cell_grid)) or test_column not in range(len(grid.cell_grid)):
            return False
        cell = grid.return_cell((test_row, test_column))
        return cell.properties.get('isPassable', True) or cell.properties.get('isExplosive', True)

    # Try: 2 STEP
    if skill_grant == 'speed_boost':
        mid_row = row + row_offset
        mid_col = column + column_offset
        new_row = row + row_offset * 2
        new_col = column + column_offset * 2

        # First check: is the intermediate cell passable?
        if is_valid_move(mid_row, mid_col):
            # Then check: is the final cell passable?
            if is_valid_move(new_row, new_col):
                grid.return_cell(entity_coordinate).property_update(entity, False)
                target_cell = grid.return_cell((new_row, new_col))
                target_cell.property_update(entity, True)

                if target_cell.properties.get('isAddSkill', True):
                    skill_count.increment()
                    target_cell.property_update('isAddSkill', False)

                grid.draw_board()
                return (new_row, new_col)

    # if not passable, Try 1 STEP
    new_row = row + row_offset
    new_col = column + column_offset
    if is_valid_move(new_row, new_col):
        grid.return_cell(entity_coordinate).property_update(entity, False)
        target_cell = grid.return_cell((new_row, new_col))
        target_cell.property_update(entity, True)

        if target_cell.properties.get('isAddSkill', True):
            skill_count.increment()
            target_cell.property_update('isAddSkill', False)

        grid.draw_board()
        return (new_row, new_col)
    
    # if invalid target cell, retain coordinate
    return entity_coordinate



async def bomb_cell(grid: Grid, entity_coordinate : tuple[int, int], skill_grant : str | None = None):
    """Put down bomb in the coordinate location. Slightly different implementation when player/ai is granted 'Quick Hand' ability"""
    row, column = entity_coordinate

    async def delayed_bomb_explosion_logic(grid : Grid, bombed_cells_list : list[tuple[int, int]]):
        await asyncio.sleep(5)

        for bombed_row, bombed_col in bombed_cells_list:
            for row_offset, col_offset in [(-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)]:
                if 0 <= (row_offset + bombed_row) < len(grid.cell_grid) and 0 <= (col_offset + bombed_col) < len(grid.cell_grid):
                    new_row = bombed_row + row_offset
                    new_column = bombed_col + col_offset
                    offset_cell = grid.return_cell((new_row, new_column))

                    if offset_cell.properties.get('isBreakable', True):
                        offset_cell.property_update('isPassable', True)
                        offset_cell.property_update('isBreakable', False)
                        offset_cell.property_update('isPlayer', False)
                        offset_cell.property_update('isEnemy', False)
            
            bombed_cell = grid.return_cell((bombed_row, bombed_col))
            bombed_cell.property_update('isExplosive', False)
            bombed_cell.property_update('isPassable', True)
        grid.draw_board()

    if skill_grant == 'quick_hand':
        bombed_cells_list: list[tuple[int, int]] = []

        for row_offset, col_offset in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if 0 <= (row_offset + row) < len(grid.cell_grid) and 0 <= (col_offset + column) < len(grid.cell_grid):
                new_row = row + row_offset
                new_column = column + col_offset
                cell_offset = grid.return_cell((new_row, new_column))

                if cell_offset.properties.get('isPassable', True) and not (cell_offset.properties.get('isPlayer', False) or cell_offset.properties.get('isEnemy', False)):
                    cell_offset.property_update('isExplosive', True)
                    cell_offset.property_update('isPassable', True)
                    bombed_cells_list.append((new_row, new_column))

        grid.draw_board()

        asyncio.create_task(delayed_bomb_explosion_logic(grid, bombed_cells_list))
        return

    # if quick_hand skill is not granted
    cell = grid.return_cell((row, column))
    cell.property_update('isExplosive', True)
    grid.draw_board()

    asyncio.create_task(delayed_bomb_explosion_logic(grid, [(row, column)]))
    return

async def raygun_skill(grid: Grid, skill_activation_coordinate: tuple[int, int]):
    row, col = skill_activation_coordinate
    cross_cells: set[tuple[int, int]] = set()

    for i in range(10):
        cross_cells.add((row, i))
        cross_cells.add((i, col))

    for r, c in cross_cells:
        raygun_cell = grid.return_cell((r, c))
        raygun_cell.property_update('isPassable', True)
        raygun_cell.property_update('isHighlight', True)

    grid.draw_board()
    await asyncio.sleep(3)

    for r, c in cross_cells:
        raygun_cell = grid.return_cell((r, c))
        if (r, c) != skill_activation_coordinate:
            raygun_cell.property_update('isPlayer', False)
            raygun_cell.property_update('isEnemy', False)
        raygun_cell.property_update('isHighlight', False)

    grid.draw_board()
