from typing import List, Tuple
from ResetMoves import ResetMovement
from ResetAgent import ResetAgent, RandomAgent, ClosestAgent, AStartAgent, NeatAgent
from BoardGenerator import BoardGenerator
from tqdm import tqdm
import neat
import os

generator = BoardGenerator("magnus.pgn")

from multiprocessing import Pool


class ParallelEvaluator(object):

    def __init__(self,
                 num_workers,
                 eval_function,
                 timeout=None,
                 maxtasksperchild=None):
        """
        eval_function should take one argument, a tuple of (genome object, config object),
        and return a single float (the genome's fitness).
        """
        self.eval_function = eval_function
        self.timeout = timeout
        self.pool = Pool(processes=num_workers,
                         maxtasksperchild=maxtasksperchild)

    def __del__(self):
        self.pool.close()
        self.pool.join()
        self.pool.terminate()

    def evaluate(self, genomes, config):
        jobs = []
        for ignored_genome_id, genome in genomes:
            jobs.append(
                self.pool.apply_async(self.eval_function, (genome, config)))

        # assign the fitness back to each genome
        for job, (ignored_genome_id, genome) in zip(jobs, genomes):
            genome.fitness = job.get(timeout=self.timeout)


def evaluateListOfResetMoves(moves: List[ResetMovement]):
    return sum([m.getTotalTime() for m in moves]), sum([
        m.getTotalEuclidDistance() for m in moves
    ]), sum([m.getNumberOfHorizontalMoves() for m in moves])


# def main():

#     boards = generator.get_boards()
#     scores = []
#     for board in tqdm(boards):
#         agent = AStartAgent(board)
#         moves = agent.generateSeriesOfResetMoves()
#         scores.append(evaluateListOfResetMoves(moves)[2])

#     print(f"Average: {sum(scores) / len(scores)}")

# if __name__ == "__main__":
#     main()


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        print(genome_id)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for board in generator.get_boards()[:10]:
            agent = NeatAgent(board, net)
            moves = agent.generateSeriesOfResetMoves()
            genome.fitness = 10000 / evaluateListOfResetMoves(moves)[0]


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 1)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat.config')
    run(config_path)
