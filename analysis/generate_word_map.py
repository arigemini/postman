import collections
from email_handler import Email
from analysis.email_dir_scanner import EmailDirScanner


class WordMap:
    def __init__(self, email_dir):
        self.scan_counter = 0
        self.word_map = collections.defaultdict(int)
        email_dir_scanner = EmailDirScanner(email_dir, self._should_recurse, self._parse_email)
        email_dir_scanner.scan()
        
    def dump(self, word_map_csv):
        with open(word_map_csv, 'w') as f:
            for k, v in self.word_map.iteritems():
                print >> f, "{0},{1}".format(k, v)  
    
    def _should_recurse(self, level, dirname, fullpath):
        return True
        # return self.scan_counter < 1000
   
    def _parse_email(self, email_file):
        if self.scan_counter % 1000 == 0:
            print "********* File ", self.scan_counter, ": ", email_file, " *************\n"
             
        email = Email(email_file)
                    
        for word in email.actual_message.split():
            word = word.strip(',.').lower()
            if word:
                self.word_map[word] += 1
                        
        self.scan_counter += 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate (word,frequency) file by scanning the email directory provided")
    parser.add_argument("--email_dir", type=str, required=True, help="Directory to scan for email files (recursive)")
    parser.add_argument("--word_map_file", type=str, required=True, help="(word, freq) file")
    args = parser.parse_args()
    
    word_map = WordMap(args.email_dir)
    print "{0} emails scanned".format(word_map.scan_counter)
    
    print "Dumping word map to csv file", args.word_map_file
    word_map.dump(args.word_map_file)
   
