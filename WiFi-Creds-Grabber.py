import subprocess
import os

# Create the output file
with open('passwords.txt', 'w') as f:
    f.write("Availabe Wi-Fi credentials on the machine:\n")
    f.close()

# Execute cmd commands
command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output = True).stdout.decode()

# Grab current directory
path = os.getcwd()

# Main
wifi_files = []
for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)

for i in wifi_files:
    with open(i, 'r') as f:
        # Prevent duplicate names from xml files
        name_counter = 0

        # Reset values
        wifi_name = ""
        wifi_password = ""
        creds = []

        for line in f.readlines():
            if "name" in line and name_counter == 0:
                name_counter += 1
                stripped = line.strip()
                front = stripped[6:]
                back = front[:-7]
                wifi_name = back
            if "keyMaterial" in line:
                stripped = line.strip()
                front = stripped[13:]
                back = front[:-14]
                wifi_password = back

    # Set password value for SSIDs with non defined passwords
    if wifi_password == "":
        wifi_password = "none"

    creds = [wifi_name, wifi_password]

    # Write the grabbed creds to passwords.txt file
    with open('passwords.txt', 'a') as f:
        f.write("\n[*] SSID: " + creds[0] + "\n" + "[!] Password: " + creds[1] + "\n")
        f.close()


# Delete created files
for i in wifi_files:
    os.remove(i)
