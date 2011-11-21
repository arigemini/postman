import sys

outgoing = {}
incoming = {}

def process(from_to_map_csv):
    global outgoing 
    global incoming
    
    filehandle = open(from_to_map_csv, 'r')
    for line in filehandle:
        emails = line.strip().split(",")
        
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


def dump_outgoing(outgoing_csv):
    writer = open(outgoing_csv, 'w')
    for email, counter in sorted(outgoing.iteritems(), key=lambda x: x[1], reverse=True):
        writer.write("{0},{1}\n".format(email, counter))
    writer.close() 

def dump_incoming(incoming_csv):
    writer = open(incoming_csv, 'w')
    for email, counter in sorted(incoming.iteritems(), key=lambda x: x[1], reverse=True):
        writer.write("{0},{1}\n".format(email, counter))
    writer.close() 

def analysis(both_csv):
    writer = open(both_csv, 'w')
    
    both_counter = {}
    for email in outgoing.keys():
        if email in incoming:
            both_counter[email] = outgoing[email] * incoming[email]

    for email, counter in sorted(both_counter.iteritems(), key=lambda x: x[1], reverse=True):
        writer.write("{0},{1},{2}\n".format(email, outgoing[email], incoming[email])) 

    writer.close()
    

def main():
    from_to_map_csv = "etc/from_to_map.csv"
    outgoing_csv = 'etc/outgoing.csv' 
    incoming_csv = 'etc/incoming.csv'
    both_csv = 'etc/both_outgoing_incoming.csv'
   
    process(from_to_map_csv)

    print >> sys.stderr, "Dumping data to csv files", outgoing_csv, " and ", incoming_csv
    dump_outgoing(outgoing_csv)
    dump_incoming(incoming_csv)
    
    print >> sys.stderr, "analysis"
    analysis(both_csv)

if __name__ == "__main__":
    main()
