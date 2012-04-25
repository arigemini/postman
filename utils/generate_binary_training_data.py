import sys

def main():
    lines = []
    max_id = -1
    labels = set()
    for line in sys.stdin:
        line = line.strip()
        lines.append(line)
        splits = line.strip(":").split(",")
        labels.add(splits[0])
        max_id = max(max_id, max(int(feature_id) for feature_id in splits))
    yes = str(max_id + 1)
    no = str(max_id + 2)
    for line in lines:
        splits = line.strip(":").split(",")
        cur_label = splits[0]
        print cur_label
        print labels
        print yes, no
        for label in labels:
            put_label = yes if label == cur_label else no
            splits[0] = label
            print "{0},{1}:".format(put_label, ",".join(splits))
        
        
            
if __name__ == "__main__":
    main()