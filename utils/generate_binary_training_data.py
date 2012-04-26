import sys

def main():
    line_splits = []
    labels = set()
    max_id = -1
    for line in sys.stdin:
        splits = line.strip().strip(":").split(",")
        line_splits.append(splits)
        labels.add(splits[0])
        max_id = max(max_id, max(int(feature_id) for feature_id in splits))
        
    yes = max_id + 1
    no = max_id + 2
    
    for splits in line_splits:
        actual_label = splits[0]
        for label in labels:
            splits[0] = label
            new_label = yes if label == actual_label else no
            print "{0},{1}:".format(new_label, ",".join(splits))
            
if __name__ == "__main__":
    main()