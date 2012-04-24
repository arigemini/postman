from email_features import EmailFeatures
from feature_extractors.ne_features import NEFeatures
from feature_extractors.simple_features import SimpleFeatures
from feature_extractors.tfidf_features import TFIDFFeatures
import argparse
import os

class SnowInputGenerator(object):
       
    def generate(self, email_dirs, email_features, training_file, emails_file, id_mappings_file):
        self._init_state()
        email_counter, skipped_counter = 0, 0
        with open(training_file, 'w') as training_file_handle:
            with open(emails_file, 'w') as emails_file_handle:
                for email_dir in email_dirs:
                    print "Processing email dir: [{0}]".format(email_dir)
                    for email_file in filter(lambda cur: os.path.isfile(cur), map(lambda cur: os.path.join(email_dir, cur), os.listdir(email_dir))):
                        if (email_counter + skipped_counter) % 100 == 0:
                            print "{0} -> {1}".format(email_counter + skipped_counter, email_file)
                        # print "\tEmail: [{0}]".format(email_file)
                        features, label = email_features.get_features_and_label(email_file)
                        if not label or not features or len(features) == 0:
                            # print "\tSkipped email [{0}]. label [{1}] features [{2}]".format(email_file, label, features)
                            skipped_counter += 1
                            continue
                        email_counter += 1
                        print >> training_file_handle, self._get_training_line(label, features)
                        print >> emails_file_handle, email_file
        
        with open(id_mappings_file, 'w') as id_mappings_file_handle:
            for feature_id, feature_value in self.id_to_value.iteritems():
                print >> id_mappings_file_handle, "{0}: {1}".format(feature_id, feature_value)
        
        print "Total emails: {0} Used: {1} Skipped: {2}".format(email_counter + skipped_counter, email_counter, skipped_counter)
     
    def _init_state(self):
        self.label_to_id = dict()
        self.feature_to_id = dict()
        self.id_to_value = dict()
        self.next_id = 0      
                
    def _get_training_line(self, label, features):
        training_line = [self._get_label_id(label)]
        for feature_type, feature_values in features.iteritems():
            training_line.extend(self._get_feature_ids(feature_type, feature_values))
        return ",".join(training_line) + ":"
    
    def _get_label_id(self, label):
        if label not in self.label_to_id:
            self.label_to_id[label] = self.next_id
            self.id_to_value[self.next_id] = label
            self.next_id += 1
        return str(self.label_to_id[label])
    
    def _get_feature_ids(self, feature_type, feature_values):        
        ids = []   
        if feature_type in self.feature_to_id:
            assert type(self.feature_to_id[feature_type]) == dict
        else:
            self.feature_to_id[feature_type] = dict()
        if type(feature_values) not in [list, set]:
            feature_values = [feature_values]               
        for value in feature_values:
            assert type(value) == str or (type(value) == tuple and len(value) == 2)
            feature, strength = [value, None] if type(value) == str else [value[0], value[1]]
            
            if feature in self.feature_to_id[feature_type]:
                assert type(self.feature_to_id[feature_type][feature]) == int
            else:
                self.feature_to_id[feature_type][feature] = self.next_id
                self.id_to_value[self.next_id] = "[{0}] {1}".format(feature_type, feature)
                self.next_id = self.next_id + 1
            token = str(self.feature_to_id[feature_type][feature])
            token += "({0})".format(strength) if strength != None else ""
            ids.append(token)
            
        return ids
                                        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates files for training on snow")
    parser.add_argument("--email_dirs", required=True, nargs="+", help="Directories to scan for email files (non-recursive)")
    parser.add_argument("--tf_idf", action="store_true", help="Uses tf_idf of the words in the email as features")
    parser.add_argument("--named_entities", action="store_true", help="Use named entities as features. Have to pre-generate annotated email files.")
    parser.add_argument("--training_file", type=str, required=True, help="features file for snow")
    parser.add_argument("--emails_file", type=str, required=True, help="file to store the corresponding emails for the training file")
    parser.add_argument("--id_mappings_file", type=str, required=True, help="feature id to value mappings file")

    args = parser.parse_args()
    
    def original_to_annotated(original):
        return original.replace("training_input", "training_input_annotated") + "-annotated"
    
    email_features = EmailFeatures()
    email_features.add_feature_extractor(SimpleFeatures())
    if args.tf_idf:
        email_features.add_feature_extractor(TFIDFFeatures("etc/word_map_training.csv"))
    if args.named_entities:
        email_features.add_feature_extractor(NEFeatures(original_to_annotated))
    
    SnowInputGenerator().generate(args.email_dirs, email_features, args.training_file, args.emails_file, args.id_mappings_file)
    