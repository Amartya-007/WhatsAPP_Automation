# WhatsApp Automation Tool

A comprehensive Python application for sending WhatsApp messages using the Twilio API with advanced scheduling capabilities. Features both a powerful command-line interface and a beautiful modern GUI with blue and white theme.

## 🚀 Key Features

### Core Functionality

- **Send WhatsApp messages immediately** or schedule for future delivery
- **Dual interface options**: Command-line and modern GUI
- **Advanced scheduling system** with precise date/time control
- **Real-time status updates** and progress tracking
- **Robust error handling** with detailed feedback
- **Countdown timers** for scheduled messages
- **Cancel functionality** for pending scheduled messages

### Modern GUI Features

- **🎨 Beautiful blue and white theme** with professional appearance
- **📱 Scrollable interface** - works perfectly on any screen size
- **📅 Built-in date/time pickers** with intuitive dropdown menus
- **🔍 Smart validation** - prevents past dates, validates inputs in real-time
- **⚡ Quick time buttons** - "+5min", "+1hr", "Now" for instant scheduling
- **🖱️ User-friendly controls** with large, accessible buttons
- **📊 Progress tracking** with detailed activity logs
- **🎯 No external dependencies** - lightweight and fast
- **🔄 Threaded operations** - UI remains responsive during message sending
- **⚠️ Error recovery** - robust handling of network issues and API errors

### Technical Excellence

- **Environment variable support** for secure credential management
- **Input validation** with comprehensive error checking
- **Threading support** for non-blocking operations
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Modular code structure** for easy maintenance and extension

## 🛠️ Installation & Setup

### 📋 Prerequisites

1. **Python 3.7+**: Download from [python.org](https://python.org)
2. **Twilio Account**: Sign up at [twilio.com](https://twilio.com)
3. **WhatsApp Business Account**: For production use (sandbox for testing)

### ⚡ Quick Start

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd WhatsAPP_Automation
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Twilio credentials:

   ```env
   ACCOUNT_SID=your_account_sid_here
   AUTH_TOKEN=your_auth_token_here
   ```

4. **Launch the application**:

   ```bash
   # GUI Version (Recommended)
   python gui_main.py
   # or
   run_gui.bat
   
   # CLI Version
   python main.py
   # or
   run_cli.bat
   ```

### 📦 Dependencies

The application uses these Python packages:

- **customtkinter**: Modern UI framework for the GUI
- **twilio**: Official Twilio API client
- **python-dotenv**: Environment variable management
- **Pillow**: Image processing support for GUI

All dependencies are automatically installed with `pip install -r requirements.txt`

### 🔧 Twilio Setup Guide

1. **Create a Twilio Account**:
   - Sign up at [twilio.com](https://www.twilio.com)
   - Verify your phone number and email

2. **Get Your Credentials**:
   - Go to the [Twilio Console](https://console.twilio.com/)
   - Find your `Account SID` and `Auth Token` on the dashboard
   - Copy these to your `.env` file

3. **Set Up WhatsApp Sandbox**:
   - Navigate to Console → Messaging → Try it out → Send a WhatsApp message
   - Follow the instructions to join your sandbox
   - Note the sandbox phone number (usually +14155238886)
   - Send the join code from your WhatsApp to activate

4. **Test Your Setup**:
   - Run the application and send a test message to yourself
   - Both sender and recipient must join the sandbox for testing

### 3. WhatsApp Setup

Before sending messages, you need to:

1. Join the Twilio WhatsApp Sandbox by sending a message to the sandbox number
2. The recipient's phone number must also join the sandbox to receive messages

## 💻 Usage

### 🎨 GUI Version (Recommended)

Launch the beautiful modern interface:

```bash
python gui_main.py
```

**Or use the convenient batch file:**

```bash
run_gui.bat
```

**GUI Features & Benefits:**

- **🎨 Beautiful Blue & White Theme**: Professional appearance with light mode for comfortable viewing
- **📱 Responsive Design**: Scrollable interface that adapts to any screen size
- **📅 Intuitive Date/Time Selection**:
  - Year/Month/Day dropdown menus with smart validation
  - Hour/Minute pickers with 5-minute intervals
  - Quick time buttons for common scheduling (+5min, +1hr, Now)
  - Automatic past-date prevention
- **📝 User-Friendly Input**:
  - Clear section organization with emoji headers
  - Real-time input validation with helpful error messages
  - Large, accessible buttons and text fields
- **📊 Advanced Progress Tracking**:
  - Real-time status updates during message sending
  - Detailed activity log with timestamps
  - Cancel functionality for long operations
- **⚡ Smart Features**:
  - Threaded operations keep UI responsive
  - Automatic input validation
  - Error recovery and retry mechanisms

### 📟 Command Line Version

For automation and scripting:

```bash
python main.py
```

**Or use the batch file:**

```bash
run_cli.bat
```

### Input Requirements

The application will prompt you for:

1. Recipient's name
2. Recipient's WhatsApp number (format: +1234567890)
3. Message content
4. Whether to schedule the message or send immediately
5. If scheduling: date (YYYY-MM-DD) and time (HH:MM in 24-hour format)

## Example

```bash
WhatsApp Automation Tool
==============================
Enter the recipient's name: John
Enter the recipient's WhatsApp number (in the format +1234567890): +1234567890
Enter the message you want to send John: Hello! This is a test message.
Do you want to schedule this message? (y/n): y
Enter the date (YYYY-MM-DD): 2025-06-16
Enter the time (HH:MM) [24-hour format]: 15:30
Message will be sent to John in 3600 seconds.
Scheduled for: 2025-06-16 15:30
```

## Important Notes

1. **Sandbox Limitations**: In the Twilio sandbox, both sender and recipient must join the sandbox
2. **Time Format**: Use 24-hour format for time (e.g., 15:30 for 3:30 PM)
3. **Date Format**: Use YYYY-MM-DD format for dates
4. **Phone Numbers**: Include country code (e.g., +1 for US numbers)
5. **Production**: For production use, you need to request WhatsApp Business API approval from Twilio

## Troubleshooting

- **"Failed to send message"**: Check your Twilio credentials and ensure the recipient has joined the sandbox
- **"Invalid date/time format"**: Ensure you're using the correct date (YYYY-MM-DD) and time (HH:MM) formats
- **"The scheduled time is in the past"**: Enter a future date and time

## 📁 Project Structure

```text
WhatsAPP_Automation/
├── main.py                 # Command-line interface
├── gui_main.py            # Modern GUI with blue/white theme
├── gui_no_deps.py         # Backup GUI version
├── requirements.txt       # Python dependencies
├── run_gui.bat           # Windows batch file to launch GUI
├── run_cli.bat           # Windows batch file to launch CLI
├── .env                  # Environment variables (create this)
├── .env.example          # Template for environment variables
├── strp.py              # Utility script
└── README.md            # This documentation
```

### Key Files

- **`gui_main.py`**: Primary GUI application with scrollable blue/white theme
- **`main.py`**: Command-line interface for automation and scripting
- **`requirements.txt`**: Contains all necessary Python dependencies
- **Batch files**: Easy-to-use shortcuts for Windows users
- **`.env`**: Secure storage for your Twilio credentials (you create this)

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **"Failed to send message"** | Check Twilio credentials in `.env` file and ensure recipient joined sandbox |
| **"Invalid date/time format"** | Use YYYY-MM-DD for dates and HH:MM (24-hour) for times |
| **"The scheduled time is in the past"** | Select a future date and time |
| **GUI not loading** | Ensure `customtkinter` is installed: `pip install customtkinter` |
| **Threading errors** | Restart the application - this should be automatically handled |
| **"Connection error"** | Check internet connection and Twilio service status |

### 🛡️ Security Best Practices

- ✅ Never commit your `.env` file to version control
- ✅ Keep your Twilio credentials secure and private
- ✅ Use environment variables for sensitive data
- ✅ Regularly rotate your API tokens
- ✅ Monitor your Twilio usage and billing

### 🚀 Advanced Features

- **Batch Processing**: Extend the CLI for multiple recipients
- **Message Templates**: Save and reuse common messages
- **Delivery Reports**: Track message delivery status
- **Webhook Integration**: Receive delivery confirmations
- **Custom Themes**: Modify colors in the GUI code
- **API Integration**: Use as a library in other projects

## 📞 Support & Contributing

### Getting Help

1. **Check the troubleshooting section** above
2. **Review Twilio documentation** for API-specific issues
3. **Check the `.env` file** for correct credential format
4. **Test with the sandbox** before production use

### Contributing

Contributions are welcome! Areas for improvement:

- Additional GUI themes and customization
- Message templates and history
- Batch message processing
- Enhanced error handling
- Mobile app version
- Web interface
- Database integration for contact management

## 📄 License

This project is open source. Please ensure you comply with Twilio's terms of service when using their API.

## 🔗 Useful Links

- [Twilio WhatsApp API Documentation](https://www.twilio.com/docs/whatsapp)
- [CustomTkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)
- [Python dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Twilio Console](https://console.twilio.com/)
