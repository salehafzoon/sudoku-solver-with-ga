import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from random import randint

sudoku=[
0,0,0,  0,0,0,  5,2,0,
9,0,2,  1,0,0,  7,3,4,
0,0,7,  9,0,2,  0,8,0,

8,2,9,  7,0,0,  0,0,5,
0,0,0,  8,0,6,  0,0,0,
5,0,0,  0,0,9,  3,7,8,

0,1,0,  5,0,3,  4,0,0,
6,3,5,  0,0,7,  2,0,1,
0,9,4,  0,0,0,  0,0,0]

start = time.time()
generation = 1
found = False
population = []
best_fits = []
avg_fits = []

POPULATION_SIZE = 500
TOURNAMENT_SIZE = 4
MUTATION_RATE = 0.3
CROSSOVER_RATE = 1
ELITSM = 0.3
MAX_GENERATION = 100
FITNESS_MODE = "mode2"
MAX_FITNESS = 144
XOVER_METHOD = "arithmetic"

def calculateListFitness(array):
    l = list(range(1,10))
    fitness = 0
    for num in l:
        if array.count(num)>1:
            fitness += array.count(num)-1
        elif array.count(num)== 0 and FITNESS_MODE == "mode2":
            fitness += 1
    
    return fitness

class Individual(object):

    def __init__(self, chromosome):
        self.original_puzzle = []
        self.chromosome = chromosome
        self.fitness = self.call_fitness()
    
    def isValid(self,bIndex,numIndex):

        if self.helpArray[bIndex][numIndex] != 0:
            return False
        else :
            return True

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

    def printStandardFormat(self):
        rows = [[],[],[],[],[],[],[],[],[]]
        rIndex = 0
        for i in range(len(self.chromosome)):
            block = self.chromosome[i]
            
            if i <3:
                rIndex = 0
            elif i< 6:
                rIndex = 3
            else:
                rIndex = 6

            rows[rIndex] += (block[0:3])
            rows[rIndex+1] += (block[3:6])
            rows[rIndex+2] += (block[6:9])
        
        print("\n",rows)

    @classmethod
    def setOriginalPuzzle(self,puzzle):
        self.original_puzzle = puzzle
        self.helpArray = Individual.convertToBlockFormat(self.original_puzzle)

    @classmethod
    def create_chromosome(self):
        if self.original_puzzle == []:
            print("original puzzle didn't set.")
            return
        else:
            
            chromosome = []
            for x in self.original_puzzle :
                y = x if x!=0 else randint(1, 9)
                chromosome.append(y)
            
            # print("initial:",chromosome)
            chromosome = Individual.convertToBlockFormat(chromosome)
            
            return chromosome
    
    def mutate1(self):

        #select one of puzzle subgrid randomly(first index of subgrid)
        block_index = random.randint(0,8)
        block = self.chromosome[block_index]
        first_index = random.randint(0,8)
        while True:
            second_index = random.randint(0,8)
            if first_index != second_index:
                break
        
        #swaping two index values if valid by use of help array
        if self.isValid(block_index,first_index) and self.isValid(block_index,second_index):
            block[first_index], block[second_index] = block[second_index],block[first_index]
            self.chromosome[block_index] = block
        
        self.call_fitness()
    
    def mutate2(self):
        
        #swap mutation in each block
        for block in self.chromosome :
            first_index = random.randint(0,8)
            while True:
                second_index = random.randint(0,8)
                if first_index != second_index:
                    break
            
            block_index = self.chromosome.index(block)

            if self.isValid(block_index,first_index) and self.isValid(block_index,second_index):
                block[first_index], block[second_index] = block[second_index],block[first_index]
            
            self.call_fitness()

    def crossOver(self, parent2):
        child1 = []
        child2 = []

        if XOVER_METHOD == "uniform":
            for b1, b2 in zip(self.chromosome, parent2.chromosome):
                prob = random.random()
                if(prob > 0.5):
                    child1.append(b1)
                    child2.append(b2)
                else:
                    child1.append(b2)
                    child2.append(b1)

        if XOVER_METHOD == "arithmetic":
            for c1, c2 in zip(self.chromosome, parent2.chromosome):
                bound = random.random()
                prob = random.random()
                if(prob > bound):
                    child1.append(c1)
                    child2.append(c2)

                else:
                    child1.append(c2)
                    child2.append(c1)
        if XOVER_METHOD == "orderOne":
            index1 = randint(0, 8)
            index2 = randint(0, 8)
            
        return (Individual(child1), Individual(child2))
    
    def countRowDuplication(self,blocks):
        fitness = 0
        numbers = []
        rows = []

        for i in range(0,9,3):
            for block in blocks:
                numbers += block[i:i+3]
                if len(numbers) == 9:
                    rows.append(numbers)
                    numbers = []

        for row in rows:
            # print("row:",row,"duplicate:",calculateListFitness(row))
            fitness += calculateListFitness(row)
        
        # print("\n")
        return fitness

    def countColDuplication(self,blocks):
        fitness = 0
        numbers = []
        columns = []

        #we start from block 0 , block 1 , block 2 
        # and go downward to caculate columns
        for i in range(3):

            #and go downward block by block
            #go in each block downward number by number    
            for k in range(3):
                for j in range(i,i+9,3):
                    numbers.append(blocks[j][k])
                    numbers.append(blocks[j][k+3])
                    numbers.append(blocks[j][k+6])

                if len(numbers) == 9:
                    columns.append(numbers)
                    numbers = []
        
        for column in columns:
            # print("col:",column,"duplicate:",calculateListFitness(column))
            fitness += calculateListFitness(column)

        return fitness

    def call_fitness(self):
        fitness = 0

        fitness += self.countRowDuplication(self.chromosome)
        fitness += self.countColDuplication(self.chromosome)

        # for block in self.chromosome :
        #     fitness += calculateListFitness(block)

        # fitness = 1.00 - (float(fitness)/MAX_FITNESS)

        return fitness
    
    @classmethod
    def tournomentSelection(self, population):
        best = None
        for _ in range(TOURNAMENT_SIZE):
            indiv = random.choice(population)
            if (best == None) or indiv.fitness < best.fitness:
                best = indiv

        return (best)

if __name__ == '__main__':

    #initial sudoku puzzle
    Individual.setOriginalPuzzle(sudoku)

    #create first generation
    for _ in range(POPULATION_SIZE):
        chromosome = Individual.create_chromosome()
        indiv = Individual(chromosome)
        population.append(indiv)
    
    while not found:
        population = sorted(population, reverse=False, key=lambda x: x.fitness)

        best_fits.append(population[0].fitness)
        avg_fits.append(np.mean([p.fitness for p in population]))

        # for ind in population[0:6]:
        #     print(ind.fitness ,"   ",end="")
        # print("\n")

        print("generation:", generation, " best fit:", population[0].fitness)
       
        if population[0].fitness == 1:
            found = True
            break
        if generation == MAX_GENERATION:
            print("not found")
            break

        new_generation = []

        # elitism 80%
        index = int(POPULATION_SIZE * ELITSM)
        new_generation += population[0:index]
        
        for _ in range(int( POPULATION_SIZE* (1-ELITSM) ) ):

            # parent selection with Tournament
            parent1 = Individual.tournomentSelection(population[index:])
            parent2= Individual.tournomentSelection(population[index:])
            
            if random.random() < CROSSOVER_RATE :
                child1,child2 = parent1.crossOver(parent2)
            else:
                child1,child2 = parent1,parent2

            if random.random() < MUTATION_RATE :
                child1.mutate2()

            if random.random() < MUTATION_RATE :
                child2.mutate2()

            new_generation.append(child1)
            new_generation.append(child2)

        population = new_generation
        generation += 1

    print("generation : ", generation, "       ",
        population[0].chromosome,  population[0].fitness)
    
    population[0].printStandardFormat()
    
    # plotResult()
        
    duration = time.time() - start
    print("minute:", (duration)//60)
    print("second:", (duration) % 60)
    
