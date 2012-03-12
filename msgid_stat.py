import os

message_id_map = {}

MAX_FILES = 100000;

def parsefile(filepath):
    parsefile.counter = parsefile.counter + 1;  
    if parsefile.counter > MAX_FILES: # Limit the total number of files scanned
        return 0
    
    if parsefile.counter % 1000 == 0:
        # print "****"
        print "********* File ", parsefile.counter, ": ", filepath, " *************\n"
         
    infile = open(filepath, 'r')
    
    messageStart = False
    
    global message_id_map
    
    for line in infile.readlines():
        modified = line.strip()
        if modified.startswith("Message-ID: "):
            curID = modified.split()[1].strip()
            if curID in message_id_map:
                if 'sent' in filepath and 'inbox' in message_id_map[curID] or \
                'inbox' in filepath and 'sent' in message_id_map[curID]:
                    print "curID -> " + curID + "\n" + filepath + " " + message_id_map[curID] + "\n"
            else:
                message_id_map[curID] = filepath
                
                
    infile.close()
    
    return 1
   
parsefile.counter = 0


def recurse_into(level, name):
    return level < 2 or name == "inbox" or name == "sent"


def scan(path, level):
    listing = os.listdir(path) 
    
    counter = 0
    
    for files in listing:
        fullpath = os.path.join(path, files)
        if os.path.isdir(fullpath):
            if recurse_into(level, files):
                counter += scan(fullpath, level + 1)
        elif level > 1 and files[0] != '.':
            counter += parsefile(fullpath)
        if counter >= MAX_FILES:
            break
    
    return counter
   
   
def main():
    email_path = '/Users/arindam/workplace/CS499/enron_mail_20110402'
    counter = scan(email_path, 0)
    print "counter: ", counter, " files scanned\n"



if __name__ == "__main__":
    main()