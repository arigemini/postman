import string

class SimpleFeatures(object):
    
    GREETINGS = ["Hi", "Hello", "Dear", "Hey"]
        
    def __init__(self):
        pass
    
    def features(self, email):
        features = {'from': email.from_, 'subject': " ".join(email.subject.split())}
        actual_message = email.actual_message
        
        split_message = actual_message.split()
        features['first-3'] = filter(lambda x: x and x[0].isupper(),
                                        map(lambda x: x.strip(string.punctuation), 
                                                split_message[:3]))
        
        # Try to get the toInfo from an email, by checking if the email starts
        # with a greeting or just the name of the person
        toInfo = None
        if len(split_message) > 1 and actual_message[len(split_message[0])] in "\n,":
            toInfo = split_message[0].strip(string.punctuation)
        else:
            for greeting in SimpleFeatures.GREETINGS:
                if actual_message.startswith(greeting):
                    pos = len(greeting) + 1;
                    while actual_message[pos].isalpha():
                        pos += 1
                    toInfo = actual_message[len(greeting) + 1:pos]
                    break
        if toInfo:
            features['toInfo'] = toInfo
       
        return features

if __name__ == "__main__":
    from email_handler import Email
    import sys
    
    for email_file in sys.argv[1:]:
        features = SimpleFeatures().features(Email(email_file))
        print "[EMAIL]:", email_file
        print "\t[FEATURES]:", features