
import os
import csv

class Reduction:
    
    def __init__(self, filename):
        self.file = filename

    def matrix(self):
        if isinstance(self.file, str):
            with open(self.file, 'r') as f: 
                subordination_matrix = []  
                reader = csv.reader(f)
                for row in reader:
                    subordination_matrix.append(row)
            return subordination_matrix
        else:
            return self.file
        
class Input:
    
    def __init__(self, filename):
        self.file = filename
        
    def pr(self):
        with open(self.file, 'r') as f: 
            pr = []  
            reader = csv.reader(f)
            for row in reader:
                pr.append(row)
        return [x[0] for x in pr if x != []]
    
    def level(self):
        level = []
        pr = self.pr()
        for i in range(len(pr)):
            for j in range(len(list(pr[i]))):
                if list(pr[i])[j] == 'P':
                    level.append(j-1)  
        return level
    
    def notes(self):
        notes = []
        pr = self.pr()
        for i in range(len(pr)):
            for j in range(len(list(pr[i]))):
                if list(pr[i])[j] == 'P':       
                    bar = pr[i].split('P')[-1].split('-')[1]
                    event = pr[i].split('P')[-1].split('-')[-1].split('"')[0]
                    notes.append(bar+event)      
        return notes

    def tree(self):
        tree = []
        level = self.level()
        notes = self.notes()
        for x in range(max(level)+1):
            counter = 0
            pair = []
            for y in range(len(level)):
                if level[y] == x:
                    pair.append(notes[y])
                    counter +=1
                    if counter == 2:
                        counter = 0
                        tree.append(pair)
                        pair = []
            if len(pair)!= 0:
                tree.append(pair)
        return tree
            
    def sub_levels(self):
        tree = self.tree()
        subordination_levels = {}
        subordination_levels[tree[0][0]] = 0
        for x in tree[1:]:
            dominating_level = subordination_levels[x[0]]
            subordination_levels[x[1]] = dominating_level+1
        return subordination_levels