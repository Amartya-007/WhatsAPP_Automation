from twilio.rest import Client
from datetime import datetime, timedelta
import time
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()

# Twilio credentials
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)


# send Whatsapp message
def send_whatsapp_message(recipient, message):
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio sandbox number
            body=message,
            to=f'whatsapp:{recipient}'
        )
        print(f"Message sent to {recipient}: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")



# Ask user for the recipient's Name & phone number & message to recipient
def get_recipient_info():
    name = input("Enter the recipient's name: ")
    recipient_number = input("Enter the recipient's WhatsApp number (in the format +1234567890): ")
    message = input(f"Enter the message you want to send {name}: ")
    return name, recipient_number, message

# parse the date & time and calculate the delay
def schedule_message(name, recipient_number, message):
    date_str = input("Enter the date (YYYY-MM-DD): ") #2023-10-01
    time_str = input("Enter the time (HH:MM) [24-hour format]: ")
    
    try:        # datetime object
        scheduled_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()
        
        # Calculate the delay in seconds
        time_difference = scheduled_datetime - current_datetime
        delay_seconds = time_difference.total_seconds()

        if delay_seconds <= 0:
            print("The scheduled time is in the past. Please enter a future date and time.")
            return False
        else:
            print(f"Message will be sent to {name} in {delay_seconds:.0f} seconds.")
            print(f"Scheduled for: {scheduled_datetime.strftime('%Y-%m-%d %H:%M')}")
            time.sleep(delay_seconds)
            send_whatsapp_message(recipient_number, message)
            return True
    except ValueError:
        print("Invalid date/time format. Please use YYYY-MM-DD for date and HH:MM for time.")
        return False

# Main execution function
def main():
    print("WhatsApp Automation Tool")
    print("=" * 30)
    
    # Get recipient information
    name, recipient_number, message = get_recipient_info()
    
    # Ask if user wants to schedule the message
    schedule_choice = input("Do you want to schedule this message? (y/n): ").lower().strip()
    
    if schedule_choice == 'y' or schedule_choice == 'yes':
        # Schedule the message
        success = schedule_message(name, recipient_number, message)
        if not success:
            print("Failed to schedule message. Please try again.")
    else:
        # Send immediately
        send_whatsapp_message(recipient_number, message)

if __name__ == "__main__":
    main()


