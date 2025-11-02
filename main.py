# Bomber Friends the CLI Game
# ===========================
# CLI game taking advantage 
# Python OOP Capabilities

# BASIC BUILD UP SESSION
# Session 1: October 28 19:27 - 20:13 >>> Basic Class Definition, Interobject actionability
# Session 2: October 28 21:58 - 23:59 >>> Experimentation with Threading
# Session 3: October 29 00:27 - 02:01 >>> Random saSpawnpoint, Assignment of Properties, Grid Reflection
# Session 4: October 29 02:50 - 03:41 >>> Refactoring and Debugging
# Session 5: October 29 09:31 - 11:13 >>> Player and Enemy Movement, 2 - Player Gamemode
# Session 6: October 29 11:47 - 12:52 >>> Asynchronization of Functions
# Session 7: Octover 29 13:36 - 14:30 >>> Removal of Threading and Replacing with Asyncio. TODO: Critical Bug in Board Creation Re: Player vs People
# Session 8: October 29 16:03 - 17:37 >>> SuperSkills Shit TODO: Critical Bug disallowing player to move after bomb is placed -> most likely due to the implementation where players should not be passable
# Session 9: October 30 09:42 - 11:30 >>> Gave up, initiated refactoring since classes were not modular, too code specific

# REFACTORING SESSION
# Session 1: October 31 16:20 - 16:50 >> Started Refactoring, I hate myself for it
# Session 2: November 1 11:00 - 12:30 >> Starting to regret refactoring
# Session 3: November 1 14:32 - 18:47 >> FIXED: Critical bug disallowing movement, Code is back to original functionality before the refactoring session
# Session 4: November 1 19:54
from random import randint
import keyboard
import random
import asyncio
from time import sleep

from bfGame import Grid, playableCharacter

def init():
    grid = Grid()
    player1 = playableCharacter('Basic')
    skillGrant = random.choice(['speedBoost', 'IEDSpecialist', 'fastHand'])

    match skillGrant:
        case 'speedBoost':
            player1.propUpdate(skillGrant, True)
            print("SKILL GRANTED:", skillGrant)
        case 'IEDSpecialist':
            player1.propUpdate(skillGrant, True)
            print("SKILL GRANTED:", skillGrant)
        case 'fastHand':
            player1.propUpdate(skillGrant, True)
            print("SKILL GRANTED:", skillGrant)
        case _:
            for skill in player1.skills.keys():
                player1.propUpdate(skill, True) 
                print("SKILL GRANTED:", skillGrant)
    
    sleep(4)
    return grid, player1

def movementHandling(grid : Grid,coords : tuple[int, int], action : str, entityType : str, isBoosted : bool = False) -> tuple[int,int]:
    newCords = grid.move(coords, action, entityType, isBoosted)
    return newCords if newCords is not None else coords

async def playerMovementHandling(grid : Grid, playerCords : tuple[int, int], skillGranted : str | None = None):
    spdBst = True if skillGranted == 'speedBoost' else False
    IEDSkill = True if skillGranted == 'IEDSpecialist' else False #type: ignore <<<<
    fastHand = True if skillGranted == 'fastHand' else False
    while True:
        if grid.gameOver:
            break
        # WASD player movement
        if keyboard.is_pressed('w'):
            playerCords = movementHandling(grid ,playerCords, 'w', 'isPlayer', spdBst)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('a'):
            playerCords = movementHandling(grid ,playerCords, 'a', 'isPlayer', spdBst)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('s'):
            playerCords = movementHandling(grid ,playerCords, 's', 'isPlayer', spdBst)
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('d'):            
            playerCords = movementHandling(grid ,playerCords, 'd', 'isPlayer', spdBst)
            await asyncio.sleep(0.3)

        # Bomb placement move
        elif keyboard.is_pressed('e'):
            await grid.bombPlace(playerCords, fastHand)
            await asyncio.sleep(0.3)

        await asyncio.sleep(0.05)

async def enemyMovementHandling(grid : Grid, enemyCords: tuple[int, int], skillGranted : str | None = None):
    while True:
        if grid.gameOver:
            break
        # Arrow Key Enemy Movement
        if keyboard.is_pressed('up'):
            enemyCords = movementHandling(grid ,enemyCords, 'up', 'isEnemy')
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('down'):
            enemyCords = movementHandling(grid ,enemyCords, 'down', 'isEnemy')
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('left'):
            enemyCords = movementHandling(grid ,enemyCords, 'left', 'isEnemy')
            await asyncio.sleep(0.3)

        elif keyboard.is_pressed('right'):            
            enemyCords = movementHandling(grid ,enemyCords, 'right', 'isEnemy')
            await asyncio.sleep(0.3)
        # Bomb placement move for enemy
        elif keyboard.is_pressed('p'):
            await grid.bombPlace(enemyCords)
            await asyncio.sleep(0.3)

        await asyncio.sleep(0.05)

async def enemyAIHandling(grid : Grid, enemyCords : tuple[int,int] , cache : list[str]):
    options : list[str] = ['up', 'down', 'left', 'right', 'p']
    while True:
        if grid.gameOver:
            break
        filtered : list[str] = options.copy()

        # If 'p' was the last move, block it for 10 turns
        if 'p' in cache:
            filtered.remove('p')

        choice : str = random.choice(filtered)
        if choice == 'p':
            await grid.bombPlace(enemyCords)
        else:
            newCords = grid.move(enemyCords, choice, 'isEnemy')
            if newCords is not None:
                enemyCords = newCords
                await asyncio.sleep(1)

        cache.append(choice)
        if len(cache) > 10:
            cache.pop(0)

        await asyncio.sleep(0.05)

async def main():
        # youkoso
    gamemode = input('=======\nWELCOME\n   2   \nBom-ber\nFriends\n=======\n\nSelect a Gamemode\n[S] - Single Player\n[M] - 2 Player Mode\n>>>').lower().strip()
    
    grid, playerCharacter = init()
    for key, item in playerCharacter.skills.items():
        if item == True:
            skillGranted : str = key
            continue

    grid.gridBuilder(10)

    used : set[tuple[int, int]] = set()

    # random player spawnpoint
    playerCords = (randint(0, 5), randint(0, 5))
    used.add(playerCords)
    
    # random enemy spawnpoint
    enemyCords = (randint(5, 9), randint(5, 9))
    used.add(enemyCords)

    playerRow, playerCol = playerCords
    playerSpawnpoint = grid.getCell(playerRow, playerCol)
    playerSpawnpoint.propUpdate('isPlayer', True)

    enemyRow, enemyCol = enemyCords
    enemySpawnpoint = grid.getCell(enemyRow, enemyCol)
    enemySpawnpoint.propUpdate('isEnemy', True)

    # unbreakable blocks spawnpoint
    while len(used) < 15:
        uB = (randint(0, 9), randint(0, 9))
        if uB not in used:
            used.add(uB)
            rcell = grid.getCell(uB[0], uB[1])
            rcell.propUpdate('isPassable', False)
            rcell.propUpdate('isBreakable', False)

    # breakable blocks spawnpoint
    while len(used) < 25:
        b = (randint(0, 9), randint(0, 9))
        if b not in used:
            used.add(b)
            bcell = grid.getCell(b[0], b[1])
            bcell.propUpdate('isPassable', False)
            bcell.propUpdate('isBreakable', True)

    grid.show()
    
    tasks = []

    if gamemode == 'm':
        tasks = [
            asyncio.create_task(playerMovementHandling(grid, playerCords, skillGranted)), #type: ignore
            asyncio.create_task(enemyMovementHandling(grid, enemyCords))
        ]
        
    elif gamemode == 's':
        cache : list[str] = []
        tasks = [
            asyncio.create_task(playerMovementHandling(grid, playerCords, skillGranted)),#type: ignore
            asyncio.create_task(enemyAIHandling(grid, enemyCords, cache))
        ]

    while not grid.gameOver:
        await asyncio.sleep(0.1)

    for task in tasks:
        task.cancel()

    print("Exiting game...")
if __name__ == '__main__':
    asyncio.run(main())