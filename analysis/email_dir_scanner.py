import os

class EmailDirScanner:
    def __init__(self, email_dir, should_recurse_callback, email_callback):
        self.email_dir = email_dir  
        self.should_recurse_callback = should_recurse_callback
        self.email_callback = email_callback   
    
    def scan(self):
        self._scan(self.email_dir, 0)
   
    def _scan(self, path, level):
        for filename in os.listdir(path):
            fullpath = os.path.join(path, filename)
            if os.path.isdir(fullpath):
                if self.should_recurse_callback(level, filename, fullpath):
                    self._scan(fullpath, level + 1)
            elif filename[0] != '.':
                self.email_callback(fullpath)           
                
if __name__ == "__main__":
    def should_recurse(level, filename, fullpath):
        return filename == "dasovich-j" or filename == "inbox"
    
    def display_email(emailpath):
        print emailpath
    
    email_dir_scanner = EmailDirScanner('{0}/enron_mail_20110402/maildir/'.format(os.getenv('HOME')), should_recurse, display_email)
    email_dir_scanner.scan()