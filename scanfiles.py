import os
from email_handler import Email

word_map = {}
from_to_map = {}

#MAX_FILES = 10000
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
             
    if not (email.sender in from_to_map):
        from_to_map[email.sender] = set()
    full_list = email.to_list
    full_list.extend(email.cc_list)
    full_list.extend(email.bcc_list)
    for cur_email in full_list:
        from_to_map[email.sender].add(cur_email);
        
    scan_counter += 1


def recurse_into(level, name):
    return True
    #return level < 2 or name == "inbox" or name == "sent"


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
        #if scan_counter >= MAX_FILES:
        #    break
   
   
def dump_word_map():
    word_map_file = open("wordmap", 'w')
    global word_map
    for k, v in word_map.items():
        line = k + " : " + str(v) + "\n"
        word_map_file.write(line)
    word_map_file.close()
    
    
def dump_from_to_map():
    from_to_map_file = open("fromtomap", 'w')
    global from_to_map
    for k, v in from_to_map.items():
        line = k + " :"
        for email in v:
            line += " " + email
        line += "\n"
        from_to_map_file.write(line)
    from_to_map_file.close()
        

def main():
    email_path = '/Users/arindam/workplace/CS499/enron_mail_20110402'
    global scan_counter
    scan(email_path, 0)
    
    dump_word_map()
    dump_from_to_map()
    
    print "counter: ", scan_counter, " files scanned\n"


if __name__ == "__main__":
    main()