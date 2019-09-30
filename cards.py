import random

class Symbol:
    def __init__( self, character, color, rotation ):
        self.character = character
        self.color = color
        self.rotation = rotation

class PlayingCard:
    def __init__( self, x1y1, x1y2, x2y1, x2y2, x3y1, x3y2 ):
        # 11 means row 1 column 1, the top left symbol
        self.symbols = {
            11 : x1y1,
            12 : x1y2,
            21 : x2y1,
            22 : x2y2,
            31 : x3y1,
            32 : x3y2
        }

pc1 = PlayingCard( 
        Symbol( 'M', "red", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '8', "black", "none"),
        Symbol( 'E', "green", "none"),
        Symbol( 'B', "green", "cw"),
        Symbol( '3', "green", "ccw")
    )
pc2 = PlayingCard( 
        Symbol( 'M', "red", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '3', "blue", "none"),
        Symbol( 'E', "blue", "none"),
        Symbol( 'B', "green", "ccw"),
        Symbol( '3', "green", "cw")
    )
pc3 = PlayingCard( 
        Symbol( 'M', "red", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '3', "blue", "none"),
        Symbol( 'E', "green", "none"),
        Symbol( 'B', "green", "ccw"),
        Symbol( '3', "green", "cw")
    )
pc4 = PlayingCard( 
        Symbol( 'M', "black", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '3', "blue", "none"),
        Symbol( 'E', "green", "none"),
        Symbol( 'B', "green", "cw"),
        Symbol( '3', "green", "ccw")
    )
pc5 = PlayingCard( 
        Symbol( 'M', "black", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '8', "black", "none"),
        Symbol( 'E', "green", "none"),
        Symbol( 'B', "green", "ccw"),
        Symbol( '3', "green", "cw")
    )
pc6 = PlayingCard( 
        Symbol( 'M', "black", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '3', "blue", "none"),
        Symbol( 'E', "red", "none"),
        Symbol( 'B', "green", "cw"),
        Symbol( '3', "green", "ccw")
    )
pc7 = PlayingCard( 
        Symbol( 'M', "red", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '3', "blue", "none"),
        Symbol( 'E', "red", "none"),
        Symbol( 'B', "green", "ccw"),
        Symbol( '3', "green", "cw")
    )
pc8 = PlayingCard( 
        Symbol( 'M', "red", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '8', "black", "none"),
        Symbol( 'E', "blue", "none"),
        Symbol( 'B', "green", "cw"),
        Symbol( '3', "green", "ccw")
    )
pc9 = PlayingCard( 
        Symbol( 'M', "red", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '8', "black", "none"),
        Symbol( 'E', "red", "none"),
        Symbol( 'B', "green", "cw"),
        Symbol( '3', "green", "ccw")
    )
pc10 = PlayingCard( 
        Symbol( 'M', "black", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '8', "black", "none"),
        Symbol( 'E', "red", "none"),
        Symbol( 'B', "green", "ccw"),
        Symbol( '3', "green", "cw")
    )
pc11 = PlayingCard( 
        Symbol( 'M', "black", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '8', "black", "none"),
        Symbol( 'E', "blue", "none"),
        Symbol( 'B', "green", "ccw"),
        Symbol( '3', "green", "cw")
    )
pc12 = PlayingCard( 
        Symbol( 'M', "black", "none"),
        Symbol( '8', "blue", "cw"),
        Symbol( '3', "blue", "none"),
        Symbol( 'E', "blue", "none"),
        Symbol( 'B', "green", "cw"),
        Symbol( '3', "green", "ccw")
    )
    
cardSet = { pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10, pc11, pc12 }

class CardGame:
    def __init__( self ):
        self.card = random.sample( cardSet )
    def query( row, column ):
        return( self.card.symbol[row*10+column] )
        
def findSymmetries( card ):
    rows = [ [11,12],[21,22],[31,32] ]
    columns = [ [11,21,31],[12,22,32] ]
    symmetries = []
    
    for row in rows:
        if( card.symbols[row[0]].color == card.symbols[row[1].color]):
            symmetries.append( "row " + rows.index(row) + " color" )
        if( card.symbols[row[0]].rotation == card.symbols[row[1].rotation]):
            symmetries.append( "row " + rows.index(row) + " rotation" )
        if( card.symbols[row[0]].character == card.symbols[row[1].character]):
            symmetries.append( "row " + rows.index(row) + " character" )
            
    for col in columns:
        if( card.symbols[col[0]].color == card.symbols[col[1]].color and card.symbols[col[1]].color == card.symbols[col[2].color]):
            symmetries.append( "column " + columns.index(col) + " color" )
        if( card.symbols[col[0]].rotation == card.symbols[col[1]].rotation and card.symbols[col[1]].rotation == card.symbols[col[2].rotation]):
            symmetries.append( "column " + columns.index(col) + " rotation" )
        if( card.symbols[col[0]].character == card.symbols[col[1].character] and card.symbols[col[1]].character == card.symbols[col[2].character]):
            symmetries.append( "column " + columns.index(col) + " character" )
            
    if( ("column 0 color" in symmetries) and ("column 1 color" in symmetries)):
        symmetries.append("all color")
    if( ("column 0 rotation" in symmetries) and ("column 1 rotation" in symmetries)):
        symmetries.append("all rotation")
    if( ("column 0 character" in symmetries) and ("column 1 character" in symmetries)):
        symmetries.append("all character")



    
    
    
    
    
    
