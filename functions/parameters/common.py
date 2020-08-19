
diatonic_functions = (
    ('I', 'i'),
    ('II', 'ii'),
    ('III', 'iii'),
    ('IV', 'iv'),
    ('V', 'v'),
    ('VI', 'vi'),
    ('VII', 'vii')
)    

sharp_keys = (
    ('C','a'),
    ('G','e'),
    ('D','b'),
    ('A','f#'),
    ('E','c#'),
    ('B','g#'),
    ('F#','d#'),
    ('C#','a#'),
    ('G#','e#'),
    ('D#','b#'),
    ('A#','f##'),
    ('E#','c##')
)  

flat_keys = (
    ('C', 'a'),
    ('F', 'd'),
    ('Bb', 'g'),
    ('Eb', 'c'),
    ('Ab', 'f'),
    ('Db', 'bb'),
    ('Gb', 'eb'),
    ('Cb', 'ab'),
    ('Fb', 'db'),
    ('Bbb', 'gb'),
    ('Ebb', 'cb'),
    ('Abb', 'fb')
) 
enharmonic_keys = {
    'G#':'Ab',
    'e#':'f',
    'D#':'Eb',
    'b#':'c',
    'A#':'Bb',
    'f##':'g',
    'E#':'F',
    'c##':'d',
    'Fb':'E', 
    'db':'c#',
    'Bbb':'A', 
    'gb':'f#',
    'Ebb':'D', 
    'cb':'b',
    'Abb':'G', 
    'fb':'e'
}

sharp_functions = (
    ('I','vi'),
    ('V','iii'),
    ('II','vii'),
    ('VI','#iv'),
    ('III','#i'),
    ('VII','#v'),
    ('#IV','#ii'),
    ('#I','##vi'),
    ('#V','#iii'),
    ('#II','#vii'),
    ('#VI','##iv'),
    ('#III','##i'),
)

flat_functions = (
    ('I', 'vi'),
    ('IV', 'ii'),
    ('bVII', 'v'),
    ('bIII', 'i'),
    ('bVI', 'iv'),
    ('bII', 'bvii'),
    ('bV', 'biii'),
    ('bI', 'bvi'),
    ('bIV', 'bii'),
    ('bbVII', 'bv'),
    ('bbIII', 'bi'),
    ('bbVI', 'biv'),
) 

major_functions = ('I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii')

minor_functions = ('i', 'ii', 'III', 'iv', 'v', 'V', 'VI', 'VII')

diatonic_notes = ('c', 'd', 'e', 'f', 'g', 'a', 'b')

order_of_sharps = ('f#', 'c#', 'g#', 'd#', 'a#', 'e#', 'b#', 'f##', 'c##')

order_of_flats = ('bb', 'eb', 'ab', 'db', 'gb', 'cb', 'fb', 'bbb', 'ebb', 'abb')

enharmonics = {
    'c#':'db', 
    'd#':'eb', 
    'e#':'f', 
    'f#':'gb', 
    'g#':'ab', 
    'a#':'bb', 
    'b#':'c', 
    'c##':'d', 
    'd##':'e', 
    'e##':'f#', 
    'f##':'g', 
    'g##':'a', 
    'a##':'b', 
    'b##':'c#',
    'cb':'b', 
    'db':'c#', 
    'eb':'d#', 
    'fb':'e', 
    'gb':'f#', 
    'ab':'g#', 
    'bb':'a#',
    'cbb':'bb', 
    'dbb':'c', 
    'ebb':'d', 
    'fbb':'eb', 
    'gbb':'f', 
    'abb':'g', 
    'bbb':'a'
}

chromatic_scale = (
    ('c','b#'),
    ('c#','db'),
    ('d','d'),
    ('d#','eb'),
    ('e','fb'),
    ('f','e#'),
    ('f#','gb'),
    ('g','g'),
    ('g#','ab'),
    ('a','a'),
    ('a#','bb'),
    ('b','cb')
)