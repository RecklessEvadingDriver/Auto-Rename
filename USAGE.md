# Usage Guide - Auto-Rename Bot

Complete guide on how to use all features of the Auto-Rename Bot.

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Basic File Renaming](#basic-file-renaming)
3. [Auto-Rename Format](#auto-rename-format)
4. [Custom Thumbnails](#custom-thumbnails)
5. [Custom Captions](#custom-captions)
6. [Sequence Mode](#sequence-mode)
7. [Metadata Settings](#metadata-settings)
8. [Admin Commands](#admin-commands)
9. [Tips & Tricks](#tips--tricks)

---

## 🚀 Getting Started

### First Steps
1. Start a chat with your bot
2. Send `/start` to initialize
3. The bot will register you and show the welcome message

### Quick Setup
Before using the bot, you might want to:
- Set a custom thumbnail (optional)
- Set a custom caption format (optional)
- Configure auto-rename format (optional)

---

## 📝 Basic File Renaming

### Simple Rename
1. Send any file to the bot
2. Bot will ask for new filename
3. Reply with the new name (include extension)
4. Bot will process and send renamed file

**Example:**
```
You: [Send video.mp4]
Bot: Send me the new filename
You: My Movie 2024.mp4
Bot: [Sends renamed file]
```

---

## 🎯 Auto-Rename Format

Set up automatic renaming with custom format and variables.

### Setting Format
Command: `/autorename <format>`

### Available Variables
- `{episode}` or `{Episode}` - Episode number
- `{quality}` or `{Quality}` - Video quality (720p, 1080p, etc.)
- `{season}` or `{Season}` - Season number
- `{audio}` or `{Audio}` - Audio language/codec

### Examples

#### Anime Format
```
/autorename Demon Slayer [S{season}] [EP{episode}] [{quality}] [{audio}] @MyChannel
```

Result: `Demon Slayer [S01] [EP05] [1080p] [Hindi] @MyChannel.mkv`

#### Series Format
```
/autorename Breaking Bad S{season}E{episode} {quality} @MyChannel
```

Result: `Breaking Bad S01E05 720p @MyChannel.mp4`

#### Movie Format
```
/autorename Inception (2010) {quality} {audio} @MyChannel
```

Result: `Inception (2010) 1080p English @MyChannel.mkv`

### View Your Format
- `/showformat` - See your current auto-rename format

---

## 🖼️ Custom Thumbnails

Add custom thumbnails to your renamed files.

### Set Thumbnail
1. Send any photo to the bot
2. Bot automatically sets it as your thumbnail

### View Thumbnail
- `/viewthumb` - See your current thumbnail

### Delete Thumbnail
- `/delthumb` - Remove your custom thumbnail
- Bot will use original file thumbnail if no custom one is set

---

## 💬 Custom Captions

Add branded captions to your files.

### Setting Caption
Command: `/set_caption <your caption text>`

### Available Variables
- `{filename}` - File name
- `{filesize}` - File size
- `{duration}` - Video duration (if applicable)

### Example
```
/set_caption 📁 File: {filename}
📊 Size: {filesize}
⏱️ Duration: {duration}

© @MyChannel
```

### View Caption
- `/see_caption` - See your current caption

### Delete Caption
- `/del_caption` - Remove your custom caption

---

## 🔢 Sequence Mode

Rename multiple files in sequence automatically.

### How It Works
1. Start sequence: `/start_sequence`
2. Send multiple files one by one
3. Files are renamed with auto-incrementing numbers
4. End sequence: `/end_sequence`

### Example
```
You: /start_sequence
Bot: Sequence mode started! Send files one by one.

You: [Send file 1]
Bot: Added to sequence (1/∞)

You: [Send file 2]
Bot: Added to sequence (2/∞)

You: [Send file 3]
Bot: Added to sequence (3/∞)

You: /end_sequence
Bot: Processing 3 files...
[Sends all renamed files in order]
```

---

## 🎬 Metadata Settings

Control video metadata (title, author, etc.)

### View Settings
- `/metadata` - See current metadata settings

### Set Metadata
The bot will ask for:
- Title
- Author
- Artist
- Audio
- Subtitle
- Video
- Encoded by

### Toggle Metadata
Enable or disable metadata modification from the settings menu.

---

## 👑 Admin Commands

Commands for bot administrators.

### User Management
- `/ban <user_id>` - Ban a user
- `/unban <user_id>` - Unban a user
- `/banned` - List banned users

### Premium Management
- `/add_premium <user_id> <days>` - Add premium access
- `/remove_premium <user_id>` - Remove premium access
- `/premium_users` - List premium users
- `/premium_info <user_id>` - Get premium user info

### Channel Management (Force Subscribe)
- `/addchnl <channel_id>` - Add force subscribe channel
- `/delchnl <channel_id>` - Remove force subscribe channel
- `/listchnl` - List all force subscribe channels
- `/fsub_mode` - Toggle force subscribe mode

### Admin Management
- `/add_admin <user_id>` - Add new admin
- `/deladmin <user_id>` - Remove admin
- `/admins` - List all admins

### Verification Settings
- `/verify_settings` - Configure verification system

### System Commands
- `/status` - Check bot status and statistics
- `/restart` - Restart the bot
- `/broadcast <message>` - Broadcast message to all users

---

## 💡 Tips & Tricks

### Best Practices

1. **Use Consistent Formats**
   - Stick to one format for similar content
   - Makes organization easier

2. **Include Your Channel**
   - Add your channel username in format/caption
   - Free promotion with every file

3. **Test First**
   - Test new formats with one file
   - Verify before batch processing

4. **Quality Tags**
   - Always include quality tags
   - Users appreciate knowing resolution

### Optimization Tips

1. **File Size Limits**
   - Maximum file size: 2GB
   - Larger files will be rejected

2. **Processing Speed**
   - Smaller files process faster
   - Be patient with large files

3. **Concurrent Operations**
   - Bot can handle multiple users
   - Your own operations are queued

### Advanced Usage

#### Combining Features
```
1. Set auto-rename format
2. Set custom thumbnail
3. Set custom caption
4. Use sequence mode

Result: Perfectly branded batch of files!
```

#### For Channels
```
1. Set channel branding in format
2. Add watermark thumbnail
3. Include channel link in caption
4. Use force subscribe

Result: Professional content distribution!
```

---

## 🆘 Troubleshooting

### Common Issues

**Bot not responding:**
- Check if bot is online
- Try /start command
- Contact admin

**File not renaming:**
- Check file size (max 2GB)
- Verify format is correct
- Ensure variables are spelled correctly

**Thumbnail not applying:**
- Make sure you sent a photo
- Check if thumbnail was confirmed
- Try setting again

**Caption not showing:**
- Verify variables are correct
- Check caption with /see_caption
- Try setting again

---

## 📞 Support

Need help?
- Check this guide first
- Use `/help` command
- Contact bot admin
- Join support group

---

## 🎉 Happy Renaming!

Enjoy using the Auto-Rename Bot! For more features and updates, stay connected with the official channel.

**Remember:** The more you use the bot, the better you'll understand its powerful features!
