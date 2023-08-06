import processscheduler as ps

pb = ps.SchedulingProblem('OptionalCondition2')
task_1 = ps.FixedDurationTask('task1', duration = 9)  # mandatory
task_2 = ps.FixedDurationTask('task2', duration = 4, optional=True) # optional
worker = ps.Worker('TheWorker')

cond = ps.OptionalTaskConditionSchedule(task_2, pb.horizon > 10)
pb.add_constraint(cond)

task_1.add_required_resource(worker)
task_2.add_required_resource(worker)

#pb.add_objective_makespan()
solver = ps.SchedulingSolver(pb, parallel=True, verbosity=True)
solution = solver.solve()

print(solution)
solver.export_to_smt2('ess2.smt2')
