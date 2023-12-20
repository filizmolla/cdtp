import random
from typing import Dict, List, Tuple, Callable
import turtle

class DrawPattern2dService:
    def __init__(self, pattern, master, scale):
        self._pattern = pattern
        self._master = master
        self._scale = scale
        self._turtle = turtle.Turtle()

    def _draw_rectangle(self, x, y, width, height, color):
        self._turtle.penup()
        self._turtle.goto(x * self._scale, y * self._scale)
        self._turtle.pendown()
        self._turtle.color("black", color)
        self._turtle.begin_fill()
        for _ in range(2):
            self._turtle.forward(width * self._scale)
            self._turtle.right(90)
            self._turtle.forward(height * self._scale)
            self._turtle.right(90)
        self._turtle.end_fill()

    def get_canvas(self):
        turtle.Screen().reset()  # Clear the previous screen
        self._turtle.speed(2)

        for blank in self._pattern.Blanks:
            self._draw_rectangle(blank.X, blank.Y, blank.Width, blank.Height, "green")

        for space in self._pattern.Spaces:
            self._draw_rectangle(space.X, space.Y, space.Width, space.Height, "lightblue")

        turtle.done()


class Rect:
    def __init__(self, height=0, width=0, x=0, y=0):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def rotate(self):
        self.height, self.width = self.width, self.height

    def equals(self, other):
        return (
            (self.height == other.height and self.width == other.width) or
            (self.height == other.width and self.width == other.height)
        )

    def is_exactly_equal(self, other):
        return self.x == other.x and self.y == other.y and self.equals(other)

    def rotated(self):
        return Rect(self.width, self.height, self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Rect):
            return self.equals(other)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Rect):
            return not self.equals(other)
        return NotImplemented

    def __hash__(self):
        return hash((self.height, self.width, self.x, self.y))


class RectComparer:
    def equals(self, x, y):
        return x.equals(y)

    def get_hash_code(self, obj):
        return hash((obj.height, obj.width))


class BlankEquality:
    def equals(self, other):
        raise NotImplementedError


class Pattern2d:
    def __init__(self):
        self.blanks = []
        self.spaces = []
        self.master = None

    def set_master_space(self):
        self.spaces.append(Rect(width=self.master.width, height=self.master.height, x=0, y=0))

    def get_distinct(self):
        distinct = []
        used = []
        for item in self.blanks:
            use_count = used.count(lambda x: x == item)
            if use_count == 0:
                used.append(item)
                distinct.append(item)
        return distinct

    def get_copy(self):
        new_pattern = Pattern2d()
        for blank in self.blanks:
            copy_blank = Rect(width=blank.width, height=blank.height, x=blank.x, y=blank.y)
            new_pattern.blanks.append(copy_blank)

        for space in self.spaces:
            copy_space = Rect(width=space.width, height=space.height, x=space.x, y=space.y)
            new_pattern.spaces.append(copy_space)

        new_pattern.master = self.master
        return new_pattern

    def __eq__(self, other):
        if isinstance(other, Pattern2d):
            if len(self.blanks) != len(other.blanks):
                return False
            for blank in self.blanks:
                if other.blanks.count(lambda x: x == blank and x.x == blank.x and x.y == blank.y) != 1:
                    return False
            return True
        return NotImplemented


class Solution:
    def __init__(self):
        self.pattern_demands = []

    @property
    def patterns(self):
        return [pd.pattern for pd in self.pattern_demands]

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = value

    @property
    def master_count(self):
        return sum(pd.demand for pd in self.pattern_demands)

    @property
    def pattern_count(self):
        return len(self.patterns)


class PatternDemand2d:
    def __init__(self, pattern=None, demand=0):
        self.pattern = pattern
        self.demand = demand


class BottomLeftBestFitHeuristic:
    def __init__(self, demand: Dict[Rect, int], master: Rect, sort: List[Rect] = None):
        self._demand = demand
        self._master = master
        self._sort = sort

    def process(self) -> List[PatternDemand2d]:
        self._pattern_demands = []
        added_blanks = []
        residual_demand = dict(self._demand)
        all_demand_complete = False
        new_blank = None

        while not all_demand_complete:
            ordered_sizes = self._sort(residual_demand.keys()) if self._sort else sorted(residual_demand.keys(), key=lambda x: x.Height * x.Width)
            stack = list(reversed(ordered_sizes))

            pattern = Pattern2d()
            added_blanks = []
            pattern.master = self._master
            pattern.set_master_space()
            master_is_complete = False

            while not master_is_complete:
                if not stack:
                    master_is_complete = True
                else:
                    new_blank = stack.pop()
                    temp_demand = residual_demand[new_blank]

                    if temp_demand == 0:
                        continue

                    blank_fits = True

                    while blank_fits:
                        blank_copy = Rect(new_blank)

                        if pattern.blanks:
                            self.set_spaces(pattern, self._master)

                        blank_fits = False
                        long_side = max(blank_copy.Width, blank_copy.Height)
                        short_side = min(blank_copy.Width, blank_copy.Height)

                        ordered_spaces = sorted(pattern.spaces, key=lambda x: (x.Y, x.X))

                        for space in ordered_spaces:
                            if self.fits_long_to_height(blank_copy, space, long_side, short_side):
                                blank_fits = True
                            elif self.fits_short_to_height(blank_copy, space, long_side, short_side):
                                blank_fits = True

                            if blank_fits:
                                blank_copy.X, blank_copy.Y = space.X, space.Y
                                pattern.blanks.append(blank_copy)

                                if new_blank not in added_blanks:
                                    added_blanks.append(new_blank)

                                temp_demand -= 1
                                break

                        if temp_demand == 0:
                            break

                    if master_is_complete:
                        if pattern.blanks:
                            self.set_spaces(pattern, self._master)

                        max_demand = self.max_patterns(pattern, residual_demand, added_blanks)

                        for i in added_blanks:
                            sub = max_demand * pattern.blanks.count(i)
                            residual_demand[i] -= sub

                        self._pattern_demands.append(PatternDemand2d(pattern=pattern, demand=max_demand))

                        if not any(residual_demand.values()):
                            all_demand_complete = True

        return self._pattern_demands

    def shuffle(self, pattern: Pattern2d) -> Pattern2d:
        shuffled = Pattern2d()
        shuffled.master = self._master

        rand_blanks = pattern.blanks.copy()
        fit_fns = [self.fits_long_to_height, self.fits_short_to_height]

        random.shuffle(rand_blanks)

        added = True

        for i in range(len(rand_blanks)):
            fit_fun_helper = [0, 1]
            blank = rand_blanks[i]
            long_side = max(blank.Width, blank.Height)
            short_side = min(blank.Width, blank.Height)

            if added:
                self.set_spaces(shuffled, self._master)

            added = False

            shu_spaces = random.sample(shuffled.spaces, len(shuffled.spaces))

            if not shu_spaces:
                break

            space_index = random.randint(0, len(shu_spaces) - 1)
            space = shu_spaces[space_index]
            fit_num = random.randint(0, 1)

            if fit_fns[fit_num](blank, space, long_side, short_side):
                new_blank = Rect(blank)
                new_blank.X, new_blank.Y = space.X, space.Y
                shuffled.blanks.append(new_blank)
                added = True
            else:
                fit_fun_helper.remove(fit_num)

                if fit_fns[fit_fun_helper[0]](blank, space, long_side, short_side):
                    new_blank = Rect(blank)
                    new_blank.X, new_blank.Y = space.X, space.Y
                    shuffled.blanks.append(new_blank)
                    added = True

        self.set_spaces(shuffled, self._master)
        return shuffled

    def max_patterns(self, pattern: Pattern2d, residual_demand: Dict[Rect, int], demand_reference: List[Rect]) -> int:
        max_val = float('inf')

        for item in demand_reference:
            count = pattern.blanks.count(item)
            demand = residual_demand[item]
            this_max = demand // count

            if this_max < max_val:
                max_val = this_max

        return max_val

    def fits_long_to_height(self, blank: Rect, space: Rect, long_side: float, short_side: float) -> bool:
        return long_side <= space.Height and short_side <= space.Width

    def fits_short_to_height(self, blank: Rect, space: Rect, long_side: float, short_side: float) -> bool:
        return long_side <= space.Width and short_side <= space.Height

    def fits_width_to_width(self, blank: Rect, space: Rect) -> bool:
        return blank.Width <= space.Width and blank.Height <= space.Height

    def fits_width_to_height(self, blank: Rect, space: Rect) -> bool:
        return blank.Width <= space.Height and blank.Height <= space.Width

    def set_spaces(self, pattern: Pattern2d, master: Rect) -> None:
        spaces = pattern.spaces = []
        blanks = pattern.blanks
        sorted_blanks = sorted(blanks, key=lambda x: (x.X, x.Y))

        if any(blank.Height == 1 for blank in blanks):
            pass  # Handle special case

        if not blanks:
            space = Rect()
            space.X, space.Y = 0, 0
            space.Width, space.Height = master.Width, master.Height
            spaces.append(space)

        rotate = False

        for blank in sorted_blanks:
            if blank.Height > blank.Width:
                blank.rotate()
                rotate = True

            space = Rect()
            space.X, space.Y = blank.X, blank.Y + blank.Height
            first_blank_above = self.get_first_block_going_up(blank, blanks)

            if not first_blank_above:
                space.Height = master.Height - space.Y
            else:
                space.Height = first_blank_above.Y - space.Y

            first_blank_right = self.get_first_block_going_right(space, blanks)

            if not first_blank_right:
                space.Width = master.Width - space.X
            else:
                space.Width = first_blank_right.X - space.X

            if space.Height > 0 and space.Width > 0:
                spaces.append(space)

            space = Rect()
            space.X, space.Y = blank.X + blank.Width, blank.Y
            first_blank_right = self.get_first_block_going_right(blank, blanks)

            if not first_blank_right:
                space.Width = master.Width - space.X
            else:
                space.Width = first_blank_right.X - space.X

            if space.Height > 0 and space.Width > 0:
                spaces.append(space)

            first_blank_above = self.get_first_block_going_up(space, blanks)

            if not first_blank_above:
                space.Height = master.Height - space.Y
            else:
                space.Height = first_blank_above.Y - space.Y

            if space.Height > 0 and space.Width > 0:
                spaces.append(space)

            if rotate:
                blank.rotate()

        for blank in pattern.blanks:
            if pattern.spaces.count(x for x in pattern.spaces if x.X == blank.X and x.Y == blank.Y) > 0:
                pass  # Handle duplicate cases

    def get_first_block_going_up(self, blank: Rect, blanks: List[Rect]) -> Rect:
        blocking = []

        blanks_above = [x for x in blanks if x.Y >= blank.Y + blank.Height and not blank.is_exactly_equal(x)]

        for blocker in blanks_above:
            if self.between(blank.X, blocker.X, blocker.X + blocker.Width, False):
                blocking.append(blocker)
                continue
            if self.between(blocker.X, blank.X, blank.X + blank.Width, False):
                blocking.append(blocker)
                continue
            if blank.X >= blocker.X and blocker.X + blocker.Width > blank.X:
                blocking.append(blocker)
                continue
            if blank.X == blocker.X and blocker.Width > 0:
                blocking.append(blocker)
                continue

        return min(blocking, key=lambda x: (x.Y, x.X), default=None)

    def get_first_block_going_right(self, blank: Rect, blanks: List[Rect]) -> Rect:
        blocking = []

        blanks_right = [x for x in blanks if x.X >= blank.X and not blank.is_exactly_equal(x)]

        for blocker in blanks_right:
            if self.between(blank.Y, blocker.Y, blocker.Y + blocker.Height, False):
                blocking.append(blocker)
                continue
            if self.between(blocker.Y, blank.Y, blank.Y + blank.Height, False):
                blocking.append(blocker)
                continue
            if blank.Y >= blocker.Y and blocker.Y + blocker.Height > blank.Y:
                blocking.append(blocker)
                continue
            if blank.Y == blocker.Y and blocker.Height > 0:
                blocking.append(blocker)
                continue

        return min(blocking, key=lambda x: (x.X, x.Y), default=None)

    def between(self, num: float, lower: float, upper: float, inclusive: bool = False) -> bool:
        return lower <= num <= upper if inclusive else lower < num < upper


class BestFitScrap:
    def __init__(self):
        self._algservice = BottomLeftBestFitHeuristic()
        self._patternComplete = {}
        self._patternDemands = []
        self._lastPatternAdded = None
        self._lastBlankAdded = None

    def Process(self, demand: Dict[Rect, int], sort: Callable[[List[Rect]], List[Rect]], master: Rect, rotate: Callable[[int], bool]) -> List[PatternDemand2d]:
        self._patternComplete = {}
        self._patternDemands = []
        addedBlanks = []
        residualDemand = dict(demand)
        allDemandComplete = False
        newBlank = None

        while not allDemandComplete:
            if sum(residualDemand.values()) == 0:
                break

            orderedSizes = sort([key for key, value in residualDemand.items() if value > 0])

            stack = list(reversed(orderedSizes))

            if any(pat.Pattern.Blanks.Count == 16 for pat in self._patternDemands):
                pass

            for pat in self._patternDemands:
                if pat.Pattern not in self._patternComplete:
                    pass

            patsBySumOfUsedArea = sorted(self._patternDemands, key=lambda x: sum(z.Height * z.Width for z in x.Pattern.Blanks))
            parentPatterns = [x.Pattern for x in patsBySumOfUsedArea if not self._patternComplete[x.Pattern]]

            parentPattern = parentPatterns[0] if parentPatterns else None
            isNewPattern = False

            if parentPattern is None:
                parentPattern = Pattern2d()
                parentPattern.Master = master
                parentPattern.SetMasterSpace()
                isNewPattern = True
                parentPatterns.append(parentPattern)

            newPattern = parentPattern.GetCopy()
            addedBlanks = []

            masterIsComplete = False
            blankFits = False
            tryCount = 0

            if not stack:
                masterIsComplete = True
            else:
                for p in parentPatterns:
                    for size in orderedSizes:
                        newBlank = size
                        parentPattern = p
                        newPattern = parentPattern.GetCopy()
                        blankFits = False

                        if not stack:
                            pass

                        if newBlank.Width == 48:
                            pass

                        tempDemand = residualDemand[newBlank]
                        if tempDemand == 0:
                            continue

                        blankCopy = Rect(size)
                        if rotate(tryCount):
                            blankCopy.Rotate()

                        longSide = max(blankCopy.Width, blankCopy.Height)
                        shortSide = min(blankCopy.Width, blankCopy.Height)

                        orderedSpaces = sorted(parentPattern.Spaces, key=lambda x: (x.Y, x.X))
                        for space in orderedSpaces:
                            if self._algservice.FitsWidthToWidth(blankCopy, space):
                                blankFits = True
                            elif self._algservice.FitsWidthToHeight(blankCopy, space):
                                blankCopy.Rotate()
                                blankFits = True

                            if blankFits:
                                blankCopy.X, blankCopy.Y = space.X, space.Y
                                newPattern.Blanks.append(blankCopy)
                                addedBlanks.append(newBlank)
                                tempDemand -= 1
                                break

                        if blankFits:
                            break

                if not blankFits and not isNewPattern:
                    newPattern = Pattern2d()
                    newPattern.Master = master
                    newPattern.SetMasterSpace()
                    isNewPattern = True
                    self._patternComplete[newPattern] = False
                    self.AddPatternDemand(newPattern, 1)
                    continue

                if newPattern.Blanks.count(lambda x: x.Height == 48 and x.Width == 48) == 1:
                    pass

                samePattern = next((x for x in self._patternDemands if x.Pattern == newPattern), None)
                parentPatDemand = next((x for x in self._patternDemands if x.Pattern == parentPattern), None)

                if samePattern:
                    samePattern.Demand += 1
                    residualDemand[newBlank] -= 1
                    if not isNewPattern:
                        parentPatDemand.Demand -= 1
                else:
                    if not isNewPattern:
                        parentPatDemand.Demand -= 1
                        self.AddPatternDemand(newPattern, 1)
                        residualDemand[newBlank] -= 1
                    else:
                        self.AddPatternDemand(newPattern, 1)
                        residualDemand[newBlank] -= 1

                        self._patternComplete[newPattern] = False

                if not isNewPattern and parentPatDemand.Demand == 0:
                    self.RemovePatternFromDemands(parentPattern)
                    del self._patternComplete[parentPattern]

                self._algservice.SetSpaces(parentPattern, master)
                self._algservice.SetSpaces(newPattern, master)

                completedPat = [pd.Key for pd in self._patternComplete.items() if not self.DoAnyBlanksFit(pd.Key, [x for x in residualDemand.keys() if residualDemand[x] > 0])]
                for x in completedPat:
                    self._patternComplete[x] = True

            self._algservice.SetSpaces(parentPattern, master)
            self._algservice.SetSpaces(newPattern, master)

        return self._patternDemands

    def DoAnyBlanksFit(self, pattern, blanks):
        for space in pattern.Spaces:
            for blank in blanks:
                if self._algservice.FitsWidthToHeight(blank, space):
                    return True
                if self._algservice.FitsWidthToWidth(blank, space):
                    return True
        return False

    def GetDemand(self, pattern):
        return next(x.Demand for x in self._patternDemands if x.Pattern == pattern)

    def AddPatternDemand(self, pattern, demand):
        self._patternDemands.append(PatternDemand2d(Pattern=pattern, Demand=demand))

    def SetDemand(self, pattern, demand):
        next((x.Demand for x in self._patternDemands if x.Pattern == pattern), demand)

    def RemovePatternFromDemands(self, pattern):
        self._patternDemands = [x for x in self._patternDemands if x.Pattern != pattern]


class _2dGeneticAlg:
    def __init__(self):
        self._solutions = []
        self._population = 50
        self._master = None
        self._demand = {}
        self._patternDemands = []
        self._items = []
        self._patternWeight = 0.1
        self._masterWeight = 0.9
        self._shuffleSolutionCount = 2
        self.additionalPatternSelection = 0.10
        self._chanceToShuffle = 0.1
        self.chanceToReorder = 0.1
        self._mutateCount = 0
        self._crossoverCount = 100

    def use_sample_data(self):
        self._demand = SampleData.get_sample_data_1()
        self._items = list(self._demand.keys())
        self._population = 10
        # Assuming SampleData.Master1 is already defined
        self._master = SampleData.get_master_1()

    def process(self):
        self.create_initial_solutions()
        for i in range(self._mutateCount):
            children = self.crossover()
            for solu in children:
                self.repair_solution(solu)
                self._solutions.append(solu)
                min_solu = min(self._solutions, key=lambda x: x.fitness)
                if solu.fitness > min_solu.fitness:
                    self._solutions.remove(min_solu)
                else:
                    self._solutions.remove(solu)
            self.set_fitness()
            self.mutate()
        return sorted(self._solutions, key=lambda x: x.master_count)

    def mutate(self):
        bf = BottomLeftBestFitHeuristic(self._demand, self._master, None)
        get_parent = self.get_select_parent_fn()
        parent = get_parent()
        rn = random.Random()
        length = len(parent.pattern_demands)
        index_to_shuffle = rn.randint(0, length - 1)
        patterns = parent.patterns
        pd = parent.pattern_demands[index_to_shuffle]
        pattern = patterns[index_to_shuffle]
        shuffle_ran = rn.random()

        if shuffle_ran <= self._chanceToShuffle:
            pd.pattern = bf.shuffle(pd.pattern)
            self.repair_solution(parent)
        else:
            shuffle_ran = rn.random()
            index_to_shuffle = rn.randint(0, length - 1)
            patterns = parent.patterns
            pd = parent.pattern_demands[index_to_shuffle]
            pattern = patterns[index_to_shuffle]

            if shuffle_ran <= self._chanceToShuffle:
                random.shuffle(parent.pattern_demands)
                self.repair_solution(parent)

        self.set_fitness()

    def repair_solution(self, solution):
        new_demand = dict(self._demand)
        zero_pats = 0
        remove = []
        for pd in solution.pattern_demands:
            max_val = self.max_patterns(pd.pattern, new_demand)
            if max_val <= 0:
                remove.append(pd)
            else:
                distinct = set(pd.pattern.blanks)
                for i in distinct:
                    dem_ref = next((key for key, value in new_demand.items() if key == i), None)
                    sub = max_val * pd.pattern.blanks.count(lambda x: x.width == i.width and x.height == i.height)
                    new_demand[dem_ref] -= sub

        for r in remove:
            solution.pattern_demands.remove(r)

        if sum(new_demand.values()) > 0:
            best_fit = BottomLeftBestFitHeuristic(new_demand, self._master, lambda t: sorted(t, key=lambda x: x.height * x.width))
            new_pd = best_fit.process()

            for pd in new_pd:
                solution.pattern_demands.append(pd)

    def max_patterns(self, pattern, residual_demand):
        max_val = float('inf')
        for item in pattern.blanks:
            dem_ref = next((key for key, value in residual_demand.items() if key == item), None)
            count = pattern.blanks.count(lambda x: x.width == item.width and x.height == item.height)
            demand = residual_demand[dem_ref]
            this_max = demand / count
            if this_max < max_val:
                max_val = this_max
        return max_val

    def create_initial_solutions(self):
        all_solutions = []
        sol = Solution()
        _sort = lambda t: sorted(t, key=lambda x: x.height * x.width)
        blbf = BottomLeftBestFitHeuristic(self._demand, self._master, _sort)
        sol.pattern_demands = blbf.process()
        self._solutions.append(sol)

        sol = Solution()
        _sort = lambda t: sorted(t, key=lambda x: x.height)
        blbf = BottomLeftBestFitHeuristic(self._demand, self._master, _sort)
        sol.pattern_demands = blbf.process()
        self._solutions.append(sol)

        sol = Solution()
        _sort = lambda t: sorted(t, key=lambda x: x.width)
        blbf = BottomLeftBestFitHeuristic(self._demand, self._master, _sort)
        sol.pattern_demands = blbf.process()
        self._solutions.append(sol)

        best_scrap = BestFitScrap()
        sol = Solution()
        _sort = lambda t: sorted(t, key=lambda x: x.height * x.width, reverse=True)
        sol.pattern_demands = best_scrap.process(self._demand, _sort, self._master, lambda x: True)

        self._solutions = [sol]
        return

        self.set_fitness()
        while len(self._solutions) < self._population:
            children = self.crossover()
            for solu in children:
                self.repair_solution(solu)
                self._solutions.append(solu)
            self.set_fitness()

        pds = self._solutions[0].pattern_demands
        bf = BottomLeftBestFitHeuristic(self._demand, self._master, None)
        shuf_me = pds[0]
        shuffled = bf.shuffle(shuf_me.pattern)
        shuf_me.pattern = shuffled
        self._solutions.reverse()
        shuffle_solutions = self._solutions[:self._shuffle_solution_count]

        for s in shuffle_solutions:
            for pd in s.pattern_demands:
                pd.pattern = bf.shuffle(pd.pattern)
            self.repair_solution(s)

        self.set_fitness()

    def set_fitness(self):
        self.set_master_count_fitness()
        self.set_pattern_count_fitness()

    def set_master_count_fitness(self):
        total_master = sum(x.master_count for x in self._solutions)
        denom = sum(total_master - x.master_count for x in self._solutions)
        for sol in self._solutions:
            num = total_master - sol.master_count
            fit = num / denom
            sol.fitness += fit * self._masterWeight

    def set_pattern_count_fitness(self):
        total_master = sum(x.pattern_count for x in self._solutions)
        denom = sum(total_master - x.pattern_count for x in self._solutions)
        for sol in self._solutions:
            num = total_master - sol.pattern_count
            fit = num / denom
            sol.fitness += fit * self._patternWeight

    def crossover(self):
        get_parent = self.get_select_parent_fn()
        parent1 = get_parent()
        pd1 = parent1.pattern_demands

        parent2 = get_parent()
        while parent2 == parent1:
            parent2 = get_parent()

        pd2 = parent2.pattern_demands

        new_solution1 = Solution()
        new_solution2 = Solution()

        rn = random.Random()
        num = rn.randint(1, 5)  # between 1 and 5 swaps

        lesser = min(parent1.pattern_count, parent2.pattern_count)

        all_nums = list(range(lesser))
        rn_swap_positions = random.sample(all_nums, num)

        x = 0
        for pd in parent1.pattern_demands:
            new_pd = PatternDemand2d()
            if x in rn_swap_positions:
                new_pd.demand = pd2[x].demand
                new_pd.pattern = pd2[x].pattern
            else:
                new_pd.demand = pd.demand
                new_pd.pattern = pd.pattern
            new_solution1.pattern_demands.append(new_pd)
            x += 1

        x = 0
        for pd in parent2.pattern_demands:
            new_pd = PatternDemand2d()
            if x in rn_swap_positions:
                new_pd.demand = pd1[x].demand
                new_pd.pattern = pd1[x].pattern
            else:
                new_pd.demand = pd.demand
                new_pd.pattern = pd.pattern
            new_solution2.pattern_demands.append(new_pd)
            x += 1

        return [new_solution1, new_solution2]

    def get_select_parent_fn(self):
        # get total weight
        total_fitness = sum(x.fitness for x in self._solutions)
        weights = {s: s.fitness / total_fitness for s in self._solutions}

        segments = {}
        segment_count = 0
        for solution, weight in weights.items():
            segment_count += weight
            segments[segment_count] = solution

        sorted_segments = sorted(segments.keys())
        def return_parent():
            r = random.random()
            selected_parent = None
            for seg in sorted_segments:
                if r < seg:
                    selected_parent = segments[seg]
                    break
            return selected_parent

        return return_parent

# SampleData class is not provided, so you need to define the required methods or use your actual data.
class SampleData:
    @staticmethod
    def get_sample_data_1() -> Dict[Rect, int]:
        sample = {}

        width = [27, 33, 12, 48, 54, 72, 38, 1]
        height = [27, 33, 12, 48, 40, 32, 38, 54]
        demand = [27, 33, 12, 48, 100, 150, 12, 5]

        for i in range(len(width)):
            rect = Rect()
            rect.width = width[i]
            rect.height = height[i]
            sample[rect] = demand[i]

        master = Rect()
        master.width = 96
        master.height = 48

        return sample

    @staticmethod
    def get_master_1() -> Rect:
        master = Rect()
        master.width = 96
        master.height = 48
        return master

class TestRectViewModel:
    def __init__(self):
        alg = _2dGeneticAlg()
        alg.use_sample_data()
        solutions = alg.process()
        self.solution_container_view_model = SolutionContainerViewModel()

        for solution in solutions:
            sol_vm = SolutionViewModel()
            sol_vm.pattern_count = len(solution.patterns)
            sol_vm.master_count = sum(pd.demand for pd in solution.pattern_demands)
            canvas_vms = []
            for pd in solution.pattern_demands:
                service = DrawPattern2dTurtleService(pd.pattern, solution.patterns[0].master, 5)
                canvas = service.get_canvas()
                canvas_vms.append(CanvasViewModel(canvas, pd.demand))
            sol_vm.canvas_view_models = canvas_vms
            self.solution_container_view_model.solution_view_models.append(sol_vm)

class CanvasViewModel:
    def __init__(self, canvas, count):
        self.Canvas = canvas
        self.Count = count

class SolutionViewModel:
    def __init__(self):
        self.pattern_count = 0
        self.master_count = 0
        self.canvas_view_models = []

class SolutionContainerViewModel:
    def __init__(self):
        self.solution_view_models = []

if __name__ == "__main__":
    test_view_model = TestRectViewModel()

