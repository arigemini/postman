import sys

def main(id_mappings_file, emails_file):
    id_to_value = {}
    
    email_list = []
    if emails_file:
        with open(emails_file, 'r') as f:
            for line in f:
                email_list.append(line.strip())
    
    with open(id_mappings_file, 'r') as f:
        for line in f:
            line = line.strip()
            idx = line.index(':')
            cur_id, value = line[:idx], line[idx + 2:]
            if id in id_to_value:
                raise RuntimeError, "id {0} occurs twice in id_mappings file".format(id)
            id_to_value[cur_id] = value
    
    for line_num, line in enumerate(sys.stdin):
        print "Line {0} - {1}".format(line_num, line.strip())
        if email_list:
            print "  - Email: {0}".format(email_list[line_num])
        line = line.strip().strip(':')
        for cur_id in line.split(','):
            if cur_id not in id_to_value:
                print "id {0} not found in id_mappings_file".format(cur_id)
            print "  - {0}: {1}".format(cur_id, id_to_value[cur_id])
        

if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print "usage: cat <csv file with feature ids> | python", __file__, "<id_mappings_file> [emails_file]"
        exit(1)
    emails_file = sys.argv[2] if len(sys.argv) ==3 else None
    main(sys.argv[1], emails_file)