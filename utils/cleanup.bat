# Clear pip cache
pip cache purge

# Clear temporary files
del /q/f/s %TEMP%\*
del /q/f/s C:\Windows\Temp\*

# List all installed packages
pip list --format=freeze > installed_packages.txt

# Remove standard library packages from the list (manually or using a script)
# Example: Remove 'pip' and 'setuptools' from the list
findstr /v "pip setuptools" installed_packages.txt > temp.txt && move /y temp.txt installed_packages.txt

# Uninstall remaining packages
pip uninstall -r installed_packages.txt -y

# Clean up
del installed_packages.txt