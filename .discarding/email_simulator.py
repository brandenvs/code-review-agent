class Email:
    def __init__(self, sender, subject, content):
        # Initialize an email object with sender, subject, content, and read status.
        self.sender = sender
        self.subject = subject
        self.content = content
        # default status is unread
        self.read = False  
    def mark_as_read(self):
        # Mark the email as read.
        self.read = True

    def __str__(self):
        # Return a string reprsentation of the email with sender subject read status.
        return f"From: {self.sender}\nSubject: {self.subject}\nRead: {'Yes' if self.read else 'No'}"


class EmailSimulator:
    def __init__(self):

        # Initialize the email simlator with an empty inbox.
        self.inbox = []

    def add_email(self, sender, subject, content):
        # Ad a new email to the inbox.
        email = Email(sender, subject, content)
        self.inbox.append(email)

    def list_all_emails(self):
        # List all emails in the inbox with their detail.
        if not self.inbox:
            # Inform the user if no email are in the inbox.
            print("\nYour inbox is empty.")  
            return
        print("\n--- All Emails ---")
        # Enumerate emails starting from 1.
        for idx, email in enumerate(self.inbox, 1):  
            print(f"{idx}. {email}")

    def read_email(self, email_number):
    
        # Ensure the input is within the vaid range.
        if 0 < email_number <= len(self.inbox):  
            email = self.inbox[email_number - 1]
            # mark the email as read.
            email.mark_as_read()  
            # Display email content.
            print(f"\n--- Email Content ---\n{email.content}")  
        else:
            # Handle invalid input
            print("\nInvalid email number.")  

    def view_unread_emails(self):
        # List all unrad emails in the inbox.
        unread_emails = [email for email in self.inbox if not email.read]
        if not unread_emails:
            # inform the user if all emals are read.
            print("\nNo unread emails.")  
            return
        print("\n--- Unread Emails ---")
        # enumerate unread emails starting from 1.
        for idx, email in enumerate(unread_emails, 1):  
            print(f"{idx}. {email}")

    def run(self):
        # Display a menu to the user for intracting with the email simulator.
        print("\nWelcome to the Email Simulator!")
        while True:
            # Display the menu options.
            print("\n--- Email Simulator Menu ---")
            print("1. List all emails")
            print("2. Read an email")
            print("3. View unread emails")
            print("4. Quit")
            choice = input("Choose an option (1-4): ")

            if choice == "1":
                # List all emails.
                self.list_all_emails()  
            elif choice == "2":
                try:
                    email_number = int(input("Enter the email number to read: "))
                    # read the specified email
                    self.read_email(email_number)  
                except ValueError:
                    # Handle non-integer input
                    print("\nInvalid input. Please enter a number.")  
            elif choice == "3":
                 # View unred emails
                self.view_unread_emails() 
            elif choice == "4":
                # Exit the code
                print("\nExiting the Email Simulator. Goodbye!")  
                break
            else:
                # Handle invalid menu choices
                print("\nInvalid choice. Please try again.")


# Example Emails to Test
def main():
    # Initialize the simlator, add example emails,  start the program.
    simulator = EmailSimulator()
    # Add some example emails.
    simulator.add_email("alice@example.com", "Meeting Reminder", "Don't forget our meeting tomorrow at 10 AM.")
    simulator.add_email("bob@example.com", "Weekend Plans", "Are you free this weekend for a hike?")
    simulator.add_email("charlie@example.com", "Project Update", "The project deadline has been extended to next Friday.")
    # Start the simultor.
    simulator.run()  


if __name__ == "__main__":
    main()  # Run the code


