from expand import expand
  


def depth_first_search(time_map, start, end):
       
    global path
    
    explored = [start]
    fringe = expand(start,time_map)
    parents = dict()
    parents[start] = None
    
    for i in fringe:
        parents[i] = start
    
    solved = False
    goal = end
    
    while len(fringe) > 0:
        push = fringe[0]
        fringe = fringe[1:]
        if push == end:
            solved = True
            break
        else:
            if explored.count(push) == 0:
                fringe = expand(push,time_map)+ fringe 
                explored.append(push)
                for i in fringe:
                    if i not in parents:
                        parents[i] = push
                 
    path = []
    if solved == True:
        path.append(goal)       
        while parents[goal] is not None:
            path.append(parents[goal])
            goal = parents[goal]
        path.reverse()
    return path


def breadth_first_search(time_map, start, end):
    global path
    
    explored = [start]
    fringe = expand(start,time_map)
    parents = dict()
    parents[start] = None
    
    for i in fringe:
        parents[i] = start
    
    solved = False
    goal = end
    
    while len(fringe) > 0:
        push = fringe[0]
        fringe = fringe[1:]
        if push == end:
            solved = True
            break
        else:
            if explored.count(push) == 0:
                fringe = fringe + expand(push,time_map)
                explored.append(push)
                for i in fringe:
                    if i not in parents:
                        parents[i] = push
    
             
    path = []
    if solved == True:
        path.append(goal)       
        while parents[goal] is not None:
            path.append(parents[goal])
            goal = parents[goal]
        path.reverse()
    return path

      

def a_star_search(dis_map, time_map, start, end):
     
    open = [start]
    closed = []
    
    dist_from_start = {}
    dist_from_start[start] = 0
       
    heuristic = {}
    heuristic[start] = dis_map[end][start]
    
    parents = {}
    parents[start] = start
    
    pos = 1
    order = {}
    order[start] = pos
    
    def node_test(node):
        return dist_from_start[node] + heuristic[node]
    
    while len(open) > 0:
        
        node = None
        
        for i in open:
            
             if i != None and i not in order:
                 pos = pos +1
                 order[i] =pos
                 
             if node != None and node_test(i) == node_test(node):
                 if heuristic[i] < heuristic[node]:
                     node = i
                 if heuristic[i] == heuristic[node]:
                     if order[i] < order[node]:
                         node = i
            
             if node == None or node_test(i) < node_test(node):
                 node = i
             
            
        
        if node == None:
            return None
        
        if node == end:
            path = []
            while parents[node] != node:
                path.append(node)
                node = parents[node]
            path.append(start)
            path.reverse()
            return path
                
           
            
        neighbors = expand(node,time_map)
        
        for i in neighbors:
            if i not in open and i not in closed:
                open = open +[i]
                parents[i] = node
                dist_from_start[i] = dist_from_start[parents[i]] + time_map[node][i]
                heuristic[i] =dis_map[end][i]
            else:
                if i in open:
                    try:
                        if time_map[parents[node]][i] > (time_map[node][i] +time_map[parents[node]][node]) and heuristic[parents[i]] >= heuristic[node]:
                            parents[i] = node
                    except TypeError:
                        pass
                if i in closed:
                    if dist_from_start[i] > node_test(node):
                        dist_from_start[i] = node_test(node)
                        parents[i] = node
                        closed.remove(i)
                        open = open + [i]
                    
        
        open.remove(node)
        closed = closed +[node]
            
        
    print("Path Not Found")
    return None
    
    
    

