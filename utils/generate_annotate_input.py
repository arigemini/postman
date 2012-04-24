from analysis.email_dir_scanner import EmailDirScanner
from email_handler import Email
import os

class GenerateAnnotateInput:
    def __init__(self, email_dir, output_dir):
        os.makedirs(output_dir)
        self.email_dir = email_dir
        self.output_dir = output_dir
        self.scan_counter = 0
        email_dir_scanner = EmailDirScanner(email_dir, lambda a, b, c: True, self.parse_email)
        email_dir_scanner.scan()

    def parse_email(self, email_fullpath):
        if self.scan_counter % 100 == 0:
            print "******", self.scan_counter, "FILE:", email_fullpath, "******"
        self.scan_counter += 1
        output_file = email_fullpath.replace(self.email_dir, self.output_dir)
        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        email = Email(email_fullpath)
        with open(output_file, 'w') as f:
            print >> f, email.subject
            print >> f, email.actual_message
    
   
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "usage: python", __file__, "<email_dir> <output_dir>"
        exit()
    
    generate_annotate_input = GenerateAnnotateInput(sys.argv[1], sys.argv[2])
       
        