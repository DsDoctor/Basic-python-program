# Made by Sheng Du
# z5171466
# COMP9414 19S2

import sys
from cspProblem import Constraint, CSP
from cspConsistency import Con_solver
from searchGeneric import FrontierPQ
from display import Displayable


# a class for extending CSP
class Problem(CSP):
    def __init__(self, domains, constraints, costs, heuristic, variables=1):
        super().__init__(domains, constraints)
        self.costs = costs
        self.heuristic = heuristic
        self.num_expanded = 0
        if variables != 1:
            self.variables = variables

    def calculate_heuristic(self, meeting):
        for _ in self.domains[meeting]:
            time = _
            for _ in self.costs:
                if _.meeting[0] == meeting:
                    self.heuristic += _.costs((time,))
            return


# a class to read soft constraints and save as a function
class Costs(object):
    def __init__(self, meeting, function):
        self.meeting = meeting
        self.function = function

    def __repr__(self):
        return self.function.__name__ + str(self.meeting)

    # a function to calculate cost
    def costs(self, day_time):
        return self.function(*tuple(day_time,))


# a class for reading file and returning a meeting csp(Problem)
class FileReader(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.domains = ['mon 9am', 'mon 10am', 'mon 11am', 'mon 12pm', 'mon 1pm', 'mon 2pm', 'mon 3pm', 'mon 4pm',
                        'tue 9am', 'tue 10am', 'tue 11am', 'tue 12pm', 'tue 1pm', 'tue 2pm', 'tue 3pm', 'tue 4pm',
                        'wed 9am', 'wed 10am', 'wed 11am', 'wed 12pm', 'wed 1pm', 'wed 2pm', 'wed 3pm', 'wed 4pm',
                        'thu 9am', 'thu 10am', 'thu 11am', 'thu 12pm', 'thu 1pm', 'thu 2pm', 'thu 3pm', 'thu 4pm',
                        'fri 9am', 'fri 10am', 'fri 11am', 'fri 12pm', 'fri 1pm', 'fri 2pm', 'fri 3pm', 'fri 4pm']
        self.days = ['mon', 'tue', 'wed', 'thu', 'fri']
        self.times = ['9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm']
        self.meetings = {}
        self.constraints = []
        self.costs = []

    def read_file(self):
        # get the contents from file
        with open(self.file_name, 'r') as file:
            contents = file.read().split('\n')
        # read each line from contents
        for content in contents:
            # if line is empty goto next line
            if not content:
                continue
            # if line start from '#', goto next line
            if content[0] == '#':
                continue
            content = content.split(', ')
            # if line is a command for creating meeting
            if content[0] == 'meeting':
                # meeting name = content[-1]
                self.creat_meeting(content[-1])
            # if line is a command for creating binary constraint
            elif content[0] == 'constraint':
                # content[-1] = ['meeting1', 'constraint', 'meeting2']
                self.creat_constraint(content[-1])
            # if line is a command for creating domain
            elif content[0] == 'domain':
                # set hard domain
                if content[-1] == 'hard':
                    self.set_domain_hard(content[1:])
                # set soft domain
                elif content[-1] == 'soft':
                    self.set_domain_soft(content[1:])
        # return a Problem
        return Problem(self.meetings, self.constraints, self.costs, 0)

    # a function for creating meeting
    def creat_meeting(self, name):
        self.meetings[name] = set(self.domains)
        return

    # a function for creating binary constraint
    def creat_constraint(self, constraint):
        constraint = constraint.split(' ')
        if constraint[1] == 'before':
            self.constraints.append(Constraint((constraint[0], constraint[2]), before))
        elif constraint[1] == 'same-day':
            self.constraints.append(Constraint((constraint[0], constraint[2]), same_day))
        elif constraint[1] == 'one-day-between':
            self.constraints.append(Constraint((constraint[0], constraint[2]), one_day_between))
        elif constraint[1] == 'one-hour-between':
            self.constraints.append(Constraint((constraint[0], constraint[2]), one_hour_between))
        return

    # a function for check hard constraint(domain hard)
    def set_domain_hard(self, command):
        # get hard-domain type
        domain_type = str(command[1].split(' ')[0])
        # a empty set, saving domains
        constraint = set()
        # day or day-time range
        if domain_type in self.days:
            time_range = command[1].split(' ')
            # day-time range
            if time_range.__len__() > 1:
                if time_range.__len__() == 3:
                    start_time = time_range[0] + ' ' + time_range[1].split('-')[0]
                    end_time = time_range[1].split('-')[-1] + ' ' + time_range[-1]
                else:
                    start_time = time_range[0] + ' ' + time_range[1]
                    end_time = time_range[-2] + ' ' + time_range[-1]
                for _ in range(self.domains.index(start_time), self.domains.index(end_time) + 1):
                    constraint.add(self.domains[_])
                self.meetings[command[0]] = self.meetings[command[0]] & constraint
                return
            # day
            for _ in self.times:
                constraint.add(domain_type + ' ' + _)
            self.meetings[command[0]] = self.meetings[command[0]] & constraint
            return
        # time
        if domain_type in self.times:
            for _ in self.days:
                constraint.add(_ + ' ' + domain_type)
            self.meetings[command[0]] = self.meetings[command[0]] & constraint
            return
        if domain_type == 'morning':
            domains = {'mon 9am', 'mon 10am', 'mon 11am', 'tue 9am', 'tue 10am', 'tue 11am',
                       'wed 9am', 'wed 10am', 'wed 11am', 'thu 9am', 'thu 10am', 'thu 11am',
                       'fri 9am', 'fri 10am', 'fri 11am'}
            self.meetings[command[0]] = self.meetings[command[0]] & domains
            return
        if domain_type == 'afternoon':
            domains = {'mon 12pm', 'mon 1pm', 'mon 2pm', 'mon 3pm', 'mon 4pm',
                       'tue 12pm', 'tue 1pm', 'tue 2pm', 'tue 3pm', 'tue 4pm',
                       'wed 12pm', 'wed 1pm', 'wed 2pm', 'wed 3pm', 'wed 4pm',
                       'thu 12pm', 'thu 1pm', 'thu 2pm', 'thu 3pm', 'thu 4pm',
                       'fri 12pm', 'fri 1pm', 'fri 2pm', 'fri 3pm', 'fri 4pm'}
            self.meetings[command[0]] = self.meetings[command[0]] & domains
        if domain_type == 'before' or 'after':
            # before or after day-time
            if command[1].split(' ')[1:].__len__() == 2:
                day_time = command[1].split(' ')[1] + ' ' + command[1].split(' ')[2]
                if domain_type == 'before':
                    constraint = set(self.domains[:self.domains.index(day_time)])
                    self.meetings[command[0]] = self.meetings[command[0]] & constraint
                    return
                else:
                    constraint = set(self.domains[self.domains.index(day_time) + 1:])
                    self.meetings[command[0]] = self.meetings[command[0]] & constraint
                    return
            # day or time
            else:
                value = command[1].split(' ')[-1]
                # day
                if value in self.days:
                    if domain_type == 'before':
                        constraint = set(self.domains[:(self.days.index(value) * self.times.__len__())])
                        self.meetings[command[0]] = self.meetings[command[0]] & constraint
                        return
                    else:
                        constraint = set(self.domains[((self.days.index(value) + 1) * self.times.__len__()):])
                        self.meetings[command[0]] = self.meetings[command[0]] & constraint
                        return
                # time
                elif value in self.times:
                    if domain_type == 'before':
                        for i in range(self.times.index(value)):
                            for _ in self.days:
                                constraint.add(_ + ' ' + self.times[i])
                        self.meetings[command[0]] = self.meetings[command[0]] & constraint
                        return
                    else:
                        for i in range(self.times.index(value), self.times.__len__() - 1):
                            for _ in self.days:
                                constraint.add(_ + ' ' + self.times[i])
                        self.meetings[command[0]] = self.meetings[command[0]] & constraint
                        return

    # a function for creating soft domain
    def set_domain_soft(self, command):
        domain_type = str(command[1].split(' ')[0])
        if domain_type == 'early-week':
            self.costs.append(Costs((command[0],), early_week))
            return
        if domain_type == 'late-week':
            self.costs.append(Costs((command[0],), late_week))
            return
        if domain_type == 'early-morning':
            self.costs.append(Costs((command[0],), early_morning))
            return
        if domain_type == 'midday':
            self.costs.append(Costs((command[0],), mid_day))
            return
        if domain_type == 'late-afternoon':
            self.costs.append(Costs((command[0],), late_afternoon))
            return


# a class to check constraints and calculate heuristic
class Search_with_AC_from_Cost_CSP(Displayable):
    def __init__(self, csp):
        self.csp = Con_solver(csp)  # copy of the CSP
        self.domains = self.csp.make_arc_consistent()


# a class for searching
class AStarSearcher(object):
    def __init__(self, csp):
        self.problem = csp
        self.frontier = FrontierPQ()
        self.solution = None
        self.add_path()

    def empty_frontier(self):
        return self.frontier.__len__() == 0

    def add_path(self):
        meeting = self.problem.variables.pop()
        new_domain = self.problem.domains.copy()
        for time in self.problem.domains[meeting]:
            domain = set()
            domain.add(time)
            new_domain[meeting] = domain
            csp = Problem(new_domain, self.problem.constraints, self.problem.costs,
                          self.problem.heuristic, variables=self.problem.variables)
            csp.domains = Search_with_AC_from_Cost_CSP(csp).domains
            csp.calculate_heuristic(meeting)
            csp.num_expanded += 1
            self.frontier.add(csp, csp.heuristic)

    @staticmethod
    def get_solution(path):
        for _ in path.domains:
            print(f'{_}:{list(path.domains[_])[0]}')
        print(f'cost:{path.heuristic}')

    def search(self):
        while not self.empty_frontier():
            path = self.frontier.pop()
            self.frontier = FrontierPQ()
            if path.variables.__len__() == 0:
                self.solution = path
                break
            meeting = path.variables.pop()
            new_domain = path.domains.copy()
            for time in path.domains[meeting]:
                domain = set()
                domain.add(time)
                new_domain[meeting] = domain
                csp = Problem(new_domain, path.constraints, path.costs,
                              path.heuristic, variables=path.variables)
                csp.domains = Search_with_AC_from_Cost_CSP(csp).domains
                csp.calculate_heuristic(meeting)
                csp.num_expanded += 1
                self.frontier.add(csp, csp.heuristic)
        if not self.solution:
            print(f'No solution')
        else:
            self.get_solution(self.solution)


# functions for binary hard constraints
# before
def before(a, b):
    days = {'mon': 10, 'tue': 20, 'wed': 30, 'thu': 40, 'fri': 50}
    times = {'9am': 0, '10am': 1, '11am': 2, '12pm': 3,
             '1pm': 4, '2pm': 5, '3pm': 6, '4pm': 7}
    time_a = a.split(' ')
    time_b = b.split(' ')
    return days[time_a[0]] + times[time_a[1]] < days[time_b[0]] + times[time_b[1]]


# same-day
def same_day(a, b):
    return a[:3] == b[:3]


# one-day-between
def one_day_between(a, b):
    days = {'mon': 10, 'tue': 20, 'wed': 30, 'thu': 40, 'fri': 50}
    time_a = a.split(' ')
    time_b = b.split(' ')
    return days[time_b[0]] - days[time_a[0]] > 10


# one-hour-between
def one_hour_between(a, b):
    days = {'mon': 10, 'tue': 20, 'wed': 30, 'thu': 40, 'fri': 50}
    times = {'9am': 0, '10am': 1, '11am': 2, '12pm': 3,
             '1pm': 4, '2pm': 5, '3pm': 6, '4pm': 7}
    time_a = a.split(' ')
    time_b = b.split(' ')
    return (days[time_b[0]] + times[time_b[1]]) - (days[time_a[0]] + times[time_a[1]]) >= 2


# functions for soft constraints
# early-week
def early_week(time):
    days = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4}
    time = time.split(' ')[0]
    return days[time]


# late-week
def late_week(time):
    days = {'mon': 4, 'tue': 3, 'wed': 2, 'thu': 1, 'fri': 0}
    time = time.split(' ')[0]
    return days[time]


# early-morning
def early_morning(time):
    time = time.split(' ')[1]
    times = {'9am': 0, '10am': 1, '11am': 2, '12pm': 3,
             '1pm': 4, '2pm': 5, '3pm': 6, '4pm': 7}
    return times[time]


# midday
def mid_day(time):
    time = time.split(' ')[1]
    times = {'9am': 3, '10am': 2, '11am': 1, '12pm': 0,
             '1pm': 1, '2pm': 2, '3pm': 3, '4pm': 4}
    return times[time]


# late-afternoon
def late_afternoon(time):
    time = time.split(' ')[1]
    times = {'9am': 7, '10am': 6, '11am': 5, '12pm': 4,
             '1pm': 3, '2pm': 2, '3pm': 1, '4pm': 0}
    return times[time]


# main function
if __name__ == "__main__":
    # read the file and return a meeting csp(Problem)
    csp_meeting = FileReader('input1.txt').read_file()
    # update csp.domains
    csp_meeting.domains = Search_with_AC_from_Cost_CSP(csp_meeting).domains
    # begin search
    AStarSearcher(csp_meeting).search()
