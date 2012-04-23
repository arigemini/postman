import os
import sys
import collections
from email_handler import Email
from analysis.email_dir_scanner import EmailDirScanner


class WordAndFromToAnalysis:
    def __init__(self, email_dir):
        self.scan_counter = 0
        self.word_map = collections.defaultdict(int)
        self.email_from_to_list = []
        email_dir_scanner = EmailDirScanner(email_dir, self._should_recurse, self._parse_email)
        email_dir_scanner.scan()
        
    def dump_word_map(self, word_map_csv):
        with open(word_map_csv, 'w') as f:
            for k, v in self.word_map.iteritems():
                print >> f, "{0},{1}".format(k, v)
    
    def dump_email_from_to_list(self, email_from_to_list_csv):
        with open(email_from_to_list_csv, 'w') as f:
            for email, from_, to in self.email_from_to_list:
                print >> f, "{0},{1},{2}".format(email, from_, to)        
    
    def _should_recurse(self, level, dirname, fullpath):
        # return True
        return self.scan_counter < 1000
   
    def _parse_email(self, email_file):
        if self.scan_counter % 1000 == 0:
            print "********* File ", self.scan_counter, ": ", email_file, " *************\n"
             
        email = Email(email_file)
                    
        for word in email.message.split():
            word = word.strip(',.').lower()
            self.word_map[word] += 1
                        
        if len(email.to_list) == 1:
            self.email_from_to_list.append((email_file, email.from_, email.to_list[0]))
           
        self.scan_counter += 1


if __name__ == "__main__":
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Generate (word,frequency) and (email_file,from,to) files by scanning the email directory provided")
    parser.add_argument("--email_dir", type=str, required=True, help="Directory to scan for email files (recursive)")
    parser.add_argument("--word_map_file", type=str, required=True, help="(word, freq) file")
    parser.add_argument("--email_from_to_file", type=str, required=True, help="(email,from,to) file")
    args = parser.parse_args()
    
    word_and_from_to_analysis = WordAndFromToAnalysis(args.email_dir)
    
    print >> sys.stderr, "Dumping word map to csv file", args.word_map_file
    word_and_from_to_analysis.dump_word_map(args.word_map_file)
    print >> sys.stderr, "Dumping email_from_to list to csv file", args.email_from_to_file
    word_and_from_to_analysis.dump_email_from_to_list(args.email_from_to_file)
   
