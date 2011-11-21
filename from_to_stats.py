import sys

outgoing = {}
incoming = {}

def process(from_to_map_csv):
    global outgoing 
    global incoming
    
    filehandle = open(from_to_map_csv, 'r')
    for line in filehandle:
        emails = line.split(",")
        
        from_ = emails[0]
        if not from_ in outgoing:
            outgoing[from_] = 0
        else:
            print >> sys.stderr, from_, "found another time in outgoing list"
        outgoing[from_] += len(emails) - 1

        for cur_email in emails[1:]:
            if not cur_email in incoming:
                incoming[cur_email] = 0
            incoming[cur_email] += 1


def main():
    from_to_map_csv = "etc/from_to_map.csv"
    process(from_to_map_csv)
    print outgoing
    print incoming


if __name__ == "__main__":
    main()
