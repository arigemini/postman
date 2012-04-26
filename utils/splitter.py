import sys
import random

def main(filename_suffix):
    NUM_FILES = 5
    
    file_handles = [open("{0}-{1}.snow".format(filename_suffix, i + 1), 'w') for i in xrange(NUM_FILES)]
    positions = [i for i in xrange(NUM_FILES)]
    counter = [0] * NUM_FILES
    
    for idx, line in enumerate(sys.stdin):
        line = line.strip()
        idx %= NUM_FILES
        rand = random.randint(idx, NUM_FILES - 1)
        print >> file_handles[positions[rand]], line
        counter[positions[rand]] += 1
        positions[idx], positions[rand] = positions[rand], positions[idx]
    
    for i in xrange(NUM_FILES):
        print file_handles[i].name, counter[i]
        file_handles[i].flush()
        file_handles[i].close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: python", __file__, "<output_file_suffix>"
        exit()
    main(sys.argv[1])