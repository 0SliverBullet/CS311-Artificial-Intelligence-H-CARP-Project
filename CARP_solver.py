import time
import numpy as np
import random
import os
import sys
from math import exp
from copy import copy, deepcopy
threshold=3000
POPSIZE=5    # the size of population
Ts=1
iter=40
cr=0.999


def floyd(graph, vertices):
    for k in range(1, vertices+1):
        for i in range(1, vertices+1):
            for j in range(1, vertices+1):
                if (graph[i][k]+graph[k][j] < graph[i][j]):
                    graph[i][j] = graph[i][k]+graph[k][j]
    #print(graph)
    return graph
   

class Solution:
    def __init__(self, route, load, cost, sum_cost):
        self.route=route
        self.load=load
        self.cost=cost
        self.sum_cost=int(sum_cost) if sum_cost != np.inf else np.inf

class EDGE:
    def __init__(self, u, v, cost, demand):
        self.u = u
        self.v = v
        self.cost = cost
        self.demand = demand

class Init:
    def __init__(self, dataPath):
        with open(dataPath, "r", encoding="utf8") as f:
            self.instance = f.readlines()
        info = self.instance[:8]
        self.NAME = info[0].split(': ')[-1].rstrip('\n')
        self.VERTICES = eval(info[1].split(': ')[-1].rstrip('\n'))
        self.DEPOT = eval(info[2].split(': ')[-1].rstrip('\n'))
        self.REQUIRED_EDGES = eval(info[3].split(': ')[-1].rstrip('\n'))
        self.NON_REQUIRED_EDGES = eval(info[4].split(': ')[-1].rstrip('\n'))
        self.VEHICLES = eval(info[5].split(': ')[-1].rstrip('\n'))
        self.CAPACITY = eval(info[6].split(': ')[-1].rstrip('\n'))
        self.TOTAL_COST_OF_REQUIRED_EDGES = eval(
            info[7].split(': ')[-1].rstrip('\n'))
        graph = self.instance[9:-1]
        self.EDGES = dict()
        self.TASKS = dict()
        map = np.full((self.VERTICES + 1, self.VERTICES + 1), np.inf)
        np.fill_diagonal(map, 0)
        for i in graph:
            s = i.split()
            u = eval(s[0])
            v = eval(s[1])
            cost = eval(s[2])
            demand = eval(s[3].rstrip('\n'))
            self.individual = EDGE(u, v, cost, demand)
            self.EDGES[(u, v)] = self.individual
            self.EDGES[(v, u)] = self.individual
            if demand != 0:
                self.TASKS[(u, v)] = self.individual
                self.TASKS[(v, u)] = self.individual
            map[u][v] = cost
            map[v][u] = cost
        self.MIN = floyd(map, self.VERTICES)


class Solver:
    def __init__(self, path, termination, seed):
        self.info = Init(path)
        self.termination = termination
        self.path = path
        self.BEST=Solution(None,None,None,np.inf)
        self.individual = []
        #random.seed(seed)
        np.random.seed(97)

    def output(self,solution): 
        out = []
        for s in solution.route:
                out.append(0)
                out.extend(s)
                out.append(0)
        ans=(",".join(str(s) for s in out)).replace(" ", "")
        print("s",ans)
        # total=0
        # for s in solution.route:
        #     for j in s:
        #          total+=self.info.TASKS[j].cost 
        #     # print(s[0][0])     
        #     total+=self.info.MIN[self.info.DEPOT][s[0][0]]
        #     total+=self.info.MIN[s[len(s)-1][1]][self.info.DEPOT]
        #     for i in range(len(s)):
        #          if i!=len(s)-1:
        #               total+=self.info.MIN[s[i][1]][s[i+1][0]]
        print("q", int(solution.sum_cost))
        # print(total)

    def solve(self):
        run_time = (time.time() - start)
        population=[]
        for i in range(1,6):
              population.append(self.initialize(i))
        id=0
        min_cost=np.inf
        cnt=0
        for i in population:
              if i.sum_cost<min_cost:
                  id=cnt
                  min_cost=i.sum_cost    
              cnt+=1
              self.individual.append(i)
        iter0 = 0
        # for _ in range(1):
        #    for i in population:
        #         self.individual.append(i)             
        self.BEST=deepcopy(self.individual[id])
        # self.SA_0()
        avg_time=0
        if self.BEST.sum_cost<threshold:
            while run_time <= self.termination-avg_time:
            #while iter<1:
                iter0 += 1
                self.SA_small(iter0)
                run_time = (time.time() - start)
                avg_time=run_time/iter0
                #print(iter0,run_time,self.BEST.sum_cost)
        else:
            while run_time <= self.termination-avg_time:
            #while iter<1:
                iter0 += 1
                self.SA_large(iter0)
                run_time = (time.time() - start)
                avg_time=run_time/iter0
                #print(iter0,run_time,self.BEST.sum_cost)              
        self.output(self.BEST)


    def initialize(self, id):
        free_list = self.info.TASKS.copy()
        route = []
        load = []
        cost = []
        while len(free_list) > 0:
            cur = self.info.DEPOT
            route.append([])
            load.append(0)
            cost.append(0)
            while len(free_list) > 0:
                next = list(free_list.values())[0]
                dis = np.inf
                for y in free_list.values():
                    if load[-1] + y.demand <= self.info.CAPACITY:
                        d = self.info.MIN[cur][y.u]
                        if d < dis:
                            dis = d
                            next = y
                        elif d == dis:
                            if id == 1 and self.info.MIN[y.v][self.info.DEPOT] > self.info.MIN[next.v][self.info.DEPOT]:
                                next = y
                            if id == 2 and self.info.MIN[y.v][self.info.DEPOT] < self.info.MIN[next.v][self.info.DEPOT]:
                                next = y
                            if id == 3 and y.demand / y.cost > next.demand / next.cost:
                                next = y
                            if id == 4 and y.demand / y.cost < next.demand / next.cost:
                                next = y
                            if id == 5:
                                if load[-1] < self.info.CAPACITY / 2:
                                    if self.info.MIN[y.v][self.info.DEPOT] > self.info.MIN[next.v][self.info.DEPOT]:
                                        next = y
                                else:
                                    if self.info.MIN[y.v][self.info.DEPOT] < self.info.MIN[next.v][self.info.DEPOT]:
                                        next = y
                if dis == np.inf:
                    break
                load[-1] += next.demand
                cost[-1] += next.cost + dis
                cur = next.v
                edge = (next.u, next.v)
                edge_inverse = (next.v, next.u)
                route[-1].append(edge)
                free_list.pop(edge)
                free_list.pop(edge_inverse)
            cost[-1] += self.info.MIN[cur][self.info.DEPOT]
        return Solution(route, load, cost, sum(cost))
    def SA_small(self,iter0):
            t=Ts
            
            while ((t>0.1 and self.termination-(time.time() - start) >1.0)  or (t<=0.1 and self.termination-(time.time() - start) < ((time.time() - start)/iter0) and  self.termination-(time.time() - start) >1.0 ) or (t<=0.1 and self.BEST.sum_cost<1000 and self.termination-(time.time() - start) < (time.time() - start) and  self.termination-(time.time() - start) >1.0 )):
                    # iteration=iter
                    t=t*cr
                    curIter=0
                    # if t>10:
                    #       iteration=iter/4*3
                    while curIter<iter:
                            curIter=curIter+1
                            p1 =np.random.randint(0, POPSIZE)
                            new=deepcopy(self.individual[p1])
                            rdft=np.random.randint(0, 7384)/ 7383.0
                            if rdft<0.3:  #flip
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                new.route[route_id][subroute_id]=(edge[1],edge[0])
                                last_end=self.info.DEPOT
                                next_begin=self.info.DEPOT
                                if subroute_id!=0:
                                    last_end=new.route[route_id][subroute_id-1][1]
                                if subroute_id!=len(new.route[route_id])-1:
                                    next_begin=new.route[route_id][subroute_id+1][0]
                                new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][edge[1]]+self.info.MIN[edge[0]][next_begin]
                            elif rdft<0.35:  #single_insertion
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                pos_rdft=np.random.randint(0, 7384)/ 7383.0
                                if pos_rdft<0.5: #the same route
                                     insert_route_id=route_id
                                     if len(new.route[insert_route_id])>1:   
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                while insert_subroute_id==subroute_id:
                                                     insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                last_end=self.info.DEPOT
                                                next_begin=self.info.DEPOT
                                                if subroute_id!=0:
                                                      last_end=new.route[route_id][subroute_id-1][1]
                                                if subroute_id!=len(new.route[route_id])-1:
                                                      next_begin=new.route[route_id][subroute_id+1][0]
                                                new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][next_begin]
                                                new.route[route_id].insert(insert_subroute_id,(edge[1],edge[0]))
                                                new.route[route_id].remove(edge)
                                                insert_subroute_id=new.route[route_id].index((edge[1],edge[0]))
                                                last_end=self.info.DEPOT
                                                next_begin=self.info.DEPOT
                                                if insert_subroute_id!=0:
                                                      last_end=new.route[route_id][insert_subroute_id-1][1]
                                                if insert_subroute_id!=len(new.route[route_id])-1:
                                                      next_begin=new.route[route_id][insert_subroute_id+1][0]
                                                new.cost[route_id]=new.cost[route_id]+self.info.MIN[last_end][edge[1]]+self.info.MIN[edge[0]][next_begin]-self.info.MIN[last_end][next_begin]
                                     else:                     
                                                curIter-=1
                                                continue
                                else: #the different route
                                    if len(new.route)>1 and len(new.route[route_id])>1:
                                        insert_route_id=np.random.randint(0, len(new.route))
                                        flag=0
                                        while flag<10 and (insert_route_id==route_id or new.load[insert_route_id]+self.info.TASKS[edge].demand>self.info.CAPACITY):
                                             flag+=1
                                             insert_route_id=np.random.randint(0, len(new.route))
                                        if flag==10:
                                            curIter-=1
                                            continue
                                        else:
                                            #print(new.load[insert_route_id])
                                            insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                            last_end=self.info.DEPOT
                                            next_begin=self.info.DEPOT
                                            if subroute_id!=0:
                                                        last_end=new.route[route_id][subroute_id-1][1]
                                            if subroute_id!=len(new.route[route_id])-1:
                                                        next_begin=new.route[route_id][subroute_id+1][0]
                                            new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][next_begin]-self.info.TASKS[edge].cost
                                            new.load[route_id]-=self.info.TASKS[edge].demand
                                            new.route[route_id].remove(edge)
                                            new.load[insert_route_id]+=self.info.TASKS[edge].demand
                                            new.route[insert_route_id].insert(insert_subroute_id,(edge))
                                            insert_subroute_id=new.route[insert_route_id].index((edge))
                                            last_end=self.info.DEPOT
                                            next_begin=self.info.DEPOT
                                            if insert_subroute_id!=0:
                                                        last_end=new.route[insert_route_id][insert_subroute_id-1][1]
                                            if insert_subroute_id!=len(new.route[insert_route_id])-1:
                                                        next_begin=new.route[insert_route_id][insert_subroute_id+1][0]
                                            new.cost[insert_route_id]=new.cost[insert_route_id]+self.info.MIN[last_end][edge[0]]+self.info.MIN[edge[1]][next_begin]-self.info.MIN[last_end][next_begin]+self.info.TASKS[edge].cost

                                    else:
                                         curIter-=1
                                         continue
                            elif rdft<0.4:  #double_insertion
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                pos_rdft=np.random.randint(0, 7384)/ 7383.0
                                if pos_rdft<0.5: #the same route
                                     insert_route_id=route_id
                                     if len(new.route[insert_route_id])>2:   
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id])-1)
                                                while insert_subroute_id==subroute_id:
                                                     insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id])-1)
                                                edge1=new.route[insert_route_id][insert_subroute_id+1]
                                                edge2=new.route[insert_route_id][insert_subroute_id]
                                                new.route[route_id].insert(subroute_id,(edge1[1],edge1[0]))
                                                new.route[route_id].insert(subroute_id+1,(edge2[1],edge2[0]))
                                                new.route[route_id].remove(edge1)
                                                new.route[route_id].remove(edge2)
                                                new.cost[route_id]=0
                                                for j in new.route[route_id]:
                                                    new.cost[route_id]+=self.info.TASKS[j].cost    
                                                new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                                new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                                for i in range(len(new.route[route_id])):
                                                    if i<len(new.route[route_id])-1:
                                                        new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]] 
                                                
                                     else:                     
                                                curIter-=1
                                                continue
                                else: #the different route
                                    if len(new.route)>1 and len(new.route[route_id])>2:
                                        subroute_id=np.random.randint(0, len(new.route[route_id])-1)
                                        edge1=new.route[route_id][subroute_id+1]
                                        edge2=new.route[route_id][subroute_id]
                                        insert_route_id=np.random.randint(0, len(new.route))
                                        flag=0
                                        while flag<10 and (insert_route_id==route_id or new.load[insert_route_id]+self.info.TASKS[edge1].demand+self.info.TASKS[edge2].demand>self.info.CAPACITY):
                                             flag+=1
                                             insert_route_id=np.random.randint(0, len(new.route))
                                        if flag==10:
                                            curIter-=1
                                            continue
                                        else:
                                            #print(new.load[insert_route_id])
                                            insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                            new.load[route_id]=new.load[route_id]-self.info.TASKS[edge1].demand-self.info.TASKS[edge2].demand
                                            new.route[route_id].remove(edge1)
                                            new.route[route_id].remove(edge2)
                                            for j in new.route[route_id]:
                                                    new.cost[route_id]+=self.info.TASKS[j].cost    
                                            new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                            new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                            for i in range(len(new.route[route_id])):
                                                    if i<len(new.route[route_id])-1:
                                                        new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]] 

                                            new.load[insert_route_id]=new.load[insert_route_id]+self.info.TASKS[edge].demand+self.info.TASKS[edge2].demand
                                            new.route[insert_route_id].insert(insert_subroute_id,(edge1[1],edge1[0]))
                                            new.route[insert_route_id].insert(insert_subroute_id+1,(edge2[1],edge2[0]))
                                            for j in new.route[insert_route_id]:
                                                    new.cost[insert_route_id]+=self.info.TASKS[j].cost    
                                            new.cost[insert_route_id]+=self.info.MIN[self.info.DEPOT][new.route[insert_route_id][0][0]]
                                            new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][len(new.route[insert_route_id])-1][1]][self.info.DEPOT]
                                            for i in range(len(new.route[insert_route_id])):
                                                    if i<len(new.route[insert_route_id])-1:
                                                        new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][i][1]][new.route[insert_route_id][i+1][0]] 
                                    else:
                                         curIter-=1
                                         continue
                            elif rdft<0.8:  #2-opt
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                pos_rdft=np.random.randint(0, 7384)/ 7383.0
                                if pos_rdft<0.5: #the same route
                                     insert_route_id=route_id
                                     if len(new.route[insert_route_id])>1:   
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                while insert_subroute_id==subroute_id:
                                                     insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                if insert_subroute_id<subroute_id:
                                                      temp=subroute_id
                                                      subroute_id=insert_subroute_id
                                                      insert_subroute_id=temp
                                                
                                                # swap_edge=new.route[insert_route_id][insert_subroute_id]
                                                reverse=[]
                                                i=subroute_id+1
                                                while i<=insert_subroute_id-1:
                                                      trace=new.route[route_id][i]
                                                      reverse.append((trace[1],trace[0]))
                                                      i=i+1
                                                i=subroute_id+1
                                                while i<=insert_subroute_id-1:
                                                      new.route[route_id][i]=reverse[(insert_subroute_id-1)-i]
                                                      i=i+1
                                                new.cost[route_id]=0
                                                for j in new.route[route_id]:
                                                    new.cost[route_id]+=self.info.TASKS[j].cost    
                                                new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                                new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                                for i in range(len(new.route[route_id])):
                                                    if i<len(new.route[route_id])-1:
                                                        new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]] 
                                                                                         
                                              
                                     else:                     
                                                curIter-=1
                                                continue
                                else: #the different route
                                    plan_rdft=np.random.randint(0, 7384)/ 7383.0
                                    if plan_rdft<1:
                                            if len(new.route)>1:
                                                insert_route_id=np.random.randint(0, len(new.route))
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                swap_edge=new.route[insert_route_id][insert_subroute_id]
                                                flag=0
                                                load1=0
                                                load2=0
                                                while flag<20 and (insert_route_id==route_id or load1 > self.info.CAPACITY or load2 >self.info.CAPACITY or load1==0 or load2==0):
                                                    flag+=1
                                                    insert_route_id=np.random.randint(0, len(new.route))
                                                    insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                    i=0
                                                    load1=0
                                                    load2=0
                                                    while i <= subroute_id:
                                                        load1+=self.info.TASKS[new.route[route_id][i]].demand
                                                        i+=1
                                                    j=insert_subroute_id+1
                                                    while j <= len(new.route[insert_route_id])-1:
                                                        load1+=self.info.TASKS[new.route[insert_route_id][j]].demand
                                                        j+=1
                                                    i=0
                                                    while i <= insert_subroute_id:
                                                        load2+=self.info.TASKS[new.route[insert_route_id][i]].demand
                                                        i+=1    
                                                    j=subroute_id+1
                                                    while j <= len(new.route[route_id])-1:
                                                        load2+=self.info.TASKS[new.route[route_id][j]].demand   
                                                        j+=1
                                                if flag==20:
                                                    curIter-=1
                                                    continue
                                                else:
                                                    trace1=[]
                                                    trace2=[]
                                                    new.load[route_id]=load1
                                                    new.load[insert_route_id]=load2
                                                    i=0
                                                    while i <= subroute_id:
                                                        trace1.append(new.route[route_id][i])
                                                        i+=1
                                                    j=insert_subroute_id+1
                                                    while j <= len(new.route[insert_route_id])-1:
                                                        trace1.append(new.route[insert_route_id][j])
                                                        j+=1
                                                    i=0
                                                    while i <= insert_subroute_id:
                                                        trace2.append(new.route[insert_route_id][i])
                                                        i+=1    
                                                    j=subroute_id+1
                                                    while j <= len(new.route[route_id])-1:
                                                        trace2.append(new.route[route_id][j])   
                                                        j+=1                           
                                                    new.route[route_id]=trace1.copy()
                                                    new.route[insert_route_id]=trace2.copy()
                                                    new.cost[route_id]=0
                                                    for j in new.route[route_id]:
                                                            new.cost[route_id]+=self.info.TASKS[j].cost    
                                                    new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                                    new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                                    for i in range(len(new.route[route_id])):
                                                            if i<len(new.route[route_id])-1:
                                                                new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]]
                                                    new.cost[insert_route_id]=0
                                                    for j in new.route[insert_route_id]:
                                                            new.cost[insert_route_id]+=self.info.TASKS[j].cost    
                                                    new.cost[insert_route_id]+=self.info.MIN[self.info.DEPOT][new.route[insert_route_id][0][0]]
                                                    new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][len(new.route[insert_route_id])-1][1]][self.info.DEPOT]
                                                    for i in range(len(new.route[insert_route_id])):
                                                            if i<len(new.route[insert_route_id])-1:
                                                                new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][i][1]][new.route[insert_route_id][i+1][0]]                                              

                                            else:
                                                curIter-=1
                                                continue      
                                    else:
                                            if len(new.route)>1:
                                                insert_route_id=np.random.randint(0, len(new.route))
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                swap_edge=new.route[insert_route_id][insert_subroute_id]
                                                flag=0
                                                load1=0
                                                load2=0
                                                while flag<20 and (insert_route_id==route_id or load1 > self.info.CAPACITY or load2 >self.info.CAPACITY or load1==0 or load2==0):
                                                    flag+=1
                                                    insert_route_id=np.random.randint(0, len(new.route))
                                                    insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                    i=0
                                                    load1=0
                                                    load2=0
                                                    while i <= subroute_id:
                                                        load1+=self.info.TASKS[new.route[route_id][i]].demand
                                                        i+=1
                                                    j=insert_subroute_id
                                                    while j >= 0:
                                                        load1+=self.info.TASKS[new.route[insert_route_id][j]].demand
                                                        j-=1
                                                    i=len(new.route[insert_route_id])-1
                                                    while i >= insert_subroute_id+1:
                                                        load2+=self.info.TASKS[new.route[insert_route_id][i]].demand
                                                        i-=1    
                                                    j=subroute_id+1
                                                    while j <= len(new.route[route_id])-1:
                                                        load2+=self.info.TASKS[new.route[route_id][j]].demand   
                                                        j+=1
                                                if flag==20:
                                                    curIter-=1
                                                    continue
                                                else:
                                                    trace1=[]
                                                    trace2=[]
                                                    new.load[route_id]=load1
                                                    new.load[insert_route_id]=load2
                                                    i=0
                                                    while i <= subroute_id:
                                                        trace1.append(new.route[route_id][i])
                                                        i+=1
                                                    j=insert_subroute_id
                                                    while j >=0:
                                                        trace1.append(new.route[insert_route_id][j])
                                                        j-=1
                                                    i=len(new.route[insert_route_id])-1
                                                    while i >= insert_subroute_id+1:
                                                        trace2.append(new.route[insert_route_id][i])
                                                        i-=1    
                                                    j=subroute_id+1
                                                    while j <= len(new.route[route_id])-1:
                                                        trace2.append(new.route[route_id][j])   
                                                        j+=1                           
                                                    new.route[route_id]=trace1.copy()
                                                    new.route[insert_route_id]=trace2.copy()
                                                    new.cost[route_id]=0
                                                    for j in new.route[route_id]:
                                                            new.cost[route_id]+=self.info.TASKS[j].cost    
                                                    new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                                    new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                                    for i in range(len(new.route[route_id])):
                                                            if i<len(new.route[route_id])-1:
                                                                new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]]
                                                    new.cost[insert_route_id]=0
                                                    for j in new.route[insert_route_id]:
                                                            new.cost[insert_route_id]+=self.info.TASKS[j].cost    
                                                    new.cost[insert_route_id]+=self.info.MIN[self.info.DEPOT][new.route[insert_route_id][0][0]]
                                                    new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][len(new.route[insert_route_id])-1][1]][self.info.DEPOT]
                                                    for i in range(len(new.route[insert_route_id])):
                                                            if i<len(new.route[insert_route_id])-1:
                                                                new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][i][1]][new.route[insert_route_id][i+1][0]]                                              

                                            else:
                                                curIter-=1
                                                continue      
                                                  
                            else:   
                                    #swap
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                pos_rdft=np.random.randint(0, 7384)/ 7383.0
                                if pos_rdft<0.5: #the same route
                                     insert_route_id=route_id
                                     if len(new.route[insert_route_id])>1:   
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                while insert_subroute_id==subroute_id:
                                                     insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                swap_edge=new.route[insert_route_id][insert_subroute_id]
                                                last_end=self.info.DEPOT
                                                next_begin=self.info.DEPOT
                                                if subroute_id!=0:
                                                      last_end=new.route[route_id][subroute_id-1][1]
                                                if subroute_id!=len(new.route[route_id])-1:
                                                      next_begin=new.route[route_id][subroute_id+1][0]
                                                new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][swap_edge[0]]+self.info.MIN[swap_edge[1]][next_begin]
                                                new.route[route_id][subroute_id]=swap_edge
                                                new.route[insert_route_id][insert_subroute_id]=edge
                                                last_end=self.info.DEPOT
                                                next_begin=self.info.DEPOT
                                                if insert_subroute_id!=0:
                                                      last_end=new.route[route_id][insert_subroute_id-1][1]
                                                if insert_subroute_id!=len(new.route[route_id])-1:
                                                      next_begin=new.route[route_id][insert_subroute_id+1][0]
                                                new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][swap_edge[0]]-self.info.MIN[swap_edge[1]][next_begin]+self.info.MIN[last_end][edge[0]]+self.info.MIN[edge[1]][next_begin]
                                     else:                     
                                                curIter-=1
                                                continue
                                else: #the different route
                                    #b=0
                                    if len(new.route)>1:
                                        insert_route_id=np.random.randint(0, len(new.route))
                                        insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                        swap_edge=new.route[insert_route_id][insert_subroute_id]
                                        flag=0
                                        while flag<20 and (insert_route_id==route_id or new.load[insert_route_id]-self.info.TASKS[swap_edge].demand+self.info.TASKS[edge].demand>self.info.CAPACITY or new.load[route_id]-self.info.TASKS[edge].demand+self.info.TASKS[swap_edge].demand>self.info.CAPACITY):
                                             flag+=1
                                             insert_route_id=np.random.randint(0, len(new.route))
                                             insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                             swap_edge=new.route[insert_route_id][insert_subroute_id]
                                        if flag==20:
                                            curIter-=1
                                            continue
                                        else:
                                            last_end=self.info.DEPOT
                                            next_begin=self.info.DEPOT
                                            if subroute_id!=0:
                                                        last_end=new.route[route_id][subroute_id-1][1]
                                            if subroute_id!=len(new.route[route_id])-1:
                                                        next_begin=new.route[route_id][subroute_id+1][0]
                                            new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][swap_edge[0]]+self.info.MIN[swap_edge[1]][next_begin]-self.info.TASKS[edge].cost+self.info.TASKS[swap_edge].cost
                                            new.load[route_id]=new.load[route_id]-self.info.TASKS[edge].demand+self.info.TASKS[swap_edge].demand
                                            new.route[route_id][subroute_id]=swap_edge
                                            last_end=self.info.DEPOT
                                            next_begin=self.info.DEPOT
                                            if insert_subroute_id!=0:
                                                        last_end=new.route[insert_route_id][insert_subroute_id-1][1]
                                            if insert_subroute_id!=len(new.route[insert_route_id])-1:
                                                        next_begin=new.route[insert_route_id][insert_subroute_id+1][0]
                                            new.cost[insert_route_id]=new.cost[insert_route_id]-self.info.MIN[last_end][swap_edge[0]]-self.info.MIN[swap_edge[1]][next_begin]+self.info.MIN[last_end][edge[0]]+self.info.MIN[edge[1]][next_begin]-self.info.TASKS[swap_edge].cost+self.info.TASKS[edge].cost
                                            new.load[insert_route_id]=new.load[insert_route_id]-self.info.TASKS[swap_edge].demand+self.info.TASKS[edge].demand
                                            new.route[insert_route_id][insert_subroute_id]=edge           
                                            

                                    else:
                                         curIter-=1
                                         continue                                

                            new.sum_cost=int(sum(new.cost))  #computeObjective
               
                            if (new.sum_cost < self.individual[p1].sum_cost):
                                self.individual[p1]=deepcopy(new)
                            else:
                                rdft=np.random.randint(0, 7384)/ 7383.0

                                if (rdft<exp(-(new.sum_cost - self.individual[p1].sum_cost)/t)):
                                    self.individual[p1]=deepcopy(new)
                            if (self.individual[p1].sum_cost < self.BEST.sum_cost):
                                    self.BEST=deepcopy(self.individual[p1])

    def SA_large(self,iter0):
            t=Ts*100
            while ((t>0.1 and self.termination-(time.time() - start) >1.0)  or (t<=0.1 and self.termination-(time.time() - start) < ((time.time() - start)/iter0) and  self.termination-(time.time() - start) >1.0 ) ):
                    # iteration=iter
                    t=t*cr
                    curIter=0
                    # if t>10:
                    #       iteration=iter/4*3
                    while curIter<iter/2:
                            curIter=curIter+1
                            p1 =np.random.randint(0, POPSIZE)
                            new=deepcopy(self.individual[p1])
                            rdft=np.random.randint(0, 7384)/ 7383.0
                            if rdft<0.3:  #flip
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                new.route[route_id][subroute_id]=(edge[1],edge[0])
                                last_end=self.info.DEPOT
                                next_begin=self.info.DEPOT
                                if subroute_id!=0:
                                    last_end=new.route[route_id][subroute_id-1][1]
                                if subroute_id!=len(new.route[route_id])-1:
                                    next_begin=new.route[route_id][subroute_id+1][0]
                                new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][edge[1]]+self.info.MIN[edge[0]][next_begin]
                            elif rdft<0.35:  #single_insertion
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                pos_rdft=np.random.randint(0, 7384)/ 7383.0
                                if pos_rdft<0.5: #the same route
                                     insert_route_id=route_id
                                     if len(new.route[insert_route_id])>1:   
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                while insert_subroute_id==subroute_id:
                                                     insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                last_end=self.info.DEPOT
                                                next_begin=self.info.DEPOT
                                                if subroute_id!=0:
                                                      last_end=new.route[route_id][subroute_id-1][1]
                                                if subroute_id!=len(new.route[route_id])-1:
                                                      next_begin=new.route[route_id][subroute_id+1][0]
                                                new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][next_begin]
                                                new.route[route_id].insert(insert_subroute_id,(edge[1],edge[0]))
                                                new.route[route_id].remove(edge)
                                                insert_subroute_id=new.route[route_id].index((edge[1],edge[0]))
                                                last_end=self.info.DEPOT
                                                next_begin=self.info.DEPOT
                                                if insert_subroute_id!=0:
                                                      last_end=new.route[route_id][insert_subroute_id-1][1]
                                                if insert_subroute_id!=len(new.route[route_id])-1:
                                                      next_begin=new.route[route_id][insert_subroute_id+1][0]
                                                new.cost[route_id]=new.cost[route_id]+self.info.MIN[last_end][edge[1]]+self.info.MIN[edge[0]][next_begin]-self.info.MIN[last_end][next_begin]
                                     else:                     
                                                curIter-=1
                                                continue
                                else: #the different route
                                    if len(new.route)>1 and len(new.route[route_id])>1:
                                        insert_route_id=np.random.randint(0, len(new.route))
                                        flag=0
                                        while flag<10 and (insert_route_id==route_id or new.load[insert_route_id]+self.info.TASKS[edge].demand>self.info.CAPACITY):
                                             flag+=1
                                             insert_route_id=np.random.randint(0, len(new.route))
                                        if flag==10:
                                            curIter-=1
                                            continue
                                        else:
                                            #print(new.load[insert_route_id])
                                            insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                            last_end=self.info.DEPOT
                                            next_begin=self.info.DEPOT
                                            if subroute_id!=0:
                                                        last_end=new.route[route_id][subroute_id-1][1]
                                            if subroute_id!=len(new.route[route_id])-1:
                                                        next_begin=new.route[route_id][subroute_id+1][0]
                                            new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][next_begin]-self.info.TASKS[edge].cost
                                            new.load[route_id]-=self.info.TASKS[edge].demand
                                            new.route[route_id].remove(edge)
                                            new.load[insert_route_id]+=self.info.TASKS[edge].demand
                                            new.route[insert_route_id].insert(insert_subroute_id,(edge))
                                            insert_subroute_id=new.route[insert_route_id].index((edge))
                                            last_end=self.info.DEPOT
                                            next_begin=self.info.DEPOT
                                            if insert_subroute_id!=0:
                                                        last_end=new.route[insert_route_id][insert_subroute_id-1][1]
                                            if insert_subroute_id!=len(new.route[insert_route_id])-1:
                                                        next_begin=new.route[insert_route_id][insert_subroute_id+1][0]
                                            new.cost[insert_route_id]=new.cost[insert_route_id]+self.info.MIN[last_end][edge[0]]+self.info.MIN[edge[1]][next_begin]-self.info.MIN[last_end][next_begin]+self.info.TASKS[edge].cost

                                    else:
                                         curIter-=1
                                         continue
                            elif rdft<0.4:  #double_insertion
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                pos_rdft=np.random.randint(0, 7384)/ 7383.0
                                if pos_rdft<0.5: #the same route
                                     insert_route_id=route_id
                                     if len(new.route[insert_route_id])>2:   
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id])-1)
                                                while insert_subroute_id==subroute_id:
                                                     insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id])-1)
                                                edge1=new.route[insert_route_id][insert_subroute_id+1]
                                                edge2=new.route[insert_route_id][insert_subroute_id]
                                                new.route[route_id].insert(subroute_id,(edge1[1],edge1[0]))
                                                new.route[route_id].insert(subroute_id+1,(edge2[1],edge2[0]))
                                                new.route[route_id].remove(edge1)
                                                new.route[route_id].remove(edge2)
                                                new.cost[route_id]=0
                                                for j in new.route[route_id]:
                                                    new.cost[route_id]+=self.info.TASKS[j].cost    
                                                new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                                new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                                for i in range(len(new.route[route_id])):
                                                    if i<len(new.route[route_id])-1:
                                                        new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]] 
                                                
                                     else:                     
                                                curIter-=1
                                                continue
                                else: #the different route
                                    if len(new.route)>1 and len(new.route[route_id])>2:
                                        subroute_id=np.random.randint(0, len(new.route[route_id])-1)
                                        edge1=new.route[route_id][subroute_id+1]
                                        edge2=new.route[route_id][subroute_id]
                                        insert_route_id=np.random.randint(0, len(new.route))
                                        flag=0
                                        while flag<10 and (insert_route_id==route_id or new.load[insert_route_id]+self.info.TASKS[edge1].demand+self.info.TASKS[edge2].demand>self.info.CAPACITY):
                                             flag+=1
                                             insert_route_id=np.random.randint(0, len(new.route))
                                        if flag==10:
                                            curIter-=1
                                            continue
                                        else:
                                            #print(new.load[insert_route_id])
                                            insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                            new.load[route_id]=new.load[route_id]-self.info.TASKS[edge1].demand-self.info.TASKS[edge2].demand
                                            new.route[route_id].remove(edge1)
                                            new.route[route_id].remove(edge2)
                                            for j in new.route[route_id]:
                                                    new.cost[route_id]+=self.info.TASKS[j].cost    
                                            new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                            new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                            for i in range(len(new.route[route_id])):
                                                    if i<len(new.route[route_id])-1:
                                                        new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]] 

                                            new.load[insert_route_id]=new.load[insert_route_id]+self.info.TASKS[edge].demand+self.info.TASKS[edge2].demand
                                            new.route[insert_route_id].insert(insert_subroute_id,(edge1[1],edge1[0]))
                                            new.route[insert_route_id].insert(insert_subroute_id+1,(edge2[1],edge2[0]))
                                            for j in new.route[insert_route_id]:
                                                    new.cost[insert_route_id]+=self.info.TASKS[j].cost    
                                            new.cost[insert_route_id]+=self.info.MIN[self.info.DEPOT][new.route[insert_route_id][0][0]]
                                            new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][len(new.route[insert_route_id])-1][1]][self.info.DEPOT]
                                            for i in range(len(new.route[insert_route_id])):
                                                    if i<len(new.route[insert_route_id])-1:
                                                        new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][i][1]][new.route[insert_route_id][i+1][0]] 
                                    else:
                                         curIter-=1
                                         continue
                            elif rdft<0.8:  #2-opt
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                pos_rdft=np.random.randint(0, 7384)/ 7383.0
                                if pos_rdft<0.5: #the same route
                                     insert_route_id=route_id
                                     if len(new.route[insert_route_id])>1:   
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                while insert_subroute_id==subroute_id:
                                                     insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                if insert_subroute_id<subroute_id:
                                                      temp=subroute_id
                                                      subroute_id=insert_subroute_id
                                                      insert_subroute_id=temp
                                                
                                                # swap_edge=new.route[insert_route_id][insert_subroute_id]
                                                reverse=[]
                                                i=subroute_id+1
                                                while i<=insert_subroute_id-1:
                                                      trace=new.route[route_id][i]
                                                      reverse.append((trace[1],trace[0]))
                                                      i=i+1
                                                i=subroute_id+1
                                                while i<=insert_subroute_id-1:
                                                      new.route[route_id][i]=reverse[(insert_subroute_id-1)-i]
                                                      i=i+1
                                                new.cost[route_id]=0
                                                for j in new.route[route_id]:
                                                    new.cost[route_id]+=self.info.TASKS[j].cost    
                                                new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                                new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                                for i in range(len(new.route[route_id])):
                                                    if i<len(new.route[route_id])-1:
                                                        new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]] 
                                                                                         
                                              
                                     else:                     
                                                curIter-=1
                                                continue
                                else: #the different route
                                    plan_rdft=np.random.randint(0, 7384)/ 7383.0
                                    if plan_rdft<1:
                                            if len(new.route)>1:
                                                insert_route_id=np.random.randint(0, len(new.route))
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                swap_edge=new.route[insert_route_id][insert_subroute_id]
                                                flag=0
                                                load1=0
                                                load2=0
                                                while flag<20 and (insert_route_id==route_id or load1 > self.info.CAPACITY or load2 >self.info.CAPACITY or load1==0 or load2==0):
                                                    flag+=1
                                                    insert_route_id=np.random.randint(0, len(new.route))
                                                    insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                    i=0
                                                    load1=0
                                                    load2=0
                                                    while i <= subroute_id:
                                                        load1+=self.info.TASKS[new.route[route_id][i]].demand
                                                        i+=1
                                                    j=insert_subroute_id+1
                                                    while j <= len(new.route[insert_route_id])-1:
                                                        load1+=self.info.TASKS[new.route[insert_route_id][j]].demand
                                                        j+=1
                                                    i=0
                                                    while i <= insert_subroute_id:
                                                        load2+=self.info.TASKS[new.route[insert_route_id][i]].demand
                                                        i+=1    
                                                    j=subroute_id+1
                                                    while j <= len(new.route[route_id])-1:
                                                        load2+=self.info.TASKS[new.route[route_id][j]].demand   
                                                        j+=1
                                                if flag==20:
                                                    curIter-=1
                                                    continue
                                                else:
                                                    trace1=[]
                                                    trace2=[]
                                                    new.load[route_id]=load1
                                                    new.load[insert_route_id]=load2
                                                    i=0
                                                    while i <= subroute_id:
                                                        trace1.append(new.route[route_id][i])
                                                        i+=1
                                                    j=insert_subroute_id+1
                                                    while j <= len(new.route[insert_route_id])-1:
                                                        trace1.append(new.route[insert_route_id][j])
                                                        j+=1
                                                    i=0
                                                    while i <= insert_subroute_id:
                                                        trace2.append(new.route[insert_route_id][i])
                                                        i+=1    
                                                    j=subroute_id+1
                                                    while j <= len(new.route[route_id])-1:
                                                        trace2.append(new.route[route_id][j])   
                                                        j+=1                           
                                                    new.route[route_id]=trace1.copy()
                                                    new.route[insert_route_id]=trace2.copy()
                                                    new.cost[route_id]=0
                                                    for j in new.route[route_id]:
                                                            new.cost[route_id]+=self.info.TASKS[j].cost    
                                                    new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                                    new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                                    for i in range(len(new.route[route_id])):
                                                            if i<len(new.route[route_id])-1:
                                                                new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]]
                                                    new.cost[insert_route_id]=0
                                                    for j in new.route[insert_route_id]:
                                                            new.cost[insert_route_id]+=self.info.TASKS[j].cost    
                                                    new.cost[insert_route_id]+=self.info.MIN[self.info.DEPOT][new.route[insert_route_id][0][0]]
                                                    new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][len(new.route[insert_route_id])-1][1]][self.info.DEPOT]
                                                    for i in range(len(new.route[insert_route_id])):
                                                            if i<len(new.route[insert_route_id])-1:
                                                                new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][i][1]][new.route[insert_route_id][i+1][0]]                                              

                                            else:
                                                curIter-=1
                                                continue      
                                    else:
                                            if len(new.route)>1:
                                                insert_route_id=np.random.randint(0, len(new.route))
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                swap_edge=new.route[insert_route_id][insert_subroute_id]
                                                flag=0
                                                load1=0
                                                load2=0
                                                while flag<20 and (insert_route_id==route_id or load1 > self.info.CAPACITY or load2 >self.info.CAPACITY or load1==0 or load2==0):
                                                    flag+=1
                                                    insert_route_id=np.random.randint(0, len(new.route))
                                                    insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                    i=0
                                                    load1=0
                                                    load2=0
                                                    while i <= subroute_id:
                                                        load1+=self.info.TASKS[new.route[route_id][i]].demand
                                                        i+=1
                                                    j=insert_subroute_id
                                                    while j >= 0:
                                                        load1+=self.info.TASKS[new.route[insert_route_id][j]].demand
                                                        j-=1
                                                    i=len(new.route[insert_route_id])-1
                                                    while i >= insert_subroute_id+1:
                                                        load2+=self.info.TASKS[new.route[insert_route_id][i]].demand
                                                        i-=1    
                                                    j=subroute_id+1
                                                    while j <= len(new.route[route_id])-1:
                                                        load2+=self.info.TASKS[new.route[route_id][j]].demand   
                                                        j+=1
                                                if flag==20:
                                                    curIter-=1
                                                    continue
                                                else:
                                                    trace1=[]
                                                    trace2=[]
                                                    new.load[route_id]=load1
                                                    new.load[insert_route_id]=load2
                                                    i=0
                                                    while i <= subroute_id:
                                                        trace1.append(new.route[route_id][i])
                                                        i+=1
                                                    j=insert_subroute_id
                                                    while j >=0:
                                                        trace1.append(new.route[insert_route_id][j])
                                                        j-=1
                                                    i=len(new.route[insert_route_id])-1
                                                    while i >= insert_subroute_id+1:
                                                        trace2.append(new.route[insert_route_id][i])
                                                        i-=1    
                                                    j=subroute_id+1
                                                    while j <= len(new.route[route_id])-1:
                                                        trace2.append(new.route[route_id][j])   
                                                        j+=1                           
                                                    new.route[route_id]=trace1.copy()
                                                    new.route[insert_route_id]=trace2.copy()
                                                    new.cost[route_id]=0
                                                    for j in new.route[route_id]:
                                                            new.cost[route_id]+=self.info.TASKS[j].cost    
                                                    new.cost[route_id]+=self.info.MIN[self.info.DEPOT][new.route[route_id][0][0]]
                                                    new.cost[route_id]+=self.info.MIN[new.route[route_id][len(new.route[route_id])-1][1]][self.info.DEPOT]
                                                    for i in range(len(new.route[route_id])):
                                                            if i<len(new.route[route_id])-1:
                                                                new.cost[route_id]+=self.info.MIN[new.route[route_id][i][1]][new.route[route_id][i+1][0]]
                                                    new.cost[insert_route_id]=0
                                                    for j in new.route[insert_route_id]:
                                                            new.cost[insert_route_id]+=self.info.TASKS[j].cost    
                                                    new.cost[insert_route_id]+=self.info.MIN[self.info.DEPOT][new.route[insert_route_id][0][0]]
                                                    new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][len(new.route[insert_route_id])-1][1]][self.info.DEPOT]
                                                    for i in range(len(new.route[insert_route_id])):
                                                            if i<len(new.route[insert_route_id])-1:
                                                                new.cost[insert_route_id]+=self.info.MIN[new.route[insert_route_id][i][1]][new.route[insert_route_id][i+1][0]]                                              

                                            else:
                                                curIter-=1
                                                continue      
                                                  
                            else:   
                                    #swap
                                route_id=np.random.randint(0, len(new.route))
                                subroute_id=np.random.randint(0, len(new.route[route_id]))
                                edge=new.route[route_id][subroute_id]
                                pos_rdft=np.random.randint(0, 7384)/ 7383.0
                                if pos_rdft<0.5: #the same route
                                     insert_route_id=route_id
                                     if len(new.route[insert_route_id])>1:   
                                                insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                while insert_subroute_id==subroute_id:
                                                     insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                                swap_edge=new.route[insert_route_id][insert_subroute_id]
                                                last_end=self.info.DEPOT
                                                next_begin=self.info.DEPOT
                                                if subroute_id!=0:
                                                      last_end=new.route[route_id][subroute_id-1][1]
                                                if subroute_id!=len(new.route[route_id])-1:
                                                      next_begin=new.route[route_id][subroute_id+1][0]
                                                new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][swap_edge[0]]+self.info.MIN[swap_edge[1]][next_begin]
                                                new.route[route_id][subroute_id]=swap_edge
                                                new.route[insert_route_id][insert_subroute_id]=edge
                                                last_end=self.info.DEPOT
                                                next_begin=self.info.DEPOT
                                                if insert_subroute_id!=0:
                                                      last_end=new.route[route_id][insert_subroute_id-1][1]
                                                if insert_subroute_id!=len(new.route[route_id])-1:
                                                      next_begin=new.route[route_id][insert_subroute_id+1][0]
                                                new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][swap_edge[0]]-self.info.MIN[swap_edge[1]][next_begin]+self.info.MIN[last_end][edge[0]]+self.info.MIN[edge[1]][next_begin]
                                     else:                     
                                                curIter-=1
                                                continue
                                else: #the different route
                                    #b=0
                                    if len(new.route)>1:
                                        insert_route_id=np.random.randint(0, len(new.route))
                                        insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                        swap_edge=new.route[insert_route_id][insert_subroute_id]
                                        flag=0
                                        while flag<20 and (insert_route_id==route_id or new.load[insert_route_id]-self.info.TASKS[swap_edge].demand+self.info.TASKS[edge].demand>self.info.CAPACITY or new.load[route_id]-self.info.TASKS[edge].demand+self.info.TASKS[swap_edge].demand>self.info.CAPACITY):
                                             flag+=1
                                             insert_route_id=np.random.randint(0, len(new.route))
                                             insert_subroute_id=np.random.randint(0, len(new.route[insert_route_id]))
                                             swap_edge=new.route[insert_route_id][insert_subroute_id]
                                        if flag==20:
                                            curIter-=1
                                            continue
                                        else:
                                            last_end=self.info.DEPOT
                                            next_begin=self.info.DEPOT
                                            if subroute_id!=0:
                                                        last_end=new.route[route_id][subroute_id-1][1]
                                            if subroute_id!=len(new.route[route_id])-1:
                                                        next_begin=new.route[route_id][subroute_id+1][0]
                                            new.cost[route_id]=new.cost[route_id]-self.info.MIN[last_end][edge[0]]-self.info.MIN[edge[1]][next_begin]+self.info.MIN[last_end][swap_edge[0]]+self.info.MIN[swap_edge[1]][next_begin]-self.info.TASKS[edge].cost+self.info.TASKS[swap_edge].cost
                                            new.load[route_id]=new.load[route_id]-self.info.TASKS[edge].demand+self.info.TASKS[swap_edge].demand
                                            new.route[route_id][subroute_id]=swap_edge
                                            last_end=self.info.DEPOT
                                            next_begin=self.info.DEPOT
                                            if insert_subroute_id!=0:
                                                        last_end=new.route[insert_route_id][insert_subroute_id-1][1]
                                            if insert_subroute_id!=len(new.route[insert_route_id])-1:
                                                        next_begin=new.route[insert_route_id][insert_subroute_id+1][0]
                                            new.cost[insert_route_id]=new.cost[insert_route_id]-self.info.MIN[last_end][swap_edge[0]]-self.info.MIN[swap_edge[1]][next_begin]+self.info.MIN[last_end][edge[0]]+self.info.MIN[edge[1]][next_begin]-self.info.TASKS[swap_edge].cost+self.info.TASKS[edge].cost
                                            new.load[insert_route_id]=new.load[insert_route_id]-self.info.TASKS[swap_edge].demand+self.info.TASKS[edge].demand
                                            new.route[insert_route_id][insert_subroute_id]=edge           
                                            

                                    else:
                                         curIter-=1
                                         continue                                

                            new.sum_cost=int(sum(new.cost))  #computeObjective
               
                            if (new.sum_cost < self.individual[p1].sum_cost):
                                self.individual[p1]=deepcopy(new)
                            else:
                                rdft=np.random.randint(0, 7384)/ 7383.0

                                if (rdft<exp(-(new.sum_cost - self.individual[p1].sum_cost)/t)):
                                    self.individual[p1]=deepcopy(new)
                            if (self.individual[p1].sum_cost < self.BEST.sum_cost):
                                    self.BEST=deepcopy(self.individual[p1])



if __name__ == '__main__':
    start = time.time()
    solver = Solver(sys.argv[1], int(sys.argv[3]), int(sys.argv[5]))
    solver.solve()
# python CARP_solver.py D:\SUSTech\Sophomore\大二（下）\专业课\CS303\Project\Project2\CARP_samples\\sample.dat -t 10 -s 1
# python CARP_solver.py D:\SUSTech\Sophomore\大二（下）\专业课\CS303\Project\Project2\CARP_samples\\gdb10.dat -t 60 -s 1
# python CARP_solver.py D:\SUSTech\Sophomore\大二（下）\专业课\CS303\Project\Project2\CARP_samples\\gdb1.dat -t 60 -s 1
# python CARP_solver.py D:\SUSTech\Sophomore\大二（下）\专业课\CS303\Project\Project2\CARP_samples\\egl-s1-A.dat -t 60 -s 1
# python CARP_solver.py D:\SUSTech\Sophomore\大二（下）\专业课\CS303\Project\Project2\CARP_samples\\egl-e1-A.dat -t 60 -s 1
# python CARP_solver.py D:\SUSTech\Sophomore\大二（下）\专业课\CS303\Project\Project2\CARP_samples\\val1A.dat -t 60 -s 1
# python CARP_solver.py D:\SUSTech\Sophomore\大二（下）\专业课\CS303\Project\Project2\CARP_samples\\val4A.dat -t 40 -s 1
# python CARP_solver.py D:\SUSTech\Sophomore\大二（下）\专业课\CS303\Project\Project2\CARP_samples\\val7A.dat -t 60 -s 1
