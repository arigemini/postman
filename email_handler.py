from email.parser import Parser

class Email:
    """ 
    Parses an email given the file.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        
        self.sender = ""
        
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
        
        self.sender = msg['From'].strip()
        
        if msg.has_key('To'):
            self.to_list = list(w.strip() for w in msg['To'].split(','))
        if msg.has_key('Cc'):
            self.cc_list = list(w.strip() for w in msg['Cc'].split(','))
        if msg.has_key('Bcc'):
            self.bcc_list = list(w.strip() for w in msg['Bcc'].split(','))
        
        self.subject = msg['Subject'].strip()
        
        self.message = msg.get_payload()
        
        
        infile.close()

        