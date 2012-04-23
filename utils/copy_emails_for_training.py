import collections
import os
import shutil

def mkdir_p(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class CopyEmails:
    def __init__(self, email_from_to_file):
        self.email_from_to_file = email_from_to_file
        
    def process(self, email_ids, output_dir):
        self.directory_to_counter = collections.defaultdict(int)
        with open(self.email_from_to_file, 'r') as f:
            for idx, line in enumerate(f):
                if idx % 1000 == 0:
                    print "{0}: {1}".format(idx, line)
                email, _, to = line.strip().split(',')
                if to in email_ids:
                    to_dir = os.path.join(output_dir, to.replace("@", "_at_"))
                    to_file = os.path.join(to_dir, str(self.directory_to_counter[to_dir]))
                    self.directory_to_counter[to_dir] += 1
                    mkdir_p(to_dir)
                    shutil.copy(email, to_file)
        
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Copy emails for training into a different directory")
    parser.add_argument("--email_from_to_file", type=str, required=True, help="input (email,from,to) file")
    parser.add_argument("--output_dir", type=str, required=True, help="directory to put the emails into")
    args = parser.parse_args()
    
    # Sorted in decreasing number of incoming emails
    email_ids = ['pete.davis@enron.com',
                 'gerald.nemec@enron.com',
                 'kenneth.lay@enron.com',
                 'sara.shackleton@enron.com',
                 'jeff.skilling@enron.com',
                 'jeff.dasovich@enron.com',
                 'tana.jones@enron.com',
                 'rick.buy@enron.com',
                 'barry.tycholiz@enron.com',
                 'lcampbel@enron.com',
                 'tracy.geaccone@enron.com',
                 'joe.parks@enron.com',
                 'sally.beck@enron.com',
                 'mark.whitt@enron.com',
                 'matt.smith@enron.com',
                 'kay.mann@enron.com',
                 'j.kaminski@enron.com',
                 'elizabeth.sager@enron.com',
                 'don.baughman@enron.com',
                 'kam.keiser@enron.com']   
    
    copy_emails = CopyEmails(args.email_from_to_file)
    copy_emails.process(set(email_ids), args.output_dir)
