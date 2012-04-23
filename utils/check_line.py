import sys

def main(label_ids_file, feature_ids_file):
    labels = set()
    with open(label_ids_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                labels.add(line)
    with open(feature_ids_file, 'r') as f:
        for line in f:
            if not "to" in line:
                continue
            line = line.strip()
            splits = line.split(" ")
            label = splits[0].replace(":", "")
            if label in labels:
                print label, splits[2]
                 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: python", __file__, "labels.snow feature_id_to_string_mappings.snow"
        exit(1)
    main(sys.argv[1], sys.argv[2])