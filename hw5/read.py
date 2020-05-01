import pstats
p = pstats.Stats('output.txt')
p.strip_dirs().sort_stats("time").print_stats()
