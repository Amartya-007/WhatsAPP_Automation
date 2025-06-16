import customtkinter as ctk
from twilio.rest import Client
from datetime import datetime, timedelta
import time
import dotenv
import os
import threading
from tkinter import messagebox
import re
import calendar

# Load environment variables from .env file
dotenv.load_dotenv()

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Constants
SEND_MESSAGE_TEXT = "Send Message"
SCHEDULE_MESSAGE_TEXT = "Schedule Message"
VALIDATION_ERROR_TITLE = "Validation Error"


class TwilioConnectionError(Exception):
    """Custom exception for Twilio connection issues"""
    pass


class WhatsAppGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("WhatsApp Automation Tool")
        self.root.geometry("700x900")  # Larger window to fit all content
        self.root.minsize(650, 850)  # Minimum size to ensure visibility
        self.root.resizable(True, True)
        
        # Twilio client
        self.client = None
        self.initialize_twilio()
        
        # Variables
        self.is_sending = False
        
        self.setup_ui()
        
    def initialize_twilio(self):
        """Initialize Twilio client with credentials from .env file"""
        account_sid = os.getenv("ACCOUNT_SID")
        auth_token = os.getenv("AUTH_TOKEN")
        
        if account_sid and auth_token:
            try:
                self.client = Client(account_sid, auth_token)
            except Exception as e:
                messagebox.showerror("Twilio Error", f"Failed to initialize Twilio client: {e}")
        else:
            messagebox.showwarning("Missing Credentials", 
                                 "Please set ACCOUNT_SID and AUTH_TOKEN in your .env file")
    
    def setup_ui(self):
        """Setup the user interface without external dependencies"""
        # Main title
        title_label = ctk.CTkLabel(
            self.root, 
            text="WhatsApp Automation Tool", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 15))
        
        # Main container frame (no scrolling)
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Setup all sections in main frame
        self.setup_recipient_section(main_frame)
        self.setup_message_section(main_frame)
        self.setup_scheduling_section(main_frame)
        self.setup_action_buttons(main_frame)
        self.setup_status_section(main_frame)
        
    def setup_recipient_section(self, parent):
        """Setup recipient information section"""
        recipient_frame = ctk.CTkFrame(parent)
        recipient_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            recipient_frame, 
            text="📱 Recipient Information", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Name input
        name_frame = ctk.CTkFrame(recipient_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(name_frame, text="Recipient Name:", width=140, anchor="w").pack(side="left")
        self.name_entry = ctk.CTkEntry(
            name_frame, 
            placeholder_text="Enter recipient's name",
            height=35
        )
        self.name_entry.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # Phone input
        phone_frame = ctk.CTkFrame(recipient_frame, fg_color="transparent")
        phone_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(phone_frame, text="Phone Number:", width=140, anchor="w").pack(side="left")
        self.phone_entry = ctk.CTkEntry(
            phone_frame, 
            placeholder_text="Enter phone number (e.g., +1234567890)",
            height=35
        )
        self.phone_entry.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
    def setup_message_section(self, parent):
        """Setup message input section"""
        message_frame = ctk.CTkFrame(parent)
        message_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            message_frame, 
            text="✉️ Message Content", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Message input with label
        msg_input_frame = ctk.CTkFrame(message_frame, fg_color="transparent")
        msg_input_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(msg_input_frame, text="Your Message:", anchor="w").pack(fill="x", pady=(0, 5))
        self.message_textbox = ctk.CTkTextbox(msg_input_frame, height=120)
        self.message_textbox.pack(fill="both", expand=True)
        
    def setup_scheduling_section(self, parent):
        """Setup message scheduling section with built-in date/time pickers"""
        scheduling_frame = ctk.CTkFrame(parent)
        scheduling_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            scheduling_frame, 
            text="⏰ Scheduling Options", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        self.schedule_var = ctk.StringVar(value="immediate")
        
        # Radio buttons
        radio_frame = ctk.CTkFrame(scheduling_frame, fg_color="transparent")
        radio_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.immediate_radio = ctk.CTkRadioButton(
            radio_frame, 
            text="Send Immediately", 
            variable=self.schedule_var, 
            value="immediate",
            command=self.on_schedule_change,
            font=ctk.CTkFont(size=14)
        )
        self.immediate_radio.pack(side="left", padx=(0, 30))
        
        self.schedule_radio = ctk.CTkRadioButton(
            radio_frame, 
            text="Schedule Message", 
            variable=self.schedule_var, 
            value="schedule",
            command=self.on_schedule_change,
            font=ctk.CTkFont(size=14)
        )
        self.schedule_radio.pack(side="left")
        
        # DateTime picker frame (initially hidden)
        self.datetime_frame = ctk.CTkFrame(scheduling_frame)
        
        # Date picker section using dropdowns
        date_section = ctk.CTkFrame(self.datetime_frame, fg_color="transparent")
        date_section.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(date_section, text="📅 Select Date:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        
        # Date picker frame
        date_picker_frame = ctk.CTkFrame(date_section, fg_color="transparent")
        date_picker_frame.pack(fill="x", pady=5)
        
        # Year picker
        year_frame = ctk.CTkFrame(date_picker_frame, fg_color="transparent")
        year_frame.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(year_frame, text="Year:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        current_year = datetime.now().year
        self.year_var = ctk.StringVar(value=str(current_year))
        self.year_optionmenu = ctk.CTkOptionMenu(
            year_frame,
            variable=self.year_var,
            values=[str(year) for year in range(current_year, current_year + 5)],
            width=80,
            command=self.update_days
        )
        self.year_optionmenu.pack()
        
        # Month picker
        month_frame = ctk.CTkFrame(date_picker_frame, fg_color="transparent")
        month_frame.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(month_frame, text="Month:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.month_var = ctk.StringVar(value=str(datetime.now().month).zfill(2))
        month_names = [f"{i:02d} - {calendar.month_name[i]}" for i in range(1, 13)]
        self.month_optionmenu = ctk.CTkOptionMenu(
            month_frame,
            variable=self.month_var,
            values=month_names,
            width=120,
            command=self.update_days
        )
        self.month_optionmenu.pack()
        
        # Day picker
        day_frame = ctk.CTkFrame(date_picker_frame, fg_color="transparent")
        day_frame.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(day_frame, text="Day:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.day_var = ctk.StringVar(value=str(datetime.now().day).zfill(2))
        self.day_optionmenu = ctk.CTkOptionMenu(
            day_frame,
            variable=self.day_var,
            values=[str(i).zfill(2) for i in range(1, 32)],
            width=60
        )
        self.day_optionmenu.pack()
        
        # Initialize days based on current month/year
        self.update_days()
        
        # Time picker section
        time_section = ctk.CTkFrame(self.datetime_frame, fg_color="transparent")
        time_section.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(time_section, text="🕐 Select Time:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        
        # Time picker frame
        time_picker_frame = ctk.CTkFrame(time_section, fg_color="transparent")
        time_picker_frame.pack(fill="x", pady=5)
        
        # Hour picker
        hour_frame = ctk.CTkFrame(time_picker_frame, fg_color="transparent")
        hour_frame.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(hour_frame, text="Hour:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.hour_var = ctk.StringVar(value=str((datetime.now() + timedelta(minutes=5)).hour).zfill(2))
        self.hour_optionmenu = ctk.CTkOptionMenu(
            hour_frame,
            variable=self.hour_var,
            values=[str(i).zfill(2) for i in range(24)],
            width=80
        )
        self.hour_optionmenu.pack()
        
        # Minute picker
        minute_frame = ctk.CTkFrame(time_picker_frame, fg_color="transparent")
        minute_frame.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(minute_frame, text="Minute:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.minute_var = ctk.StringVar(value=str((datetime.now() + timedelta(minutes=5)).minute).zfill(2))
        self.minute_optionmenu = ctk.CTkOptionMenu(
            minute_frame,
            variable=self.minute_var,
            values=[str(i).zfill(2) for i in range(0, 60, 5)],  # 5-minute intervals
            width=80
        )
        self.minute_optionmenu.pack()
        
        # Quick time buttons
        quick_time_frame = ctk.CTkFrame(time_picker_frame, fg_color="transparent")
        quick_time_frame.pack(side="left", padx=(20, 0))
        
        ctk.CTkLabel(quick_time_frame, text="Quick Set:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        
        quick_buttons_frame = ctk.CTkFrame(quick_time_frame, fg_color="transparent")
        quick_buttons_frame.pack(fill="x")
        
        ctk.CTkButton(quick_buttons_frame, text="+5min", width=60, height=25, 
                     command=lambda: self.set_quick_time(5)).pack(side="left", padx=2)
        ctk.CTkButton(quick_buttons_frame, text="+1hr", width=60, height=25,
                     command=lambda: self.set_quick_time(60)).pack(side="left", padx=2)
        ctk.CTkButton(quick_buttons_frame, text="Now", width=60, height=25,
                     command=lambda: self.set_quick_time(0)).pack(side="left", padx=2)
        
        # Initially hide datetime frame
        self.datetime_frame.pack_forget()
        
        # Add padding
        ctk.CTkLabel(scheduling_frame, text="").pack(pady=10)
    
    def update_days(self, *args):
        """Update available days based on selected month and year"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get().split(' - ')[0])
            
            # Get number of days in the month
            days_in_month = calendar.monthrange(year, month)[1]
            
            # Update day options
            day_values = [str(i).zfill(2) for i in range(1, days_in_month + 1)]
            self.day_optionmenu.configure(values=day_values)
            
            # Adjust current day if it's beyond the month's range
            current_day = int(self.day_var.get())
            if current_day > days_in_month:
                self.day_var.set(str(days_in_month).zfill(2))
                
        except (ValueError, AttributeError):
            pass  # Ignore errors during initialization
        
    def set_quick_time(self, minutes_from_now):
        """Set time quickly using buttons"""
        target_time = datetime.now() + timedelta(minutes=minutes_from_now)
        self.hour_var.set(str(target_time.hour).zfill(2))
        self.minute_var.set(str((target_time.minute // 5) * 5).zfill(2))  # Round to nearest 5 minutes
        
        # Also set date to today if setting current time
        if minutes_from_now <= 60:  # For quick times, set to today's date
            today = target_time.date()
            self.year_var.set(str(today.year))
            self.month_var.set(f"{today.month:02d} - {calendar.month_name[today.month]}")
            self.day_var.set(str(today.day).zfill(2))
            self.update_days()
        
    def setup_action_buttons(self, parent):
        """Setup action buttons"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Inner frame for buttons
        inner_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        inner_frame.pack(fill="x", padx=20, pady=20)
        
        self.send_button = ctk.CTkButton(
            inner_frame,
            text=SEND_MESSAGE_TEXT,
            command=self.send_message,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.send_button.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        self.clear_button = ctk.CTkButton(
            inner_frame,
            text="Clear All",
            command=self.clear_all,
            height=45,
            width=120,
            fg_color="gray",
            hover_color="darkgray",
            font=ctk.CTkFont(size=14)
        )
        self.clear_button.pack(side="right")
        
    def setup_status_section(self, parent):
        """Setup status display section"""
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            status_frame, 
            text="📊 Status & Progress", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Progress bar
        progress_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(progress_frame, text="Progress:", anchor="w").pack(fill="x", pady=(0, 5))
        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=20)
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)
        
        # Status text area
        status_text_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_text_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        ctk.CTkLabel(status_text_frame, text="Activity Log:", anchor="w").pack(fill="x", pady=(0, 5))
        self.status_textbox = ctk.CTkTextbox(status_text_frame, height=120, state="disabled")
        self.status_textbox.pack(fill="both", expand=True)
        
    def on_schedule_change(self):
        """Handle schedule option change"""
        if self.schedule_var.get() == "schedule":
            self.datetime_frame.pack(fill="x", padx=0, pady=(0, 15))
            self.send_button.configure(text=SCHEDULE_MESSAGE_TEXT)
        else:
            self.datetime_frame.pack_forget()
            self.send_button.configure(text=SEND_MESSAGE_TEXT)
    
    def validate_inputs(self):
        """Validate all user inputs"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        message = self.message_textbox.get("1.0", "end-1c").strip()
        
        if not name:
            messagebox.showerror(VALIDATION_ERROR_TITLE, "Please enter recipient's name")
            return False
            
        if not phone:
            messagebox.showerror(VALIDATION_ERROR_TITLE, "Please enter phone number")
            return False
            
        if not re.match(r'^\+\d{10,15}$', phone):
            messagebox.showerror(VALIDATION_ERROR_TITLE, 
                               "Please enter a valid phone number with country code (e.g., +1234567890)")
            return False
            
        if not message:
            messagebox.showerror(VALIDATION_ERROR_TITLE, "Please enter a message")
            return False
            
        if self.schedule_var.get() == "schedule":
            try:
                year = int(self.year_var.get())
                month = int(self.month_var.get().split(' - ')[0])
                day = int(self.day_var.get())
                hour = int(self.hour_var.get())
                minute = int(self.minute_var.get())
                
                scheduled_datetime = datetime(year, month, day, hour, minute)
                
                if scheduled_datetime <= datetime.now():
                    messagebox.showerror(VALIDATION_ERROR_TITLE, "Scheduled time must be in the future")
                    return False
                    
            except (ValueError, IndexError) as e:
                messagebox.showerror(VALIDATION_ERROR_TITLE, f"Invalid date/time selection: {str(e)}")
                return False
                
        return True
    
    def update_status(self, message):
        """Update status display"""
        self.status_textbox.configure(state="normal")
        self.status_textbox.insert("end", f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_textbox.configure(state="disabled")
        self.status_textbox.see("end")
        self.root.update_idletasks()
    
    def send_whatsapp_message(self, recipient, message):
        """Send WhatsApp message using Twilio"""
        try:
            if not self.client:
                raise TwilioConnectionError("Twilio client not initialized. Check your credentials.")
                
            message_obj = self.client.messages.create(
                from_='whatsapp:+14155238886',
                body=message,
                to=f'whatsapp:{recipient}'
            )
            return True, f"Message sent successfully! SID: {message_obj.sid}"
        except Exception as e:
            return False, f"Failed to send message: {str(e)}"
    
    def send_message_thread(self):
        """Thread function for sending messages"""
        try:
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            message = self.message_textbox.get("1.0", "end-1c").strip()
            
            if self.schedule_var.get() == "schedule":
                year = int(self.year_var.get())
                month = int(self.month_var.get().split(' - ')[0])
                day = int(self.day_var.get())
                hour = int(self.hour_var.get())
                minute = int(self.minute_var.get())
                
                scheduled_datetime = datetime(year, month, day, hour, minute)
                current_datetime = datetime.now()
                time_difference = scheduled_datetime - current_datetime
                delay_seconds = time_difference.total_seconds()
                
                self.update_status(f"Message scheduled for {name} at {scheduled_datetime.strftime('%Y-%m-%d %H:%M')}")
                self.update_status(f"Waiting {int(delay_seconds)} seconds...")
                
                # Countdown with progress bar
                for i in range(int(delay_seconds)):
                    if not self.is_sending:
                        self.update_status("Message sending cancelled")
                        return
                        
                    remaining = int(delay_seconds) - i
                    progress = i / delay_seconds
                    self.progress_bar.set(progress)
                    
                    if remaining % 60 == 0 or remaining <= 10:
                        self.update_status(f"Sending in {remaining} seconds...")
                    
                    time.sleep(1)
                
                self.progress_bar.set(1.0)
            
            # Send the message
            self.update_status(f"Sending message to {name}...")
            success, result = self.send_whatsapp_message(phone, message)
            
            if success:
                self.update_status(f"✅ {result}")
                messagebox.showinfo("Success", f"Message sent successfully to {name}!")
            else:
                self.update_status(f"❌ {result}")
                messagebox.showerror("Error", result)
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.update_status(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
        finally:
            # Reset UI
            self.is_sending = False
            button_text = SEND_MESSAGE_TEXT if self.schedule_var.get() == "immediate" else SCHEDULE_MESSAGE_TEXT
            self.send_button.configure(text=button_text)
            self.send_button.configure(state="normal")
            self.clear_button.configure(state="normal")
            self.progress_bar.set(0)
    
    def send_message(self):
        """Handle send message button click"""
        if not self.validate_inputs():
            return
            
        if self.is_sending:
            # Cancel sending
            self.is_sending = False
            self.update_status("Cancelling...")
            return
            
        # Start sending
        self.is_sending = True
        self.send_button.configure(text="Cancel", fg_color="red", hover_color="darkred")
        self.clear_button.configure(state="disabled")
        
        # Start thread for sending
        thread = threading.Thread(target=self.send_message_thread, daemon=True)
        thread.start()
    
    def clear_all(self):
        """Clear all input fields"""
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.message_textbox.delete("1.0", "end")
        
        # Reset date and time to default (5 minutes from now)
        future_time = datetime.now() + timedelta(minutes=5)
        self.year_var.set(str(future_time.year))
        self.month_var.set(f"{future_time.month:02d} - {calendar.month_name[future_time.month]}")
        self.day_var.set(str(future_time.day).zfill(2))
        self.hour_var.set(str(future_time.hour).zfill(2))
        self.minute_var.set(str((future_time.minute // 5) * 5).zfill(2))
        self.update_days()
        
        # Clear status
        self.status_textbox.configure(state="normal")
        self.status_textbox.delete("1.0", "end")
        self.status_textbox.configure(state="disabled")
        
        # Reset progress bar
        self.progress_bar.set(0)
        
        self.update_status("All fields cleared")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = WhatsAppGUI()
    app.run()
