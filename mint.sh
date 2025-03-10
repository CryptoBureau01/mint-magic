# !/bin/bash

curl -s https://raw.githubusercontent.com/CryptoBureau01/logo/main/logo.sh | bash
sleep 5

# Function to print info messages
print_info() {
    echo -e "\e[32m[INFO] $1\e[0m"
}

# Function to print error messages
print_error() {
    echo -e "\e[31m[ERROR] $1\e[0m"
}



#Function to check system type and root privileges
master_fun() {
    echo "Checking system requirements..."

    # Check if the system is Ubuntu
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [ "$ID" != "ubuntu" ]; then
            echo "This script is designed for Ubuntu. Exiting."
            exit 1
        fi
    else
        echo "Cannot detect operating system. Exiting."
        exit 1
    fi

    # Check if the user is root
    if [ "$EUID" -ne 0 ]; then
        echo "You are not running as root. Please enter root password to proceed."
        sudo -k  # Force the user to enter password
        if sudo true; then
            echo "Switched to root user."
        else
            echo "Failed to gain root privileges. Exiting."
            exit 1
        fi
    else
        echo "You are running as root."
    fi

    echo "System check passed. Proceeding to package installation..."
}


# Function to install dependencies
install_dependency() {
    print_info "<=========== Install Dependency ==============>"
    echo "Checking Python version..."
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    REQUIRED_VERSION="3.10"
    
    if [[ "$PYTHON_VERSION" != "$REQUIRED_VERSION"* ]]; then
        echo "Upgrading to Python 3.10..."
        sudo apt update && sudo apt install -y python3.10 python3.10-venv python3.10-dev
    else
        echo "Python 3.10 is already installed."
    fi
    
    echo "Installing required dependencies..."
    sudo apt update && sudo apt install -y curl jq chromium-browser unzip python3-pip
    pip3 install --upgrade pip selenium

    sleep 1
    pip3 install eth_account

    sleep 1
    wget -q https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip && sudo mv chromedriver /usr/local/bin/
    
    echo "Dependencies installed successfully!"
    
    # Call the uni_menu function to display the menu
    master
}



# Function: Set Private Key
set_private_key() {
    mkdir -p magic
    touch magic/data
    read -sp "Enter your MetaMask Private Key: " PRIVATE_KEY
    echo "$PRIVATE_KEY" > magic/data
    echo "\nPrivate key set successfully and saved to magic/data!"
    master
}



check_balance() {
    echo "Checking balance on Monad Testnet..."
    
    # Load private key from file
    if [ -f magic/data ]; then
        PRIVATE_KEY=$(cat magic/data)
    else
        echo "❌ Private key file not found! Please set your private key first."
        return
    fi
    
    # Generate wallet address from private key using Python
    WALLET_ADDRESS=$(python3 -c "from eth_account import Account; acct = Account.from_key('$PRIVATE_KEY'); print(acct.address)" 2>/dev/null)

    if [ -z "$WALLET_ADDRESS" ]; then
        echo "❌ Error generating wallet address! Check your private key."
        return
    fi
    
    echo "🔹 Wallet Address: $WALLET_ADDRESS"
    
    # Get balance from Monad Testnet
    BALANCE_HEX=$(curl -s -X POST "https://testnet-rpc.monad.xyz" \
    -H "Content-Type: application/json" \
    --data '{"jsonrpc":"2.0","method":"eth_getBalance","params":["'$WALLET_ADDRESS'", "latest"],"id":1}' | jq -r '.result')

    if [ -z "$BALANCE_HEX" ] || [ "$BALANCE_HEX" == "null" ]; then
        BALANCE_HEX="0x0"
    fi

    BALANCE_IN_MON=$(python3 -c "print(int('$BALANCE_HEX', 16) / 10**18)")

    echo "✅ Your Monad Testnet Balance: $BALANCE_IN_MON MON"

    # Call the uni_menu function to display the menu
    master
}



# Function: Set Magic Eden Mint URL
set_mint_url() {
    read -p "Enter Magic Eden Mint Page URL: " MINT_URL
    echo "$MINT_URL" > magic/data_url
    echo "Mint URL set and saved to magic/data_url!"
    
    # Call the uni_menu function to display the menu
    master
}


# Function: Check Mint Time
check_mint_time() {
    # Ensure magic folder exists
    mkdir -p magic

    # Check if time.py exists, if not download it
    if [ ! -f magic/time.py ]; then
        echo "🔄 Downloading time.py from GitHub..."
        curl -s -o magic/time.py https://raw.githubusercontent.com/CryptoBureau01/mint-magic/main/time.py
        if [ $? -ne 0 ]; then
            echo "❌ Failed to download time.py! Check your internet connection or GitHub link."
            return
        fi
        chmod +x magic/time.py  # Make it executable
    fi

    # Run the Python script and fetch the mint time
    echo "🔄 Running Python script to fetch mint time..."
    MINT_TIME=$(python3 magic/time.py | grep -oP '(?<=✅ Mint starts in: ).*')

    if [ -z "$MINT_TIME" ]; then
        echo "❌ Could not retrieve mint time. Please check the URL in magic/data."
    else
        echo "✅ Mint starts at: $MINT_TIME"
    fi

    # Call the uni_menu function to display the menu
    master
}



# Function: Automatic Fast Mint with Selenium
automatic_mint() {
    if [ ! -f magic/data ] || [ ! -f magic/data_url ]; then
        echo "Missing private key or mint URL! Please set both first."
        return
    fi
    
    PRIVATE_KEY=$(cat magic/data)
    MINT_URL=$(cat magic/data_url)
    
    echo "Launching browser for minting..."
    
    python3 - <<EOF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening browser
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

driver.get("$MINT_URL")
time.sleep(2)  # Allow page to load

try:
    mint_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Mint')]")
    mint_button.click()
    print("Mint button clicked successfully!")
except Exception as e:
    print("Error clicking mint button:", e)

time.sleep(2)
driver.quit()
EOF

    echo "Fast minting executed via CryptoBureau!"
    
    # Call the uni_menu function to display the menu
    master
}








# Function to display menu and prompt user for input
master() {
    print_info "==============================="
    print_info "    Magic-Mint Tool Menu       "
    print_info "==============================="
    print_info ""
    print_info "1. Install-Dependency"
    print_info "2. Set-Private-Key"
    print_info "3. Check-Balance"
    print_info "4. Set-Mint-Url"
    print_info "5. Check-Mint-Time"
    print_info "6. Auto-Mint"
    print_info "7. Exit"
    print_info ""
    print_info "==============================="
    print_info " Created By : CB-Master "
    print_info "==============================="
    print_info ""
    
    read -p "Enter your choice (1 or 7): " user_choice

    case $user_choice in
        1)
            install_dependency
            ;;
        2)
            set_private_key
            ;;
        3) 
            check_balance
            ;;
        4)
            set_mint_url
            ;;
        5)
            check_mint_time
            ;;
        6)
            automatic_mint
            ;;
        7)
            exit 0  # Exit the script after breaking the loop
            ;;
        *)
            print_error "Invalid choice. Please enter 1 or 7 : "
            ;;
    esac
}

# Call the uni_menu function to display the menu
master_fun
master


