# 📝 Todo App Tutorial

A simple, powerful todo list application with both command-line and web interfaces.

## 🚀 Quick Start (5 minutes)

### Install Python
First, make sure you have Python 3.11 or newer installed:
```bash
python --version  # Should show 3.11 or higher
```

### Setup Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate it (choose one):
source venv/bin/activate     # Mac/Linux
.\venv\Scripts\activate      # Windows
```

### Install Todo App
```bash
# Install all components
pip install -e todo-core/
pip install -e todo-cli/
pip install -e todo-api/
```

## 💻 Command Line Usage

The `todo` command provides a simple way to manage your tasks.

### Adding Tasks
```bash
todo add "Buy groceries"
todo add "Call mom"
todo add "Write report"
```

### Listing Tasks
```bash
todo list              # Show all tasks
todo list --pending    # Show only pending tasks
todo list --done      # Show completed tasks
```

### Completing Tasks
```bash
todo done 1    # Complete task #1
```

### Removing Tasks
```bash
todo rm 2      # Remove task #2
```

### Getting Help
```bash
todo --help    # Show all commands
todo add --help  # Show help for specific command
```

## 🌐 Web Interface

### Starting the Server
```bash
todo-api serve
```
Then open http://localhost:8000 in your browser.

### Using the Web Interface

1. **Add Tasks**
   - Type task in the input box
   - Click "Add Task" or press Enter

2. **Complete Tasks**
   - Click the circle next to a task
   - Click again to un-complete

3. **Delete Tasks**
   - Click the trash icon on the right

## 📱 Features

### Command Line
- ✨ Rich text output with colors
- 📊 List filtering (pending/completed)
- 🔍 Clear error messages
- 📚 Built-in help system

### Web Interface
- 🎯 Clean, minimal design
- ⚡ Fast updates with HTMX
- 🖱️ One-click actions
- 📱 Mobile-friendly

## 🤔 Common Questions

### Q: Where is my data stored?
All tasks are stored in `todo.db` in your current directory.

### Q: Can I back up my tasks?
Yes, just copy the `todo.db` file to a safe location.

### Q: What if I make a mistake?
Most commands can be undone:
- Accidentally completed? Just click/tap again
- Accidentally deleted? Add the task again

### Q: Can I run the web interface on a different port?
```bash
todo-api serve --port 3000
```

### Q: How do I stop the web server?
Press `Ctrl+C` in the terminal where it's running.

## 🛠️ Advanced Usage

### Command Line JSON Output
```bash
todo-core list --format json
```

### Custom Server Host
```bash
todo-api serve --host 0.0.0.0 --port 8080
```

### Development Mode
```bash
todo-api serve --reload  # Auto-reload on code changes
```

## 🆘 Getting Help

### Command Line Help
Every command has built-in help:
```bash
todo --help           # General help
todo list --help     # Help with list command
todo add --help      # Help with add command
todo done --help     # Help with done command
todo rm --help       # Help with remove command
```

### Web Interface Tips
- 💡 Hover over buttons to see what they do
- 🎯 Click tasks to see more options
- ⌨️ Use Enter key to add tasks quickly

## 🔜 Coming Soon
- 📅 Due dates
- 🏷️ Task priorities
- 📱 Mobile app
- 🔄 Task synchronization

## 💡 Tips and Tricks

### Command Line
1. Use tab completion for commands
2. Add aliases for common commands:
   ```bash
   # Add to your .bashrc or .zshrc:
   alias t="todo"
   alias ta="todo add"
   alias tl="todo list"
   ```

### Web Interface
1. Keep it open in a pinned tab
2. Use keyboard shortcuts:
   - Enter: Add task
   - Click circle: Complete task
   - Click trash: Delete task

## 🐛 Troubleshooting

### Common Issues

1. **"Command not found"**
   ```bash
   # Make sure you've:
   source venv/bin/activate  # Activated virtual environment
   pip install -e todo-cli/  # Installed the packages
   ```

2. **"Database error"**
   ```bash
   # Remove and let it recreate:
   rm todo.db
   ```

3. **"Port already in use"**
   ```bash
   # Use a different port:
   todo-api serve --port 3000
   ```

### Still Need Help?
- Check the error message carefully
- Make sure your Python version is 3.11+
- Try reinstalling the packages
- File an issue on GitHub

## 🎉 You're Ready!

Now you have both command-line and web interfaces to manage your tasks efficiently. Start with:

1. Add a few tasks:
   ```bash
   todo add "Try the todo app"
   todo add "Check the web interface"
   ```

2. Open the web interface:
   ```bash
   todo-api serve
   ```

3. Visit http://localhost:8000 and enjoy organizing your tasks!