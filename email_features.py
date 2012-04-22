from email_handler import Email

class EmailFeatures(object):
    
    def __init__(self):
        self.feature_extractors = []
    
    def add_feature_extractor(self, feature_extractor):
        self.feature_extractors.append(feature_extractor)
      
    def get_features_and_label(self, email_file):
        email = Email(email_file)
        if len(email.to_list) != 1:
            # print "[WARNING] Email {0} does not have a single recipient. Not generating any features".format(email_file)
            return None, None
        features = {}
        for feature_extractor in self.feature_extractors:
            cur_features = feature_extractor.features(email)
            if any(cur_key in features for cur_key in cur_features.keys()):
                raise RuntimeError, "Feature key produced by {0} is not unique".format(feature_extractor)
            features.update(cur_features)
        return features, email.to_list[0]
            

if __name__ == "__main__":
    from feature_extractors.simple_features import SimpleFeatures
    from feature_extractors.ne_features import NEFeatures
    from feature_extractors.tfidf_features import TFIDFFeatures
    import sys
    
    email_features = EmailFeatures()
    email_features.add_feature_extractor(SimpleFeatures())
    email_features.add_feature_extractor(NEFeatures())
    email_features.add_feature_extractor(TFIDFFeatures())
    
    for email_file in sys.argv[1:]:
        features, label = email_features.get_features_and_label(email_file)
        print "[EMAIL]:", email_file
        print "\t[FEATURES]:", features
        print "\t[LABEL]:", label
       
        
