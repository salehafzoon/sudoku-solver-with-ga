import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from random import randint

sudoku=[
8,0,0,0,0,0,0,0,0,
0,0,3,6,0,0,0,0,0,
0,7,0,0,9,0,2,0,0,
0,5,0,0,0,7,0,0,0,
0,0,0,0,4,5,7,0,0,
0,0,0,1,0,0,0,3,0,
0,0,1,0,0,0,0,6,8,
0,0,8,5,0,0,0,1,0,
0,9,0,0,0,0,4,0,0]

start = time.time()
generation = 1
found = False
population = []
best_fits = []
avg_fits = []

POPULATION_SIZE = 1
TOURNAMENT_SIZE = 3
MUTATION_RATE = 0.1
CROSSOVER_RATE =0.5
ELITSM = 0.8
MAX_GENERATION = 50000

def countDuplicateElement(array):
    duplication = 0
    seen = []
    for element in array:
        if element in seen:
            duplication +=1
        else:
            seen.append(element)
    
    return duplication
    

class Individual(object):

    def __init__(self, chromosome):
        self.standardFormat = None
        self.chromosome = chromosome
        self.fitness = self.call_fitness()
        
    @classmethod
    def convertToBlockFormat(self,puzzle):
        blocks = []
        #divide puzzle to 3 rows consist of 
        # 3 blocks horizontally.
        #iterate over rows
        for i in range(0,9,3):
            #each horizontal row contains 3 normal rows
            rowList = []
            rowList.append(puzzle[ i*9 : (i+1)*9 ])
            rowList.append(puzzle[ (i+1)*9 : (i+2)*9 ])
            rowList.append(puzzle[ (i+2)*9 : (i+3)*9 ])
            
            for j in range(0,9,3):
                block = []
                for row in rowList:
                    block += row[j:j+3]
                blocks.append(block)

        return blocks

    @classmethod
    def setOriginalPuzzle(self,puzzle):
        self.original_puzzle = Individual.convertToBlockFormat(puzzle)
        print(self.original_puzzle)

    @classmethod
    def create_chromosome(self):
        if self.original_puzzle ==None:
            print("original puzzle didn't set.")
            return
        else:
            chromosome = []
            for x in self.original_puzzle :
                y = x if x!=0 else randint(1, 9)
                chromosome.append(y)
            
            return chromosome
    
    def mutate(self):

        #select one of puzzle subgrid randomly(first index of subgrid)
        sub_grid_index = random.choice(list([x*9 for x in range(9)]))

        first_index = random.choice(list(range(sub_grid_index , sub_grid_index + 9)))
        while True:
            second_index = random.choice(list(range(sub_grid_index , sub_grid_index + 9)))
            if first_index != second_index:
                break
        print("sub_grid_index:",sub_grid_index,"first_index:",first_index,"second_index:",second_index)
        print("first:",self.chromosome[first_index],"second:",self.chromosome[second_index])
        
        #swaping two index values
        self.chromosome[first_index], self.chromosome[second_index] = self.chromosome[second_index],self.chromosome[first_index]
        print("first:",self.chromosome[first_index],"second:",self.chromosome[second_index])
    
    def crossOver(self, parent2):
        return
    
    def countRowDuplication(self,blocks):
        duplication = 0
        numbers = []
        rows = []

        for i in range(0,9,3):
            for block in blocks:
                numbers += block[i:i+3]
                if len(numbers) == 9:
                    rows.append(numbers)
                    numbers = []

        # self.standardFormat = rows
        # print("rows:",self.standardFormat)
        
        for row in rows:
            # print("row duplications:",countDuplicateElement(row))
            duplication += countDuplicateElement(row)
        
        return duplication

    def countColDuplication(self,blocks):
        duplication = 0
        numbers = []
        columns = []

        #we start from block 0 , block 1 , block 2 
        # and go downward to caculate columns
        for i in range(3):

            #and go downward block by block
            for j in range(i,i+9,3):
                #go in each block downward number by number
                for k in range(3):
                    numbers.append(blocks[j][k])
                    numbers.append(blocks[j][k+3])
                    numbers.append(blocks[j][k+6])
                if len(numbers) == 9:
                    columns.append(numbers)
                numbers = []
        
        print("columns:",columns)

        for column in columns:
            print("column duplications:",countDuplicateElement(column))
            duplication += countDuplicateElement(column)


        return duplication

    def call_fitness(self):
        fitness = 0
        blocks = []
        for i in range(0,81,9):
            blocks.append(self.chromosome[i:i+9])
        print(self.chromosome)
        print("blocks:",blocks)

        # fitness += self.countRowDuplication(blocks)
        fitness += self.countColDuplication(blocks)

        return fitness
    
    @classmethod
    def tournomentSelection(self, population):
        best = None
        for _ in range(TOURNAMENT_SIZE):
            indiv = random.choice(population)
            if (best == None) or indiv.fitness > best.fitness:
                best = indiv

        return (best)

if __name__ == '__main__':

    # l = [1,1,1,3,3,4,4,4,4,5]
    # print(countDuplicateElement(l))

    #initial sudoku puzzle
    Individual.setOriginalPuzzle(sudoku)

    # #create first generation
    # for _ in range(POPULATION_SIZE):
    #     gnome = Individual.create_chromosome()
    #     indiv = Individual(gnome)
    #     print(indiv.chromosome)

    #     # population.append(indiv)
    
    # while not found:

        # population = sorted(population, reverse=True, key=lambda x: x.fitness)

    #     best_fits.append(population[0].fitness)
    #     avg_fits.append(np.mean([p.fitness for p in population]))

    #     print("generation:", generation, " best fit:", population[0].fitness)

    #     if population[0].fitness == len(CAN_POS) * 10:
    #         found = True
    #         break

    #     new_generation = []

    #     # selection pressure with coefficient 70% of best
    #     index = int(POPULATION_SIZE * 0.7)

    #     for _ in range(POPULATION_SIZE):

    #         # parent selection with Roulette Wheel method
    #         (parent1, parent2) = Individual.rouletteWheelSelection(
    #             population[:index])
    #         child = parent1.crossOver(parent2)

    #         child.mutate()

    #         new_generation.append(child)

    #     population = new_generation
    #     generation += 1

    # if found:
    #     print("generation : ", generation, "       ",
    #         population[0].chromosome[0:10],  population[0].fitness)
    #     plotResult()
        
    # duration = time.time() - start
    # print("minute:", (duration)//60)
    # print("second:", (duration) % 60)
    
