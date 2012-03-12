import os
import sys

name_to_idx = {}
names = []

folder_to_idx = {}
folders = []

data = {}

person_emails = {}
folder_emails = {}

def scan(path, person, level):
    
    print >> sys.stderr, "Scanning " + person + " " + path + "...."
    
    global name_to_idx
    global names
    global folder_to_idx
    global folders

    counter = 0
    
    listing = filter(lambda x: x[0] != '.', os.listdir(path))
    for files in listing:       
        fullpath = os.path.join(path, files)
        if level == 0:
            if not os.path.isdir(fullpath):
                raise RuntimeError("{0} is not a directory".format(fullpath))
            print >> sys.stderr, "\tAdding " + files + " to names"
            name_to_idx[files] = len(names)
            names.append(files)
            data[name_to_idx[files]] = {}

            now = scan(fullpath, files, 1)
            person_emails[files] = now
            counter += now

        elif level == 1:
            if not os.path.isdir(fullpath):
                print >> sys.stderr, "{0} is not a directory".format(fullpath)
                continue
            if not files in folder_to_idx:
                folder_to_idx[files] = len(folder_to_idx)
                folders.append(files)
                print >> sys.stderr, "\t\tAdding " + files + " to folders"
            
            now = scan(fullpath, person, level + 1)
            data[name_to_idx[person]][folder_to_idx[files]] = now
            counter += now
        
            if not files in folder_emails: folder_emails[files] = 0
            folder_emails[files] += now
        else:
            if os.path.isdir(fullpath):
                counter += scan(fullpath, person, level + 1)
            else:
                counter += 1
    
    return counter

def dump_sparse_csv(sparse_csv_file):
    global names
    global folders
    
    global data

    writer = open(sparse_csv_file, 'w')
    
    line = ' ';
    for j in range(0, len(folders)):
        line += "," + str(folders[j])
    line += "\n"
    
    writer.write(line)

    for i in range(0, len(names)):
        line = str(names[i])
        for j in range(0, len(folders)):
            counter = data[i].get(j, 0)
            line += "," + str(counter)
        line += "\n"
        writer.write(line)
    
    writer.close()

def dump_grouped_csv(grouped_csv_file):
    
    writer = open(grouped_csv_file, 'w')
    
    writer.write("Name,Emails\n")
    for person, emails in sorted(person_emails.iteritems(), key=lambda x: x[1], reverse=True):
        writer.write("{0},{1}\n".format(person, emails))
    writer.write("\n")
   
    writer.write("Folder, Emails\n")
    for folder, emails in sorted(folder_emails.iteritems(), key=lambda x: x[1], reverse=True):
        writer.write("{0},{1}\n".format(folder, emails))
    writer.write("\n")
    
    for personidx, folderidx_counter in sorted(data.iteritems(), key=lambda x: names[x[0]]):
        writer.write(names[personidx] + "\n")
        for folder_idx, counter in sorted(folderidx_counter.iteritems(), key=lambda x: folders[x[0]]):
            writer.write("{0},{1}\n".format(folders[folder_idx], counter))
        writer.write("\n")
   
    writer.close()

def main():
    email_path = 'enron_mail_20110402/maildir'
    sparse_csv_file = 'etc/email_sparse_stats.csv'
    grouped_csv_file = 'etc/email_grouped_stats.csv' 

    global scan_counter
    counter = scan(email_path, '', 0)
        
    print >> sys.stderr, "counter: ", counter, " files found"
    
    print >> sys.stderr, "checking..."
    sum_person = sum([value for value in person_emails.values()])
    sum_folders = sum([value for value in folder_emails.values()])
    assert(sum_person == sum_folders)
    assert(sum_person == counter)
    assert(counter == sum([counter for folder_counter in data.values() for counter in folder_counter.values()]))

    print >> sys.stderr, "dumping data to grouped csv file", grouped_csv_file, "..."
    dump_grouped_csv(grouped_csv_file)

    print >> sys.stderr, "dumping data to sparse csv file", sparse_csv_file, "..."
    dump_sparse_csv(sparse_csv_file)
    
    


if __name__ == "__main__":
    main()

     
