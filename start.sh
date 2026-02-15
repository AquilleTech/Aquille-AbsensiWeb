#!/data/data/com.termux/files/usr/bin/bash
# Startup script for Absensi Web - Termux optimized

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Absensi Web Startup ===${NC}"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python -m venv venv
    echo -e "${GREEN}Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install/update dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}Dependencies installed${NC}"

# Initialize data files
echo -e "${YELLOW}Initializing data files...${NC}"
python -c "from wsgi import init_data_files; init_data_files()"

# Check if running in development mode
if [ "$1" == "--dev" ]; then
    echo -e "${YELLOW}Starting in DEVELOPMENT mode...${NC}"
    python app.py --dev
else
    # Production mode with Gunicorn
    echo -e "${GREEN}Starting in PRODUCTION mode with Gunicorn...${NC}"
    echo -e "${YELLOW}Workers: 2 (optimized for Termux)${NC}"
    echo -e "${YELLOW}Binding to: 0.0.0.0:5000${NC}"
    echo ""
    echo -e "${GREEN}Server will be accessible at:${NC}"
    echo -e "  Local:   http://localhost:5000"
    echo -e "  Network: http://$(hostname -I | awk '{print $1}'):5000"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
    echo ""
    
    gunicorn -c gunicorn_config.py wsgi:application
fi
