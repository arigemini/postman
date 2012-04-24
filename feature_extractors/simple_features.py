import string

class SimpleFeatures(object):
            
    def __init__(self):
        pass
    
    def features(self, email):
        features = {}
        features['from'] = email.from_
        features['subject'] = filter(lambda x: x not in ["RE", "FW", "Re"], 
                                      map(lambda x: x.strip(string.punctuation), 
                                            email.subject.split()))
        features['first-3'] = filter(lambda x: x and x[0].isupper(),
                                       map(lambda x: x.strip(string.punctuation), 
                                               email.actual_message.split()[:3]))
        return features

if __name__ == "__main__":
    from email_handler import Email
    import sys
    
    for email_file in sys.argv[1:]:
        features = SimpleFeatures().features(Email(email_file))
        print "[EMAIL]:", email_file
        print "\t[FEATURES]:", features