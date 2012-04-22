import collections

class NEFeatures(object):
    def __init__(self):
        self.types = {"ORG", "PER", "LOC", "MISC"}
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
    
    def features(self, email):
        raise NotImplementedError