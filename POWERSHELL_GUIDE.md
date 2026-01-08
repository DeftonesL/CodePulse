# PowerShell Quick Start Guide

## Running CodePulse in PowerShell

### Important Note
PowerShell requires `.\` before scripts in the current directory for security reasons.

---

## Basic Usage

```powershell
# Navigate to CodePulse directory
cd C:\Users\xsll7\Desktop\CodePulse

# Run scanner
.\codepulse.bat C:\Users\xsll7\Desktop\discord

# With options
.\codepulse.bat C:\Projects\MyApp --workers 8
.\codepulse.bat .\src --no-cache
```

---

## Common Commands

### Scan a Project
```powershell
.\codepulse.bat C:\path\to\project
```

### Scan with 8 Workers
```powershell
.\codepulse.bat C:\path\to\project --workers 8
```

### Clear Cache and Scan
```powershell
.\codepulse.bat C:\path\to\project --clear-cache
```

### Full Scan (No Incremental)
```powershell
.\codepulse.bat C:\path\to\project --no-incremental
```

### Disable Cache
```powershell
.\codepulse.bat C:\path\to\project --no-cache
```

### Scan Specific File Type
```powershell
.\codepulse.bat C:\path\to\project --pattern "*.js"
```

---

## Alternative: Direct Python

If you prefer not to use the batch file:

```powershell
python fast_scan.py C:\path\to\project
python fast_scan.py C:\path\to\project --workers 8
python fast_scan.py C:\path\to\project --no-cache
```

---

## Troubleshooting

### Error: "codepulse.bat is not recognized"
**Solution:** Add `.\` before the command
```powershell
# Wrong
codepulse.bat C:\project

# Correct
.\codepulse.bat C:\project
```

### Error: "Script execution is disabled"
**Solution:** Change execution policy (one-time setup)
```powershell
# Run as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\codepulse.bat C:\project
```

### Error: "Python is not installed"
**Solution:** Install Python 3.9+
1. Download from https://www.python.org/downloads/
2. Run installer
3. Check "Add Python to PATH"
4. Restart PowerShell

---

## Command Prompt Alternative

If PowerShell is causing issues, use Command Prompt instead:

```cmd
# Open Command Prompt
cmd

# Run without .\
codepulse.bat C:\path\to\project
```

---

## Quick Reference

| Task | PowerShell Command |
|------|-------------------|
| Basic scan | `.\codepulse.bat C:\project` |
| 8 workers | `.\codepulse.bat C:\project --workers 8` |
| Clear cache | `.\codepulse.bat C:\project --clear-cache` |
| No cache | `.\codepulse.bat C:\project --no-cache` |
| Full scan | `.\codepulse.bat C:\project --no-incremental` |
| JS files only | `.\codepulse.bat C:\project --pattern "*.js"` |

---

## Examples

### Scan Discord Bot Project
```powershell
.\codepulse.bat C:\Users\xsll7\Desktop\discord
```

### Scan with Maximum Performance
```powershell
.\codepulse.bat C:\Users\xsll7\Desktop\discord --workers 16
```

### Fresh Scan (Ignore Cache)
```powershell
.\codepulse.bat C:\Users\xsll7\Desktop\discord --clear-cache --no-incremental
```

---

## Pro Tips

1. **Add CodePulse to PATH** (Optional)
   ```powershell
   # Add this to your PowerShell profile
   $env:Path += ";C:\Users\xsll7\Desktop\CodePulse"
   
   # Then you can run from anywhere:
   codepulse.bat C:\any\project
   ```

2. **Create Alias** (Optional)
   ```powershell
   # Add to PowerShell profile
   function codepulse { .\codepulse.bat $args }
   
   # Then use:
   codepulse C:\project
   ```

3. **Tab Completion**
   ```powershell
   # Type path and press TAB
   .\codepulse.bat C:\Users\[TAB]
   ```

---

**Remember:** Always use `.\` before `codepulse.bat` in PowerShell!
