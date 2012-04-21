import os
import sys
import collections
from email_handler import Email

word_map = {}
from_to_map = collections.defaultdict(lambda: collections.defaultdict(int))

# MAX_FILES = 10000
scan_counter = 0


def parsefile(filepath):
    global scan_counter
    
    #if scan_counter == MAX_FILES: # Limit the total number of files scanned
    #     return
    
    if scan_counter % 1000 == 0:
        print "********* File ", scan_counter, ": ", filepath, " *************\n"
         
    email = Email(filepath)
        
    global word_map
    
    for word in email.message.split():
        word = word.strip(',.').lower()
        if word in word_map:
            word_map[word] = word_map[word] + 1
        else:
            word_map[word] = 1
                    
    global from_to_map
             
    recipients = email.to_list + email.cc_list + email.bcc_list
    if len(recipients) == 1:
        from_to_map[email.from_][recipients[0]] += 1
       
    scan_counter += 1


def recurse_into(level, name):
    return True


def scan(path, level):
    listing = os.listdir(path) 
    
    global scan_counter
    
    for files in listing:
        fullpath = os.path.join(path, files)
        if os.path.isdir(fullpath):
            if recurse_into(level, files):
                scan(fullpath, level + 1)
        elif level > 1 and files[0] != '.':
            parsefile(fullpath)
        # if scan_counter >= MAX_FILES:
        #     break
   
   
def dump_word_map(word_map_csv):
    word_map_file = open(word_map_csv, 'w')
    global word_map
    for k, v in word_map.iteritems():
        line = k + "," + str(v) + "\n"
        word_map_file.write(line)
    word_map_file.close()
    
    
def dump_from_to_map(from_to_map_csv):
    from_to_map_file = open(from_to_map_csv, 'w')
    global from_to_map
    for email, tos in from_to_map.iteritems():
        line = email
        for to, freq in tos.iteritems():
            line += "," + to + "," + str(freq)
        line += "\n"
        from_to_map_file.write(line)
    from_to_map_file.close()
        

def main():
    email_path = '/Users/arindam/workplace/CS499/enron_mail_20110402/maildir'
    word_map_csv = 'etc/word_map.csv'
    from_to_map_csv = 'etc/from_to_map.csv'

    global scan_counter
    scan(email_path, 0)
    
    print >> sys.stderr, "counter: ", scan_counter, " files scanned\n"

    print >> sys.stderr, "Dumping word map to csv file", word_map_csv
    dump_word_map(word_map_csv)
    print >> sys.stderr, "Dumping from_to map to csv file", from_to_map_csv
    dump_from_to_map(from_to_map_csv)


if __name__ == "__main__":
    main()
