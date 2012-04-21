from email_features import EmailFeatures
import os

class SnowInputGenerator(object):
   
    def __init__(self, email_dirs, feature_generator):
        self.email_dirs = email_dirs
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
    
    def generate(self, features_file, feature_mappings_file, labels_file, emails_file):
        all_labels = []
        with open(features_file, 'w') as features_file_handle:
            with open(labels_file, 'w') as labels_file_handle:
                with open(emails_file, 'w') as emails_file_handle:
                    for email_dir in self.email_dirs:
                        print "Processing email dir", email_dir
                        for email_file in filter(lambda cur: os.path.isfile(cur), map(lambda cur: os.path.join(email_dir, cur), os.listdir(email_dir))):
                            print "\t", email_file
                            features, labels = self.feature_generator.get_features_and_labels(email_file)
                            if not features:
                                print "Skipped", email_file
                                continue
                            print >> features_file_handle, self._get_feature_line(features)
                            print >> emails_file_handle, email_file
                            for label_name, values in labels.iteritems():
                                if type(values) == str:
                                    values = [values]
                                print >> labels_file_handle, ", ".join([str(self.feature_to_id[label_name][value]) for value in values])
        
        with open(feature_mappings_file, 'w') as file_handle:
            for feature_id, feature_name in self.id_to_feature.iteritems():
                print >> file_handle, str(feature_id) + ": " + feature_name
                
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generates files for training on snow")
    parser.add_argument("--named_entities", action="store_true", help="Use named entities as features. Have to pre-generate annotated email files.")
    parser.add_argument("--tf_idf", action="store_true", help="Uses tf_idf of the words in the email as features")
    parser.add_argument("--features_file", type=str, required=True, help="features file for snow")
    parser.add_argument("--feature_mappings_file", type=str, required=True, help="feature id to value mappings file")
    parser.add_argument("--labels_file", type=str, required=True, help="file to store the labels for the corresponding training file")
    parser.add_argument("--emails_file", type=str, required=True, help="file to store the corresponding emails for the training file")
    parser.add_argument("--email_dirs", required=True, nargs="+", help="Directories to scan for email files (non-recursive)")
    args = parser.parse_args()
    
    feature_generator = EmailFeatures(args.named_entities, args.tf_idf)
    snow_input_generator = SnowInputGenerator(args.email_dirs, feature_generator)
    snow_input_generator.generate(args.features_file, args.feature_mappings_file, args.labels_file, args.emails_file)
    