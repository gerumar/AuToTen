

from functions.classes.matrix import Input

def generator(pr_file):
        
    '''
    
    This function calculates a representation, in the form of a matrix,
    of GTTM's prolongational reduction of a piece of music.
    The input file should be the prolongational reduction, in XML format, of a piece of music,
    following the structure defined by the Interactive GTTM Analyser (http://gttm.jp/gttm/).
    '''
    
    # Reading input data
    
    tree = Input(pr_file).tree()
    notes = Input(pr_file).notes()
    subordination_levels = Input(pr_file).sub_levels()
    
    note_positions = [int(x) for x in notes]
    sorted_positions = []
    for x in note_positions:
        if x not in sorted_positions:
            sorted_positions.append(x)
    sorted_positions = sorted(sorted_positions)
    tree[0].append(tree[0][0])
    
    # Creating the prolongational matrix
    
    matrix = []
    for i in range(len(tree)):
        row = []
        for j in range(len(tree)):
            if [str(sorted_positions[j]), str(sorted_positions[i])] in tree:
                row.append(subordination_levels[str(sorted_positions[i])])
            else:
                row.append('')
        matrix.append(row)
    
    return matrix

