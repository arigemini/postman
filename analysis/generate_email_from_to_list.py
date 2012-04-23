from email_handler import Email
from analysis.email_dir_scanner import EmailDirScanner


class EmailFromToList:
    def __init__(self, email_dir):
        self.scan_counter = 0
        self.email_from_to_list = []
        email_dir_scanner = EmailDirScanner(email_dir, self._should_recurse, self._parse_email)
        email_dir_scanner.scan()
    
    def dump(self, email_from_to_list_csv):
        with open(email_from_to_list_csv, 'w') as f:
            for email, from_, to in self.email_from_to_list:
                print >> f, "{0},{1},{2}".format(email, from_, to)        
    
    def _should_recurse(self, level, dirname, fullpath):
        return level == 0 or (dirname in ["inbox", "deleted_items"])
        # return level == 0 or (dirname not in ["sent", "sent_items", "_sent_mail", "all_documents"])
        # return level == 0 or dirname == "inbox"
        # return self.scan_counter < 1000
   
    def _parse_email(self, email_file):
        if self.scan_counter % 1000 == 0:
            print "********* File ", self.scan_counter, ": ", email_file, " *************\n"
             
        email = Email(email_file)
       
        if len(email.to_list) == 1:
            self.email_from_to_list.append((email_file, email.from_, email.to_list[0]))
           
        self.scan_counter += 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate (email_file,from,to) file by scanning the email directory provided")
    parser.add_argument("--email_dir", type=str, required=True, help="Directory to scan for email files (recursive)")
    parser.add_argument("--email_from_to_file", type=str, required=True, help="(email,from,to) file")
    args = parser.parse_args()
    
    email_from_to_list = EmailFromToList(args.email_dir)
    print "{0} emails scanned".format(email_from_to_list.scan_counter)
    
    print "Dumping email_from_to list to csv file", args.email_from_to_file
    email_from_to_list.dump(args.email_from_to_file)
   
