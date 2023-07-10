#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    dimensions = (num_rows,num_cols)
    return new_game_nd(dimensions, bombs)



def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    return dig_nd(game, (row,col))


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    board = game['board'][:]
    hidden = game['hidden']
    dimensions = game['dimensions']
                 
    for row in range(dimensions[0]):
        board[row]=list(map(str,board[row]))
        for col in range(dimensions[1]):
                      
            if xray:     
                if board[row][col] == '0':                    
                    board[row][col]= ' '   
    
            else:
                if hidden[row][col]:
                    board[row][col] = '_'
                elif board[row][col] == '0':                    
                    board[row][col]= ' '        
                     
    return board


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    d = render_2d_locations(game,xray) 
    dimensions = game['dimensions']
    art = str()
    for row in range(dimensions[0]): 
        art+="".join(d[row]) 
        if row!=dimensions[0]-1: 
            art+="\n"
    return art
   



# N-D IMPLEMENTATION



#HELPER FUNCTIONS
def get_coordinates(dimensions):
    """
    Returns all the coordinates in a list

    """
    coordinates = set()
    for x in range(dimensions[0]):
        if len(dimensions) == 1:
            coordinates.add((x,))
        
        else:       
            for y in get_coordinates(dimensions[1:]):
                coordinates.add((x,)+y)
    return coordinates


def find_val(board,coordinate):
    """
    returns the value in the board at a given coordinate

    """
    if coordinate == ():
        return board
    return find_val(board[coordinate[0]],coordinate[1:])


def replace(board,coordinate,value):
    """
    changes value at a specific coordinate

    """
    first = coordinate[0] 
    if len(coordinate)==1: 
        board[first] = value

    else:
        return replace(board[first],coordinate[1:],value)



def new_board(dimensions, value): #takes the dimensions and a value and returns 
#a board replacing the value in the corresponding coordinates
    board = []
    if len(dimensions)==1: 
        for i in range(dimensions[0]):        
            board.append(value)  
    else:  
        for i in range(dimensions[0]):  
            board.append(new_board(dimensions[1:],value))
    return board

def get_neighbors(dimensions, coordinate):
    """
    returns all the neighbors

    """
    for i in range(coordinate[0]-1,coordinate[0]+2):
        if i<0 or i>=dimensions[0]:
            continue
        elif len(coordinate) == 1:
            yield(i,)
        else:
            for neighbor in get_neighbors(dimensions[1:],coordinate[1:]):
                yield (i,) + neighbor
                
                
def coords(dimensions):
   """
   returns the coordinates of the board 
   
   """
   if len(dimensions) == 0:
        yield ()
        return
    
   for i in range(dimensions[0]):
        for coord in coords(dimensions[1:]):
            yield ((i,) + coord)


#Implementation 
def new_game_nd(dimensions, bombs):
    """
    Start a new game.
    

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """
    board=new_board(dimensions,0)
    hidden = new_board(dimensions,True)
    

    for bomb_coords in bombs:
            bomb_neighbors = list(get_neighbors(dimensions,bomb_coords))
            replace(board,bomb_coords,'.')
            for neighbor in bomb_neighbors:
                if neighbor in bombs:
                    continue
                else:
                    previous= find_val(board,neighbor)  
                    replace(board,neighbor,previous+1)
     

    return {
         'dimensions': dimensions,
         'board' : board,
         'hidden' : hidden,
         'state': 'ongoing'}
    


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat

    """
    
    val = find_val(game['board'], coordinates)
    #print(val)
    #print(coordinates, "coordinates")
    #print('hidden', hidden)
    
    
    if game['state'] == 'defeat' or game['state'] == 'victory':  
        return 0

    if val == '.':
        replace(game['hidden'],coordinates,False)
        game['state'] = 'defeat'
        return 1   
   
    def zero(game, coordinates):
        total = 0
        
        if find_val(game['hidden'],coordinates):
            total+=1
            return total

        replace(game['hidden'],coordinates,True)
        
        uncovered = find_val(game['board'],coordinates)
        
        if uncovered == 0:
            
            neighbors=get_neighbors(game['dimensions'],coordinates)
            
            replace(game['hidden'],coordinates,True)
            
            for i in neighbors:
                total+=zero(game, i)
                
        return total 
        
    if val == 0:
        replace(game['hidden'],coordinates,False)
        return zero(game, coordinates)
    
    elif  val>0:
        game['state'] = 'ongoing'
        return 1  
    
    return val






def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    board = game['board']
    final = new_board(game['dimensions'],'0')
    hidden = game['hidden']

    
    
    all_coordinates = get_coordinates(game['dimensions'])   
    
    for i in all_coordinates:
        value = str(find_val(board,i))
        if xray:
            if value == '0':
                replace(final,i,' ')
            else:
                replace(final,i,value)
              
        if xray is False:
           hidden_value = find_val(hidden,i)
           if hidden_value==True:
               replace(final,i,'_') 
                #print(final,i,hidden)
           elif value == '0':
                replace(final,i,' ')
           else:
                replace(final,i,value)
    return final


if __name__ == "__main__":
    pass
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    #doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
