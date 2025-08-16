# 🎭 Enhanced Calendar CLI - Vintage Event Edition

Your all-in-one solution for discovering vintage events and managing your calendar! This CLI combines vintage event search with intelligent calendar management, allowing you to find events, check availability, and schedule them seamlessly.

## ✨ Features

### 🔍 **Event Discovery**

- **Smart Search**: Find vintage events using natural language queries
- **Location-Based**: Discover events near you or in specific areas
- **Event Types**: Search for markets, fairs, popups, and more
- **Real-Time Results**: Get up-to-date event information

### 📅 **Calendar Management**

- **Google Calendar Integration**: Full sync with your Google Calendar
- **Availability Checking**: See when you're free and when you have conflicts
- **Smart Scheduling**: Automatically check for conflicts before adding events
- **Multi-Calendar Support**: Work with all your calendars

### 💡 **Intelligent Planning**

- **Conflict Detection**: Avoid double-booking with automatic conflict checking
- **Free Time Analysis**: Find available time slots throughout your day
- **Smart Suggestions**: Get recommendations for optimal scheduling
- **Event Integration**: Seamlessly add found events to your calendar

## 🚀 Quick Start

### 1. **Check Authentication**

```bash
python enhanced_calendar_cli.py auth
```

### 2. **Search for Vintage Events**

```bash
python enhanced_calendar_cli.py search "vintage markets near brooklyn"
```

### 3. **Check Your Availability**

```bash
python enhanced_calendar_cli.py free 2025-08-20
```

### 4. **Add Events to Calendar**

```bash
python enhanced_calendar_cli.py add "Vintage Market" 2025-08-20 "14:00" 180
```

## 📚 Complete Command Reference

### 🔍 **Search & Discovery Commands**

#### `search <query>`

Search for events using natural language:

```bash
python enhanced_calendar_cli.py search "vintage popup shops this weekend"
python enhanced_calendar_cli.py search "antique fairs manhattan"
python enhanced_calendar_cli.py search "vintage clothing markets brooklyn"
```

#### `find <event_type> <location>`

Find specific types of events in a location:

```bash
python enhanced_calendar_cli.py find "vintage markets" "brooklyn"
python enhanced_calendar_cli.py find "antique fairs" "manhattan"
python enhanced_calendar_cli.py find "popup shops" "queens"
```

#### `nearby <location>`

Find events in a specific area:

```bash
python enhanced_calendar_cli.py nearby "downtown brooklyn"
python enhanced_calendar_cli.py nearby "chelsea manhattan"
python enhanced_calendar_cli.py nearby "astoria queens"
```

### 📅 **Calendar Management Commands**

#### `auth`

Check Google Calendar authentication status:

```bash
python enhanced_calendar_cli.py auth
```

#### `calendars`

List all accessible calendars:

```bash
python enhanced_calendar_cli.py calendars
```

#### `events [days]`

List upcoming events (default: 7 days):

```bash
python enhanced_calendar_cli.py events
python enhanced_calendar_cli.py events 14  # Next 14 days
```

#### `free <date>`

Show when you're free on a specific date:

```bash
python enhanced_calendar_cli.py free 2025-08-20
python enhanced_calendar_cli.py free 2025-08-25
```

#### `conflicts <date> <time> <duration>`

Check for scheduling conflicts:

```bash
python enhanced_calendar_cli.py conflicts 2025-08-20 "14:00" 120
```

### ➕ **Event Scheduling Commands**

#### `add <title> <date> <time> <duration>`

Add a new event to your calendar:

```bash
python enhanced_calendar_cli.py add "Vintage Market" 2025-08-20 "14:00" 180
python enhanced_calendar_cli.py add "Antique Fair" 2025-08-22 "10:00" 240
```

#### `schedule <event_id> <date> <time>`

Schedule a previously found event:

```bash
# First search for events
python enhanced_calendar_cli.py search "vintage markets"

# Then schedule one of the found events
python enhanced_calendar_cli.py schedule 1 2025-08-20 "14:00"
```

### 💡 **Smart Features**

#### `plan <query>`

Smart planning that combines search and calendar:

```bash
python enhanced_calendar_cli.py plan "vintage markets this weekend"
python enhanced_calendar_cli.py plan "antique fairs next week"
```

## 🎯 **Real-World Examples**

### **Scenario 1: Planning a Vintage Shopping Day**

```bash
# 1. Search for vintage events
python enhanced_calendar_cli.py search "vintage markets antique fairs brooklyn"

# 2. Check your availability
python enhanced_calendar_cli.py free 2025-08-20

# 3. Add events to your calendar
python enhanced_calendar_cli.py add "Brooklyn Vintage Market" 2025-08-20 "10:00" 180
python enhanced_calendar_cli.py add "Antique Fair" 2025-08-20 "14:00" 120
```

### **Scenario 2: Finding Weekend Activities**

```bash
# 1. Smart planning for the weekend
python enhanced_calendar_cli.py plan "vintage popup shops this weekend"

# 2. Check conflicts before scheduling
python enhanced_calendar_cli.py conflicts 2025-08-23 "15:00" 90

# 3. Schedule if no conflicts
python enhanced_calendar_cli.py add "Weekend Popup" 2025-08-23 "15:00" 90
```

### **Scenario 3: Exploring New Areas**

```bash
# 1. Find events in a new area
python enhanced_calendar_cli.py nearby "chelsea manhattan"

# 2. Check your schedule for the day
python enhanced_calendar_cli.py free 2025-08-25

# 3. Schedule exploration time
python enhanced_calendar_cli.py add "Chelsea Vintage Exploration" 2025-08-25 "13:00" 240
```

## 🔧 **Configuration & Setup**

### **Google Calendar Authentication**

The CLI automatically handles OAuth2 authentication:

1. First run will open a browser for authorization
2. Tokens are cached locally for future use
3. Automatic token refresh when needed

### **Event Search Sources**

- **Exa Search**: Real-time web search for events
- **Location Intelligence**: Smart parsing of NYC areas
- **Event Categorization**: Automatic classification of event types

## 📱 **Advanced Usage Tips**

### **Natural Language Queries**

The search is designed to understand natural language:

- ✅ "vintage markets near me"
- ✅ "antique fairs this weekend"
- ✅ "vintage popup shops in brooklyn"
- ✅ "vintage clothing markets manhattan"

### **Date and Time Formats**

- **Date**: YYYY-MM-DD (e.g., 2025-08-20)
- **Time**: HH:MM (e.g., 14:00 for 2:00 PM)
- **Duration**: Minutes (e.g., 180 for 3 hours)

### **Conflict Resolution**

The CLI automatically:

- Detects scheduling conflicts
- Shows available alternatives
- Asks for confirmation before overriding
- Suggests optimal time slots

## 🚨 **Troubleshooting**

### **Authentication Issues**

```bash
# Check auth status
python enhanced_calendar_cli.py auth

# If failed, re-run the setup
python setup_python_calendar.py
```

### **Search Issues**

```bash
# Try more specific queries
python enhanced_calendar_cli.py search "vintage markets brooklyn august 2025"

# Use the find command for specific types
python enhanced_calendar_cli.py find "vintage markets" "brooklyn"
```

### **Calendar Issues**

```bash
# Check your calendars
python enhanced_calendar_cli.py calendars

# Verify events are syncing
python enhanced_calendar_cli.py events 1
```

## 🎉 **What You Can Do Now**

1. **Discover Events**: Find vintage markets, antique fairs, and popup shops
2. **Check Availability**: See when you're free and when you have conflicts
3. **Smart Scheduling**: Add events with automatic conflict detection
4. **Plan Ahead**: Use smart planning to combine search and calendar
5. **Stay Organized**: Keep track of all your vintage adventures

## 🔮 **Future Enhancements**

- Weather integration for outdoor events
- Travel time calculations
- Event recommendations based on preferences
- Social sharing of events
- Integration with other calendar services

---

**Ready to discover amazing vintage events and organize your calendar? Start with:**

```bash
python enhanced_calendar_cli.py help
```
