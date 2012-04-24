import collections
import string

class TFIDFFeatures(object):
    
    THRESHOLD = 0.003
    
    def __init__(self, word_map_csv_file):
        self.freq = {}
        with open(word_map_csv_file, 'r') as f:
            for line in f:
                splits = line.strip().split(',')
                self.freq[",".join(splits[1:])] = int(splits[0])
    
    def features(self, email):
        features = {"words": []}
        word_map = collections.defaultdict(int)
               
        for word in email.actual_message.split():
            word = word.strip(string.punctuation).lower()
            if word:
                word_map[word] += 1
                        
        for word, counter in word_map.iteritems():
            if word not in self.freq or (float(counter) / self.freq[word]) > TFIDFFeatures.THRESHOLD:
                features["words"].append(word)
                
        return features
    
if __name__ == "__main__":
    from email_handler import Email
    import sys
    
    if len(sys.argv) < 3:
        print "usage: python", __file__, "<word_map_csv_file> <email> [<email>, ...]"
        exit()
        
    for email_file in sys.argv[2:]:
        features = TFIDFFeatures(sys.argv[1]).features(Email(email_file))
        print "[EMAIL]:", email_file
        print "\t[FEATURES]:", features