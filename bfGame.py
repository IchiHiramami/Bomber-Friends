from typing import Any
import os
import asyncio

class Cell:
    def __init__(self, x: int, y: int):
        self.properties = {
            'x-coord' : x,
            'y-coord' : y,
            'isPlayer' : False,
            'isBreakable' : True,
            'isPassable' : True,
            'isExplosive': False,
            'isEnemy' : False
        }

    def __repr__(self):
        if self.properties['isPlayer']:
            return '[\u25db]'  
        elif self.properties['isEnemy']:
            return '[\u25bc]'  
        elif self.properties['isExplosive']:
            return '[\u25ce]'  
        elif not self.properties['isPassable'] and not self.properties['isBreakable']:
            return '[\u25a3]'  
        elif not self.properties['isPassable'] and self.properties['isBreakable']:
            return '[☒]'      
        else:
            return '[ ]'       

        
    def propUpdate(self, key : str, value : Any):
        """Update a specific property"""
        self.properties[key] = value
    
class playableCharacter:
    def __init__(self, name : str):
        self.name = name
        self.skills : dict[str, Any] ={
            'speedBoost' : False,   
            'IEDSpecialist' : False,
            'fastHand' : False
        }
    
    def propUpdate(self, key : str, value : bool):
        self.skills[key] = value

    def getProp(self, key : str) -> bool:
        return self.skills[key]

class Grid:
    """
    The `Grid` Class represents the game board, handling most game logic from cell type detection, player movement, and skill implementation.
    """
    def __init__(self):
        self.cells = []
        self.gameOver = False

    def gridBuilder(self, sideLength : int):
        """Builds the n x n board"""
        self.sideLength = sideLength
        self.cells = [[Cell(row, column) for column in range(sideLength)] for row in range(sideLength)]
            
    def getCell(self, row: int, column : int):
        """Returns the cell within the gameboard space that matches the desired coordinates"""
        return self.cells[row][column]

    def move(self, coords : tuple[int, int], actiontype : str, entity : str, spdBst : bool = False) -> tuple[int, int] | None:
        """Handles Player Movement in 4 Directons"""
        row, col = coords
        dRow, dCol = 0, 0

        match actiontype:
            case 'w' | 'up':
                dRow -= 1
            case 's' | 'down':
                dRow += 1
            case 'a' | 'left':
                dCol -= 1
            case 'd' | 'right':
                dCol += 1
            case _:
                return None

        step = 2 if spdBst else 1
        for step in range(1, step + 1):
            nRow = row + dRow * step
            nCol = col + dCol * step

            if not (0 <= nRow < self.sideLength and 0 <= nCol < self.sideLength):
                break

            targetCell = self.getCell(nRow, nCol)
            if targetCell.properties.get('isPassable', True):
                self.getCell(row, col).propUpdate(entity, False)
                targetCell.propUpdate(entity, True)

                self.show()
                return(nRow, nCol)
            

    async def bombPlace(self, coords : tuple[int, int], fastHand : bool = False ):
        row, col = coords
        if fastHand:
            IEDList : list[tuple[int,int]] = []
            for offsetRow, offsetCol in [(-1,0), (1,0), (0,1), (0,-1)]:
                if 0 <= (offsetRow + row) < self.sideLength and 0 <= (offsetCol + col) < self.sideLength:
                    nRow = row + offsetRow
                    nCol = col + offsetCol
                    offsetCell = self.getCell(nRow, nCol)

                    
                    #If passable, set bomb
                    if offsetCell.properties.get('isPassable', True) and not (offsetCell.properties.get('isPlayer', False) or offsetCell.properties.get('isEnemy', False)):
                        offsetCell.propUpdate('isExplosive', True)
                        IEDList.append((nRow, nCol))

            self.show()
            await asyncio.sleep(5)

            for r,c in IEDList:
            # 5 - Way breakability Check and Block Destruction
                for offsetRow, offsetCol in [(-1,0), (1,0), (0,1), (0,-1), (0,0)]:
                    if 0 <= (offsetRow + r) < self.sideLength and 0 <= (offsetCol + c) < self.sideLength:
                        offsetCell = self.getCell(r + offsetRow, c + offsetCol)
                        
                        #If breakable, change adjacent cell property
                        if offsetCell.properties.get('isBreakable', True):
                            offsetCell.propUpdate('isPassable', True)
                            offsetCell.propUpdate('isBreakable', False)

                            # Kills all player in the bomb radius
                            if offsetCell.properties.get('isPlayer', True):
                                offsetCell.propUpdate('isPlayer', False)
                            if offsetCell.properties.get('isEnemy', True):
                                offsetCell.propUpdate('isEnemy', False)
            return
        
    
        cell = self.getCell(row, col)
        cell.propUpdate('isExplosive', True)
        cell.propUpdate('isPassable', True)
        self.show()
        await asyncio.sleep(5)

        # 5 - Way breakability Check and Block Destruction
        for offsetRow, offsetCol in [(-1,0), (1,0), (0,1), (0,-1), (0,0)]:
            if 0 <= (offsetRow + row) < self.sideLength and 0 <= (offsetCol + col) < self.sideLength:
                offsetCell = self.getCell(row + offsetRow, col + offsetCol)
                
                #If breakable, change adjacent cell property
                if offsetCell.properties.get('isBreakable', True):
                    offsetCell.propUpdate('isPassable', True)
                    offsetCell.propUpdate('isBreakable', False)

                    # Kills all player in the bomb radius
                    if offsetCell.properties.get('isPlayer', True):
                        offsetCell.propUpdate('isPlayer', False)
                    if offsetCell.properties.get('isEnemy', True):
                        offsetCell.propUpdate('isEnemy', False)

        # Revert current bomb cell to normal cell
        cell.propUpdate('isExplosive', False)
        cell.propUpdate('isPassable', True)

        self.show()

    def show(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.targetLifeCheck()
        for row in self.cells:
            print(''.join(str(cell) for cell in row))

    def targetLifeCheck(self):
        playerFound = False
        enemyFound = False
        for _, row in enumerate(self.cells):
            for __, cell in enumerate(row):
                if cell.properties.get('isPlayer', True):
                    playerFound = True
                if cell.properties.get('isEnemy', True):
                    enemyFound = True

        if not playerFound:
            print('Game Over')
            self.gameOver = True
        if not enemyFound:
            print('Win!')
            self.gameOver = True


