import itertools
import math

#from a list of teams, this functions checks if there is any overlap of members among the teams
def overlap(division):
    for i in range(len(division)):
        for x in division[i].get_names():
            for j in range (len(division)):
                if j == i:
                    continue

                if division[j].is_name_there(x):
                    return True
    return False

#this class takes in a text file and extracts the swimmer information from it
class InputProcessor:
    def __init__(self, file_path):
        self.file = open(file_path, "r")
        self.timings = self.get_timings()
        self.swimmers = self.get_swimmers()

    def get_seconds(self, ms):
        if ms == "inf":
            return float("inf")
        split = ms.split(":")
        return int(split[0]) * 60 + float(split[1])

    def get_timings(self):
        dummy_timings = []

        for x in self.file:
            dummy_timings.append(x.strip().split(", "))

        for i in range(len(dummy_timings)):
            for j in range(len(dummy_timings[i])):
                if dummy_timings[i][j].isalpha() and dummy_timings[i][j] != "inf":
                    continue

                dummy_timings[i][j] = self.get_seconds(dummy_timings[i][j])
        return dummy_timings

    def get_swimmers(self):
        dummy_swimmers = []

        for x in self.timings:
            dummy_swimmers.append(Swimmer(x[0], x[1], x[2], x[3], x[4]))
        return dummy_swimmers

    def get_batches(self):
        batches = list(itertools.combinations(self.swimmers, 4))
        best_batches = []

        count = 0
        for x in batches:
            permutations = []
            for perm in itertools.permutations(x):
                permutations.append(Team(perm))

            best_score = float("inf")

            for y in permutations:
                if y.total_timing < best_score:
                    best = y
                    best_score = y.total_timing
            best_batches.append(best)

        best_batches.sort()
        return best_batches


#class representing a swimmer
class Swimmer:
    def __init__(self, name, backcrawl, breaststroke, butterfly, crawl):
        self.name = name
        self.backcrawl = backcrawl
        self.breaststroke = breaststroke
        self.butterfly = butterfly
        self.crawl = crawl

    def print_timings(self):
        print("\n" + self.name + ":\n")
        print("\tBackcrawl: " + str(self.backcrawl) + "\n")
        print("\tBreasktroke: " + str(self.breaststroke) + "\n")
        print("\tButterfly: " + str(self.butterfly) + "\n")
        print("\tCrawl: " + str(self.crawl) + "\n")

    def __eq__(self, other):
        return self.name == other.name

    
#class representing a team of 4 swimmers
class Team:
    def __init__(self, swimmers):
        self.backcrawl_swimmer = swimmers[0]
        self.breaststroke_swimmer = swimmers[1]
        self.butterfly_swimmer = swimmers[2]
        self.crawl_swimmer = swimmers[3]

        self.total_timing = self.backcrawl_swimmer.backcrawl + self.breaststroke_swimmer.breaststroke + self.butterfly_swimmer.butterfly + self.crawl_swimmer.crawl

    def print_team(self):
        print("\nBackcrawl: " + self.backcrawl_swimmer.name + " - " + str(self.backcrawl_swimmer.backcrawl))
        print("Breaststroke: " + self.breaststroke_swimmer.name + " - " + str(self.breaststroke_swimmer.breaststroke))
        print("Butterfly: " + self.butterfly_swimmer.name + " - " + str(self.butterfly_swimmer.butterfly))
        print("Crawl: " + self.crawl_swimmer.name + " - " + str(self.crawl_swimmer.crawl))
        print("Total timing: " + str(self.total_timing))

    def get_names(self):
        return [self.backcrawl_swimmer.name, self.breaststroke_swimmer.name, self.butterfly_swimmer.name, self.crawl_swimmer.name]
    def is_name_there(self, name):
        if self.get_names().count(name) > 0:
            return True
        return False

    def __gt__(self, other):
        return self.total_timing > other.total_timing

    def __lt__(self, other):
        return self.total_timing < other.total_timing

#a class representing 3 teams which form a division
class Division:
    def __init__(self, batches):
        self.batches = batches
        self.mean = self.get_mean()
        self.stddev = self.get_stddev()

    def get_mean(self):
        mean = 0
        for x in self.batches:
            mean += x.total_timing
        return mean / len(self.batches)
        
    def get_stddev(self):
        stddev = 0
        for x in self.batches:
            stddev += (x.total_timing - self.mean) ** 2

        return (stddev / len(self.batches)) ** 0.5

def main():
    file_processor = InputProcessor("medley_timings.txt")

    timings = []
    swimmers = file_processor.swimmers.copy()

    print("Created swimmer list")

    #batches = list(itertools.combinations(swimmers, 4))
    best_batches = file_processor.get_batches()
    print("batch list length is " + str(len(best_batches)))
    slice_percentage = 0.49

    no_of_teams = int(len(swimmers) / 4)

    while slice_percentage >= 0:
        slice_batches = best_batches[math.floor(len(best_batches) * slice_percentage):math.floor((len(best_batches) - 1) * (1-slice_percentage))]
        print(len(slice_batches))
        divisions = list(itertools.combinations(slice_batches, no_of_teams))
        print("Number of unoptimised divisions: " + str(len(divisions)))
        input()

        index = 0
        while index < len(divisions):
            print("Index is now " + str(index) + " and length is now " + str(len(divisions)))
            if overlap(divisions[index]):
                divisions.pop(index)
                continue
            index += 1

        if len(divisions) == 0:
            slice_percentage -= 0.01
        else:
            for i in range(len(divisions)):
                divisions[i] = Division(divisions[i])

        min_std = float("inf")
        for x in divisions:
            if x.stddev < min_std:
                min_std = x.stddev
                best_division = x
            elif x.stddev == min_std and x.mean < best_division.mean:
                best_division = x

        answer = input("The smallest standard deviation of a division found between the " + str(slice_percentage) + " + and " + str(1 - slice_percentage) + " percentile is " + str(min_std) + ". Is this ok? (y/n) ")
        if answer == 'y':
            break
        else:
            slice_percentage -= 0.01

    for x in best_division.batches:
        x.print_team()

main()