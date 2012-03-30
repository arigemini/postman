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
    
    def generate(self, snow_input_file, feature_mappings_file):
        with open(snow_input_file, 'w') as file_handle:
            for email_file in self.email_files:
                features = self.feature_generator.get_features(email_file)
                print >> file_handle, self._get_feature_line(features)
        
        with open(feature_mappings_file, 'w') as file_handle:
            for feature_id, feature_name in self.id_to_feature.iteritems():
                print >> file_handle, str(feature_id) + ": " + feature_name
                
if __name__ == "__main__":
    feature_generator = EmailFeatures()
    files = glob.glob("/Users/arindam/workplace/CS499/enron_mail_20110402/maildir/allen-p/sent/*.")
    snow_input_generator = SnowInputGenerator(files, feature_generator)
    snow_input_generator.generate('training_set_for_snow.in', 'feature_id_to_string_mappings.txt')
    