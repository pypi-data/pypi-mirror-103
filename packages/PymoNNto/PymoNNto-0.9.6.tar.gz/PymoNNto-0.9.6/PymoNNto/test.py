from PymoNNto.Exploration.Evolution.Evolution import *

if __name__ == '__main__':
    evo = Evolution(name='abc',
                slave_file='Exploration/Evolution/test_slave.py',
                individual_count=10,
                mutation=0.05,
                death_rate=0.5,
                constraints=['a<b','b<=c'],
                inactive_genome_info={},
                start_genomes=[{'a':1,'b':2,'c':2,'d':2,'e':3}],
                devices={'multi_thread': 4}
                )

    if not evo.start(ui=False):
        evo.continue_evolution(ui=False)

