class SimpleFeatures(object):
    def __init__(self):
        pass
    
    def features(self, email):
        features = {'from': email.from_, 'subject': email.subject}
        actual_message = email.actual_message
        
        # Thanks Regards Best
        idx = actual_message.find('Thanks,')
        if idx != -1:
            features['senderInfo'] = actual_message[idx + 7:].strip()
        # Hi Hello Dear *, *\n
        idx = actual_message.find('Hi ')
        if idx != -1 and actual_message[idx + 3].isupper():
            end = idx + 3
            while actual_message[end].isalpha():
                end += 1
            features['toInfo'] = actual_message[idx + 3: end]
        return features

if __name__ == "__main__":
    from email_handler import Email
    import sys
    
    for email_file in sys.argv[1:]:
        features = SimpleFeatures().features(Email(email_file))
        print "[EMAIL]:", email_file
        print "\t[FEATURES]:", features