import os

name_to_idx = {}
names = []

folder_to_idx = {}
folders = []

data = []

def scan(path, prev, level):
    listing = os.listdir(path) 
    
    counter = 0
    
    if level == 2:
        print "Scanning " + prev + "...."
    
    global name_to_idx
    global names
    global folder_to_idx
    global folders
    
    for files in listing:
        fullpath = os.path.join(path, files)
        if os.path.isdir(fullpath):
            if level == 1 and (not files in name_to_idx):
                name_to_idx[files] = len(names)
                names.append(files)
                
                print "\tAdding " + files + " to names"
                
            if level == 2 and (not files in folder_to_idx):
                folder_to_idx[files] = len(folder_to_idx)
                folders.append(files)
                
                print "\tAdding " + files + " to folders"
                
            now = scan(fullpath, files, level + 1)
            counter += now
            
            if level == 2:
                data.append((name_to_idx[prev], folder_to_idx[files], now))
        elif level > 2 and files[0] != '.':
            counter += 1
            
    return counter
    
def dump_data_to_csv():
    data_file = open("email_stats.csv", 'w');
    
    global names
    global folders
    
    global data
    
    line = ' ';
    for j in range(0, len(folders)):
        line += "," + str(folders[j])
    line += "\n"
    
    data_file.write(line)
    
    for i in range(0, len(names)):
        line = str(names[i])
        for j in range(0, len(folders)):
            counter = 0
            for (n, f, c) in data:
                if n == i and f == j:
                    counter = c
                    break
            line += "," + str(counter)
        line += "\n"
        data_file.write(line)
        
    data_file.close()

def main():
    email_path = '/Users/arindam/workplace/CS499/enron_mail_20110402'
    global scan_counter
    counter = scan(email_path, '', 0)
    
    dump_data_to_csv()
    
    print "counter: ", counter, " files found\n"


if __name__ == "__main__":
    main()
	
     
