

def offset(mr_file):

    '''
    
    This function calculates a flat list of the offsets in
    GTTM's metrical reduction of a piece of music.
    The input file should be the metrical reduction, in XML format, of a piece of music,
    following the structure defined by the Interactive GTTM Analyser (http://gttm.jp/gttm/).
    '''

    # Reading input file
     
    mpr = [line for line in open(mr_file, 'r').readlines()]

    # Reading metrical positions
    
    metric_dots = []
    for x in mpr:
        if 'P' in x and x != '<MPR>\n':
            note = x.split('=')[-1].split('/')[0]
            if '-' in note:
                metric_dots.append(note)
        elif 'metric dot' in x:
            dot = float(x.split('at=')[-1].split('>')[0].split('"')[1])
            metric_dots.append(str(dot))

    # Flattening metrical positions
    
    metric_positions = []
    for x in range(len(metric_dots)):
        if 'P' in metric_dots[x]:
            metric_positions.append(float(metric_dots[x-1]))

    return metric_positions