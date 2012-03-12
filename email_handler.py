from email.parser import Parser

class Email:
    """ 
    Parses an email given the file.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        
        self.from_ = ""
        
        self.subject = ""
        
        self.to_list = []
        self.cc_list = []
        self.bcc_list = []
        
        self.message = ""
        
        self._parseFile()
        
    def _parseFile(self):
        
        infile = open(self.filepath, 'r')
        
        parser = Parser()
        msg = parser.parse(infile)
        
        self.from_ = msg['From'].strip()
        
        if msg.has_key('To'):
            self.to_list = list(w.strip() for w in msg['To'].split(','))
        if msg.has_key('Cc'):
            self.cc_list = list(w.strip() for w in msg['Cc'].split(','))
        if msg.has_key('Bcc'):
            self.bcc_list = list(w.strip() for w in msg['Bcc'].split(','))
        self.subject = msg['Subject'].strip()
        self.message = msg.get_payload().strip()
        
        infile.close()
        
    @property
    def remove_original_message(self):
        idx = self.message.find('-----Original Message-----')
        if idx != -1:
            return self.message[:idx].strip()
        else:
            idx = self.message.find('---------------------- Forwarded by')
            if idx != -1:
                return self.message[:idx].strip()
            else:
                return self.message
        

if __name__ == "__main__":
    """
    usage: python email_handler.py [email_files]
    """
    import sys
    
    for filename in sys.argv[1:]:
        print "**Email file: ", filename
        email = Email(filename)
        print "**From: ", email.from_
        print "**To: ", email.to_list
        print "**Cc: ", email.cc_list
        print "**Bcc: ", email.bcc_list
        print "**Subject: ", email.subject
        print "**Message:\n", email.message
        print "**Without original message: \n", email.remove_original_message
        
