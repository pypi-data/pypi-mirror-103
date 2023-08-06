import processscheduler as ps

pb = ps.SchedulingProblem('ForceScheduleOptionalTasks2', horizon=14)
task_1 = ps.VariableDurationTask('task1', optional=True)
task_2 = ps.FixedDurationTask('task2', duration = 7, optional=True)
task_3 = ps.FixedDurationTask('task3', duration = 2, optional=True)
print(type(task_2.duration))
cond = ps.ForceScheduleNOptionalTasks([task_1, task_2], 1)
pb.add_constraint(cond)

solver = ps.SchedulingSolver(pb, verbosity=1)
solution = solver.solve()

print(solution)
