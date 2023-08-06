#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.display import JSON
import processscheduler as ps
import math
import random as rand
import json
from itertools import permutations
import pandas as pd
pd.options.mode.chained_assignment = None


# In[2]:


PROBLEM_HORIZON = 65
problem = ps.SchedulingProblem('Example', horizon=PROBLEM_HORIZON)

# In[3]:


# Initialize resource and constraints
constraints = []
Resource = ps.Worker('resource')


# In[4]:


# People dict already generated for example purposes
people = {'person_0': {'id': 'person_0',
                       'num_tasks_dur1': 0,
                       'num_tasks_dur2': 1,
                       'num_tasks_dur1_scheduled': 0,
                       'num_tasks_dur2_scheduled': 1,
                       'availability': [(0, 2), (13, 15), (52, 54)]},
          'person_1': {'id': 'person_1',
                       'num_tasks_dur1': 1,
                       'num_tasks_dur2': 2,
                       'num_tasks_dur1_scheduled': 1,
                       'num_tasks_dur2_scheduled': 2,
                       'availability': [(8, 13), (21, 26), (33, 39), (46, 47), (49, 52), (59, 65)]},
          'person_2': {'id': 'person_2',
                       'num_tasks_dur1': 0,
                       'num_tasks_dur2': 5,
                       'num_tasks_dur1_scheduled': 0,
                       'num_tasks_dur2_scheduled': 4,
                       'availability': [(2, 5), (15, 18), (28, 31), (41, 44), (54, 57)]},
          'person_3': {'id': 'person_3',
                       'num_tasks_dur1': 3,
                       'num_tasks_dur2': 1,
                       'num_tasks_dur1_scheduled': 3,
                       'num_tasks_dur2_scheduled': 0,
                       'availability': [(25, 26), (51, 52), (64, 65)]},
          'person_4': {'id': 'person_4',
                       'num_tasks_dur1': 2,
                       'num_tasks_dur2': 2,
                       'num_tasks_dur1_scheduled': 2,
                       'num_tasks_dur2_scheduled': 1,
                       'availability': [(6, 7), (19, 20), (32, 33), (45, 46), (51, 52), (62, 65)]},
          'person_5': {'id': 'person_5',
                       'num_tasks_dur1': 0,
                       'num_tasks_dur2': 5,
                       'num_tasks_dur1_scheduled': 0,
                       'num_tasks_dur2_scheduled': 1,
                       'availability': [(0, 2), (62, 65)]},
          'person_6': {'id': 'person_6',
                       'num_tasks_dur1': 3,
                       'num_tasks_dur2': 1,
                       'num_tasks_dur1_scheduled': 1,
                       'num_tasks_dur2_scheduled': 0,
                       'availability': [(10, 13), (23, 26), (36, 39), (62, 65)]},
          'person_7': {'id': 'person_7',
                       'num_tasks_dur1': 5,
                       'num_tasks_dur2': 2,
                       'num_tasks_dur1_scheduled': 3,
                       'num_tasks_dur2_scheduled': 0,
                       'availability': [(0, 1),
                                        (7, 8),
                                        (20, 21),
                                        (26, 27),
                                        (33, 34),
                                        (46, 47),
                                        (52, 53),
                                        (59, 60)]},
          'person_8': {'id': 'person_8',
                       'num_tasks_dur1': 0,
                       'num_tasks_dur2': 3,
                       'num_tasks_dur1_scheduled': 0,
                       'num_tasks_dur2_scheduled': 2,
                       'availability': [(9, 13), (22, 26), (35, 39), (48, 52), (61, 65)]},
          'person_9': {'id': 'person_9',
                       'num_tasks_dur1': 1,
                       'num_tasks_dur2': 1,
                       'num_tasks_dur1_scheduled': 1,
                       'num_tasks_dur2_scheduled': 1,
                       'availability': [(2, 7),
                                        (11, 13),
                                        (15, 20),
                                        (24, 26),
                                        (28, 33),
                                        (37, 39),
                                        (41, 46),
                                        (50, 52),
                                        (54, 59),
                                        (63, 65)]},
          'person_10': {'id': 'person_10',
                        'num_tasks_dur1': 0,
                        'num_tasks_dur2': 3,
                        'num_tasks_dur1_scheduled': 0,
                        'num_tasks_dur2_scheduled': 2,
                        'availability': [(8, 10), (22, 24), (34, 36), (48, 50), (57, 61)]},
          'person_11': {'id': 'person_11',
                        'num_tasks_dur1': 0,
                        'num_tasks_dur2': 3,
                        'num_tasks_dur1_scheduled': 0,
                        'num_tasks_dur2_scheduled': 2,
                        'availability': [(7, 9), (33, 35), (59, 61)]},
          'person_12': {'id': 'person_12',
                        'num_tasks_dur1': 2,
                        'num_tasks_dur2': 3,
                        'num_tasks_dur1_scheduled': 2,
                        'num_tasks_dur2_scheduled': 3,
                        'availability': [(2, 5),
                                         (11, 13),
                                         (15, 18),
                                         (24, 26),
                                         (28, 31),
                                         (37, 39),
                                         (41, 44),
                                         (50, 52),
                                         (54, 57),
                                         (63, 65)]},
          'person_13': {'id': 'person_13',
                        'num_tasks_dur1': 1,
                        'num_tasks_dur2': 2,
                        'num_tasks_dur1_scheduled': 1,
                        'num_tasks_dur2_scheduled': 0,
                        'availability': [(23, 24), (49, 50), (62, 63)]},
          'person_14': {'id': 'person_14',
                        'num_tasks_dur1': 0,
                        'num_tasks_dur2': 2,
                        'num_tasks_dur1_scheduled': 0,
                        'num_tasks_dur2_scheduled': 2,
                        'availability': [(52, 55), (56, 63)]},
          'person_15': {'id': 'person_15',
                        'num_tasks_dur1': 0,
                        'num_tasks_dur2': 0,
                        'num_tasks_dur1_scheduled': 0,
                        'num_tasks_dur2_scheduled': 0,
                        'availability': [(2, 7),
                                         (9, 13),
                                         (15, 20),
                                         (22, 26),
                                         (28, 33),
                                         (35, 39),
                                         (41, 46),
                                         (48, 52),
                                         (54, 59),
                                         (61, 65)]},
          'person_16': {'id': 'person_16',
                        'num_tasks_dur1': 2,
                        'num_tasks_dur2': 2,
                        'num_tasks_dur1_scheduled': 2,
                        'num_tasks_dur2_scheduled': 2,
                        'availability': [(18, 26), (31, 39), (44, 52)]}
           }


# # Format of people

# In[5]:


JSON(people)


# In[6]:


# Create people tasks, assigning resource and adding their constraints
people_tasks_dur1 = []
people_tasks_dur2 = []

for person_id in people:
    person_tasks_dur1 = []
    person_tasks_dur2 = []

    num_tasks_dur1 = people[person_id]['num_tasks_dur1']
    num_tasks_dur2 = people[person_id]['num_tasks_dur2']
    availability = people[person_id]['availability']
    task_num = 0

    # duration 2 tasks
    for i in range(num_tasks_dur2):
        task_num += 1

        # add task
        person_tasks_dur2.append(ps.FixedDurationTask(
            f'{person_id}__{task_num:02d}', duration=2, optional=True))
        person_tasks_dur2[-1].add_required_resource(Resource)

        # add constraints associated to task
        all_ctr = []
        for j in availability:
            ctr1 = ps.TaskStartAfterLax(
                person_tasks_dur2[-1], j[0], optional=True)
            ctr2 = ps.TaskEndBeforeLax(
                person_tasks_dur2[-1], j[1], optional=True)

            all_ctr.append(ctr1)
            all_ctr.append(ctr2)

            constraints.append(ps.and_([ctr1, ctr2]))
            # force both ctr1 and ctr2 to be applied or not applied simultaneously
            constraints.append(ctr1.applied == ctr2.applied)

        constraints.append(ps.ForceApplyNOptionalConstraints(
            all_ctr, 2))  # force 2 optional constraints to True

    # duration 1 tasks
    for i in range(num_tasks_dur1):
        task_num += 1

        # add task
        person_tasks_dur1.append(ps.FixedDurationTask(
            f'{person_id}__{task_num:02d}', duration=1, optional=True))
        person_tasks_dur1[-1].add_required_resource(Resource)

        # add constraints associated to task
        all_ctr = []
        for j in availability:
            ctr1 = ps.TaskStartAfterLax(
                person_tasks_dur1[-1], j[0], optional=True)
            ctr2 = ps.TaskEndBeforeLax(
                person_tasks_dur1[-1], j[1], optional=True)

            all_ctr.append(ctr1)
            all_ctr.append(ctr2)

            constraints.append(ps.and_([ctr1, ctr2]))
            # force both ctr1 and ctr2 to be applied or not applied simultaneously
            constraints.append(ctr1.applied == ctr2.applied)

        constraints.append(ps.ForceApplyNOptionalConstraints(
            all_ctr, 2))  # force 2 optional constraints to True

    person_tasks = person_tasks_dur1 + person_tasks_dur2

    # schedule at least 1 task of each person (only if they asked for any)
    if len(person_tasks) >= 1:
        constraints.append(ps.ForceScheduleNOptionalTasks(
            person_tasks, 1, kind='atleast'))

# # Allowing a max of n tasks from a list to be sheduled between timepoint i and j
#     for t1,t2 in permutations(person_tasks,2):
#         constraints.append(ps.if_then_else(t1.start/13 < 1,[ps.TaskStartAfterLax(t2,13)],
#             [ps.if_then_else(t1.start/13 < 2,[ps.TaskStartAfterLax(t2,13*2)],
#                 [ps.if_then_else(t1.start/13 < 3,[ps.TaskStartAfterLax(t2,13*3)],
#                     [ps.implies(t1.start/13 < 4,[ps.TaskStartAfterLax(t2,13*4)])
#                 ])
#             ])
#         ]))

#     people_tasks_dur1 += person_tasks_dur1
#     people_tasks_dur2 += person_tasks_dur2

# # Forcing resource maximization
# constraints.append(ps.ForceScheduleNOptionalTasks(people_tasks_dur2,20,kind='atleast'))
# constraints.append(ps.ForceScheduleNOptionalTasks(people_tasks_dur1,12,kind='atleast'))


# In[7]:


tasks_total = 0
tasks_dur1 = 0
tasks_dur2 = 0
for student in people:
    num_tasks_dur1 = people[student]['num_tasks_dur1']
    num_tasks_dur2 = people[student]['num_tasks_dur2']
    tasks_total += num_tasks_dur1 + 2*num_tasks_dur2
    tasks_dur1 += num_tasks_dur1
    tasks_dur2 += num_tasks_dur2

print(f'Ordered dur1 tasks: {tasks_dur1}\nOrdered dur2 tasks: {tasks_dur2}')
print(f'Ordered slots: {tasks_total}\nAvailable slots: {PROBLEM_HORIZON}')


# In[ ]:
from z3 import *
# problem.add_objective_priorities()
utilization_ind = problem.add_indicator_resource_utilization(Resource)
constraints.append(utilization_ind.indicator_variable <= 100)
constraints.append(utilization_ind.indicator_variable >= 95)
problem.add_constraints(constraints)

solver = ps.SchedulingSolver(problem, verbosity=False, max_time=30, parallel=False)
#smt_solver = solver._solver
solution = False
solution = solver.solve()
import time

# set_option("sat.restart.max", 10)
# from multiprocessing.pool import ThreadPool
# from copy import deepcopy

# pool = ThreadPool(8)
# def cube_and_conquer(s):
#     print("In cube and conquer")
#     for cube in s.cube():
#        if len(cube) == 0:
#           return unknown
#        if is_true(cube[0]):
#           return sat
#        is_sat = s.check(cube)
#        print("Cube is sat")
#        if is_sat == unknown:
#           print("Cube is unknwon")
#           s1 = s.translate(s.ctx)
#           s1.add(cube)
#           # Kick off parallel computation
#           pool.apply_async(cube_and_conquer, [s1])#calculate, [x_i, i, i_context])
          
#           #is_sat = cube_and_conquer(s1)
#        if is_sat != unsat:
#           print("Cube is unsat")
#           return is_sat
#     return unsat
# init_time = time.time()
# sol = cube_and_conquer(smt_solver)

# pool.close()
# pool.join()
# print(time.time()-init_time)
# print(sol)
solution.render_gantt_matplotlib(fig_size=(200, 3), render_mode='Resource')


# In[10]:


solution_dict = json.loads(solution.to_json_string())
JSON(solution_dict)


# # Final notes
# - I have deleted for the sake of this example all data preprocessing that translates real-life times into problem time-points. Therefore, there's a people dictionary already filled out with needed information
# 
# - Allowing a max of n tasks from a list to be sheduled between timepoint i and j is something I don't know how to implement. You can see I tried something in cell 6 but with no success.
# 
# - An interesting feature would be multiobjective optimizated solutions (for instance: priority + utilization)

# In[ ]:



