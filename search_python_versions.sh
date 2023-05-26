#!/bin/bash

# Search for Python installations in the Registry
python_reg_keys=(
  "HKLM\\SOFTWARE\\Python\\PythonCore\\*"
  "HKCU\\SOFTWARE\\Python\\PythonCore\\*"
)

# Loop through the registry keys and extract the installed Python versions
for reg_key in "${python_reg_keys[@]}"; do
  IFS=$'\n' read -rd '' -a reg_values < <(reg query "$reg_key" /s /v "DisplayName" 2>/dev/null | grep "DisplayName" | sed -E 's/.*REG_SZ[[:space:]]+(.+)/\1/')
  
  for reg_value in "${reg_values[@]}"; do
    if [[ "$reg_value" == Python* ]]; then
      echo "$reg_value"
    fi
  done
done


echo "use where method"

#!/bin/bash

python_executables=("python.exe" "python3.exe" "python3.11.exe" "python3.10.exe" "python3.9.exe" "python3.8.exe" "python3.7.exe" "python3.6.exe" "python2.exe")

# Loop through the list of Python executable names
for executable in "${python_executables[@]}"; do
  # Use the 'where' command to search for the executable
  path=$(where "$executable" 2>/dev/null)
  
  if [ -n "$path" ]; then
    # Extract the version from the executable path
    version=$(echo "$path" | grep -oP "(?<=Python)\d\.\d+")
    echo "Python $version for the executable $executable found at:\n$path"
  fi
done
