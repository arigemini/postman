from email_handler import Email
import collections

class EmailFeatures(object):
 
    def __init__(self):
        self.types = {"ORG", "PER", "LOC"}
        pass
    
    def process_annotated_line(self, prefix, line):
        found = False
        found_idx = -1
        idx = -1
        for ch in line:
            idx += 1
            if found:
                if ch == "]":
                    if idx > found_idx + 3:
                        type_of = line[found_idx + 1:found_idx + 4]
                        if type_of in self.types:
                            self.features[prefix + "-" + type_of].append(line[found_idx + 4:idx].strip())
                    found = False
                elif ch == "[":
                    found_idx = idx
                    #"Found nested [ in annotated email file {0}".format(self.cur_email_file)
            if ch == "[":
                found = True
                found_idx = idx
    
    def get_features_from_annotated_file(self, email_file):
        self.cur_email_file = email_file
        
        self.features = collections.defaultdict(list)
        boundary = "-" * 10
        found_boundary = False
        with open(email_file + "-annotate-input-annotated", 'r') as f:
            for line in f:
                if found_boundary:
                    self.process_annotated_line("BODY", line)
                else:
                    idx = line.find(boundary)
                    if idx != -1:
                        self.process_annotated_line("SUBJECT", line[:idx])
                        self.process_annotated_line("BODY", line[idx + 10])
                        found_boundary = True
                    else:
                        self.process_annotated_line("SUBJECT", line)
                
        return self.features
    
    def get_features_and_labels(self, email_file):
        email = Email(email_file) 
        actual_message = email.remove_original_message
        features = {'from': email.from_, 'subject': email.subject}
        features['to'] = email.to_list[0] if email.to_list else []
        idx = actual_message.find('Thanks,')
        if idx != -1:
            features['senderInfo'] = actual_message[idx + 7:].strip()
        idx = actual_message.find('Hi ')
        if idx != -1 and actual_message[idx + 3].isupper():
            end = idx + 3
            while actual_message[end].isalpha():
                end += 1
            features['toInfo'] = actual_message[idx + 3: end]
        # features.update(self.get_features_from_annotated_file(email_file))
        labels = {'to': email.to_list[0]} if email.to_list else {'to': []}
        return features, labels

if __name__ == "__main__":
    feature_generator = EmailFeatures()
    features = feature_generator.get_features('/Users/arindam/workplace/CS499/enron_mail_20110402/maildir/allen-p/_sent_mail/427.')
    print features
       
        