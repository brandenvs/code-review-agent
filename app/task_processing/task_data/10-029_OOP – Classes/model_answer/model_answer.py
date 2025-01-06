# Email class
class Email:
    def __init__(self, email_address, subject_line, email_content, has_been_read=False):
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content
        self.has_been_read = has_been_read

    def mark_as_read(self):
        self.has_been_read = True
    
    def __str__(self) -> str:
        output = f'''
    From: {self.email_address}
    Subject: {self.subject_line}

    {self.email_content}
    '''
        return output

inbox = [] # List to store emails


def populate_inbox(email_address, subject_line, email_content):
    email = Email(email_address, subject_line, email_content)

    inbox.append(email) # Append email to inbox

    return inbox # return populated inbox


def list_emails(inbox: list[Email]):
    # Create email list
    email_list = {inbox.index(email): email.subject_line for email in inbox if email.has_been_read == False} # Ensures only unread emails are listed.

    # Print out each email ID and subject line respectively
    for id, email_subject in email_list.items():
        print(f'{id} {email_subject}')

    return len(email_list)


def get_email(id: int) -> Email | None:
    try:
        selected_email = [email for email in inbox if id == inbox.index(email)] # Get email based on ID
        return selected_email[0]

    except Exception as ex:
        print(ex)


def read_email(email: Email):
    # Build email string
    output = f'''
    From: {email.email_address}
    Subject: {email.subject_line}
    
    {email.email_content}
    '''
    print(output) # Print formatted email
    email.mark_as_read() # Mark as read

    return email


def main():
    # Populate inbox with a test emails
    populate_inbox('branden@gmail.com', 'Hello World!', 'Hello my name is Branden and this is a test email.')
    populate_inbox('john@doe.com', 'Best programmer in the world!', 'Hello my name is John and I am the best programmer in the world.')

    while True:
        menu = f'''Please select an option:
        1. Read an email
        2. View unread emails
        3. Quit Application
        '''
        print(menu)

        try:
            user_input = int(input('> '))

        except:
            print('Please select a valid option!')
            continue

        # Match user input with menu option
        match user_input:
            case 1:
                total_emails = list_emails(inbox)

                if total_emails > 0:
                    print('Input an email ID to read it.')

                    user_input = int(input('> '))
                    email = get_email(user_input)

                    if email:
                        read_email(email)

                else: 
                    print("You're all caught up!")

            case 2:
                list_emails(inbox)

            case 3:
                print('Goodbye!')
                exit()

            case _:
                print('Invalid option, try again!')

if __name__ == "__main__":
    main()
