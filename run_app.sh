#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Kimi AI Chat Application...${NC}"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}ERROR: pip3 is not installed!${NC}"
    echo "Please install pip3 to continue"
    exit 1
fi

# Check if required packages are installed
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Installing required packages...${NC}"
    pip3 install -r requirements.txt
fi

# Run the Streamlit app
echo
echo -e "${GREEN}🚀 Starting Kimi AI Chat App...${NC}"
echo -e "${YELLOW}📝 Make sure to enter your API key in the sidebar${NC}"
echo

streamlit run kimi_chat_app.py