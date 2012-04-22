from email.parser import Parser

class Email:
    """ 
    Parses an email given the file.
    """
    FROM_KEY = "From"
    SUBJECT_KEY = "Subject"
    TO_KEY = "To"
    CC_KEY = "Cc"
    BCC_KEY = "Bcc"
    ACTUAL_MESSAGE_DELIMITERS = ['-Original Message-', '-- Forwarded by']
    
    def __init__(self, filepath):
        self.filepath = filepath
        
        self.from_ = ""       
        self.subject = ""
        self.to_list = []
        self.cc_list = []
        self.bcc_list = []
        self.message = ""
        
        self._actual_message = None
        self._parseFile()
        
    @property
    def actual_message(self):
        if self._actual_message:
            return self._actual_message
        self._actual_message = self.message
        for delim in Email.ACTUAL_MESSAGE_DELIMITERS:
            idx = self._actual_message.find(delim)
            if idx != -1:
                self._actual_message = self._actual_message[:idx].strip('-').strip()
        return self._actual_message
        
    def _parseFile(self):
        
        infile = open(self.filepath, 'r')
        
        parser = Parser()
        msg = parser.parse(infile)
        
        if not msg.has_key('From'):
            raise RuntimeError, "{0} does not have From field".format(self.filepath)
        self.from_ = msg['From'].strip()
        
        if not msg.has_key('Subject'):
            raise RuntimeError, "{0} does not have Subject field".format(self.filepath)
        self.subject = msg['Subject'].strip()
        
        if msg.has_key('To'):
            self.to_list = list(w.strip() for w in msg['To'].split(','))
        if msg.has_key('Cc'):
            self.cc_list = list(w.strip() for w in msg['Cc'].split(','))
        if msg.has_key('Bcc'):
            self.bcc_list = list(w.strip() for w in msg['Bcc'].split(','))
        
        self.message = msg.get_payload().strip()
        
        infile.close()
        

if __name__ == "__main__":
    """
    usage: python email_handler.py [email_files]
    """
    import sys
    
    for filename in sys.argv[1:]:
        print "** Email file: ", filename
        email = Email(filename)
        print "\t** From: ", email.from_
        print "\t** To: ", email.to_list
        print "\t** Cc: ", email.cc_list
        print "\t** Bcc: ", email.bcc_list
        print "\t** Subject: ", email.subject
        print "\t** Message:\n", email.message
        print "\t** Actual message: \n", email.actual_message
        
