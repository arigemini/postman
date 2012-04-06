from email_features import EmailFeatures
import glob

class SnowInputGenerator(object):
   
    def __init__(self, email_files, feature_generator):
        self.email_files = email_files
        self.feature_generator = feature_generator
        
        self.id_to_feature = dict()
        self.feature_to_id = dict()
        self.next_feature_id = 0
        
    def _get_feature_line(self, features):
        feature_line = []
        for feature_name, feature_values in features.iteritems():
            if type(feature_values) == int:
                if feature_name in self.feature_to_id:
                    assert type(self.feature_to_id[feature_name]) == int
                    feature_line.append(str(self.feature_to_id[feature_name]) + "(" + str(feature_values) + ")")
                else:
                    self.feature_to_id[feature_name] = self.next_feature_id
                    feature_line.append(str(self.next_feature_id) + "(" + feature_values + ")")
                    self.id_to_feature[self.next_feature_id] = feature_name
                    self.next_feature_id = self.next_feature_id + 1
            else:
                if type(feature_values) == str:
                    feature_values = [feature_values]
                if feature_name in self.feature_to_id:
                    assert type(self.feature_to_id[feature_name]) == dict
                else:
                    self.feature_to_id[feature_name] = dict()
                for value in feature_values:
                    if value in self.feature_to_id[feature_name]:
                        feature_line.append(str(self.feature_to_id[feature_name][value]))
                    else:
                        self.feature_to_id[feature_name][value] = self.next_feature_id
                        feature_line.append(str(self.next_feature_id))
                        self.id_to_feature[self.next_feature_id] = "[" + feature_name + "] " + value
                        self.next_feature_id = self.next_feature_id + 1
                        
        return ",".join(feature_line) + ":"
    
    def generate(self, snow_input_file, feature_mappings_file, labels_file):
        all_labels = []
        with open(snow_input_file, 'w') as file_handle:
            for email_file in self.email_files:
                features, labels = self.feature_generator.get_features_and_labels(email_file)
                all_labels.append(labels)
                print >> file_handle, self._get_feature_line(features)
        
        with open(labels_file, 'w') as file_handle:
            for label in all_labels:
                for label_name, values in label.iteritems():
                    if type(values) == str:
                        values = [values]
                    print >> file_handle, ", ".join([str(self.feature_to_id[label_name][value]) for value in values])
        
        with open(feature_mappings_file, 'w') as file_handle:
            for feature_id, feature_name in self.id_to_feature.iteritems():
                print >> file_handle, str(feature_id) + ": " + feature_name
                
if __name__ == "__main__":
    feature_generator = EmailFeatures()
    files = glob.glob("/Users/arindam/workplace/CS499/enron_mail_20110402/maildir/dasovich-j/inbox/*.")
    files.extend(glob.glob("/Users/arindam/workplace/CS499/enron_mail_20110402/maildir/sally-b/inbox/*."))
    files.extend(glob.glob("/Users/arindam/workplace/CS499/enron_mail_20110402/maildir/lay-k/inbox/*."))
    files.extend(glob.glob("/Users/arindam/workplace/CS499/enron_mail_20110402/maildir/jones-t/inbox/*."))
    files.extend(glob.glob("/Users/arindam/workplace/CS499/enron_mail_20110402/maildir/skilling-j/inbox/*."))
    snow_input_generator = SnowInputGenerator(files, feature_generator)
    snow_input_generator.generate('train.snow', 'feature_id_to_string_mappings.snow', 'labels.snow')
    