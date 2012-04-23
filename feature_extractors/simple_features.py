import string

class SimpleFeatures(object):
    
    ENDINGS = ["Thanks", "Regards", "Best"]
    
    def __init__(self):
        pass
    
    def features(self, email):
        features = {'from': email.from_, 'subject': " ".join(email.subject.split())}
        actual_message = email.actual_message
        
        split_message = actual_message.split()
        features['first-3'] = filter(lambda x: x and x not in ["Hi", "Hello", "Dear", "Hey"] and x[0].isupper(),
                                        map(lambda x: x.strip(string.punctuation), 
                                                split_message[:3]))
        
        for ending in SimpleFeatures.ENDINGS:    
            idx = actual_message.find(ending)
            if idx != -1:
                splits = actual_message[idx + len(ending) + 1:].strip().split()
                if 0 < len(splits) < 4:
                    features['senderInfo'] = " ".join(splits)
                    break
       
        return features

if __name__ == "__main__":
    from email_handler import Email
    import sys
    
    for email_file in sys.argv[1:]:
        features = SimpleFeatures().features(Email(email_file))
        print "[EMAIL]:", email_file
        print "\t[FEATURES]:", features