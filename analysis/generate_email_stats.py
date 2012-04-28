from analysis.email_dir_scanner import EmailDirScanner
import collections


class EmailStats:
    def __init__(self, email_dir):
        self.scan_counter = 0
        self.emails_by_person = collections.defaultdict(int)
        self.emails_by_folder = collections.defaultdict(int)
        self.cur_person = "?"
        self.cur_folder = "?"
        email_dir_scanner = EmailDirScanner(email_dir, self._should_recurse, self._parse_email)
        email_dir_scanner.scan()
    
    def dump_emails_by_person(self, emails_by_person_file):
        with open(emails_by_person_file, 'w') as f:
            for person, num_emails in sorted(self.emails_by_person.iteritems(), key=lambda x: x[1], reverse=True):
                print >> f, "{0},{1}".format(person, num_emails)        
    
    def dump_emails_by_folder(self, emails_by_folder_file):
        with open(emails_by_folder_file, 'w') as f:
            for folder, num_emails in sorted(self.emails_by_folder.iteritems(), key=lambda x: x[1], reverse=True):
                print >> f, "{0},{1}".format(folder, num_emails)  
    
    def _should_recurse(self, level, dirname, fullpath):
        if level == 0:
            self.cur_person = dirname
        if level == 1:
            self.cur_folder = dirname
        return True
   
    def _parse_email(self, email_file):
        if self.scan_counter % 100000 == 0:
            print "********* File ", self.scan_counter, ": ", email_file, " *************"
        self.scan_counter += 1
        
        self.emails_by_person[self.cur_person] += 1
        self.emails_by_folder[self.cur_folder] += 1

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate (person, no. of emails) and (folder_type, no. of emails) files by scanning the email directory provided")
    parser.add_argument("--email_dir", type=str, required=True, help="Directory to scan for email files (recursive)")
    parser.add_argument("--emails_by_person_file", type=str, required=True, help="(person's folder, no. of emails) file")
    parser.add_argument("--emails_by_folder_file", type=str, required=True, help="(folder type, no. of emails) file")
    args = parser.parse_args()
    
    email_stats = EmailStats(args.email_dir)
    print "{0} emails scanned".format(email_stats.scan_counter)
    
    print "Dumping emails_by_person to csv file", args.emails_by_person_file
    email_stats.dump_emails_by_person(args.emails_by_person_file)
   
    print "Dumping emails_by_folder to csv file", args.emails_by_folder_file
    email_stats.dump_emails_by_folder(args.emails_by_folder_file)
