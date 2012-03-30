from email_handler import Email


class EmailFeatures(object):
 
    def __init__(self):
        pass
        
    def get_features(self, email_file):
        email = Email(email_file) 
        actual_message = email.remove_original_message
        features = {'from': email.from_, 'to': email.to_list, 'subject': email.subject}
        idx = actual_message.find('Thanks,')
        if idx != -1:
            features['senderInfo'] = actual_message[idx + 7:].strip()
        idx = actual_message.find('Hi ')
        if idx != -1 and actual_message[idx + 3].isupper():
            end = idx + 3
            while actual_message[end].isalpha():
                end += 1
            features['toInfo'] = actual_message[idx + 3: end]
        
        return features

if __name__ == "__main__":
    feature_generator = EmailFeatures()
    features = feature_generator.get_features('/Users/arindam/workplace/CS499/enron_mail_20110402/maildir/allen-p/_sent_mail/427.')
    print features
       
        