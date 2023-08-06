import processscheduler as ps
problem = ps.SchedulingProblem('SolvePriorities', horizon=10)
task_1 = ps.FixedDurationTask('task1', duration=2, priority=1, optional=True)
task_2 = ps.FixedDurationTask('task2', duration=2, priority=10, optional=True)
task_3 = ps.FixedDurationTask('task3', duration=2, priority=100, optional=True)

worker = ps.Worker('AWorker')
task_1.add_required_resource(worker)
task_2.add_required_resource(worker)
task_3.add_required_resource(worker)

problem.add_objective_resource_utilization(worker)
problem.add_objective_priorities()

solver = ps.SchedulingSolver(problem, verbosity=True)
#solver._solver.set(priority='pareto')
solution = solver.solve()

print(solution)
