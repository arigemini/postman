from email_handler import Email

def generate_annotate_input(email_file):
    email = Email(email_file)
    actual_message = email.remove_original_message
    with open(email_file + '-annotate-input', 'w') as f:
        print >> f, email.subject
        print >> f, "body"
        print >> f, actual_message

if __name__ == "__main__":
    import sys
    for email_file in sys.argv[1:]:
        generate_annotate_input(email_file)
       
        