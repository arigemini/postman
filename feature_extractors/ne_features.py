import re

class NEFeatures(object):
        
    def __init__(self, email_to_annotated_func):
        self.email_to_annotated_func = email_to_annotated_func
        self.regex = re.compile("\[(ORG|PER|LOC|MISC)\s([^\]]*)]")
        pass
    
    def features(self, email):
        features = {}
        annotated_file = self.email_to_annotated_func(email.filepath)
        with open(annotated_file, 'r') as f:
            for line in f:
                for category, value in self.regex.findall(line):
                    features.setdefault(category, set()).add(value.strip())
        return features
    
if __name__ == "__main__":
    from email_handler import Email
    import sys
    
    def original_to_annotated(email_file):
        return email_file.replace("training_input", "training_input_annotated") + "-annotated"
    
    for email_file in sys.argv[1:]:
        features = NEFeatures(original_to_annotated).features(Email(email_file))
        print "[EMAIL]:", email_file
        print "\t[FEATURES]:", features