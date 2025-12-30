#!/bin/bash
# Example commands for the Nurses CSV Processor
# Make this file executable: chmod +x example_commands.sh

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Nurses CSV Processor - Example Commands${NC}"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if input file is provided, otherwise use data.csv from project root
if [ -z "$1" ]; then
    INPUT_FILE="$SCRIPT_DIR/data.csv"
    echo "Usando arquivo padrão: data.csv"
else
    INPUT_FILE="$1"
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Erro: Arquivo '$INPUT_FILE' não encontrado!"
    if [ -z "$1" ]; then
        echo ""
        echo "Dica: Coloque seu arquivo CSV como 'data.csv' na raiz do projeto:"
        echo "  $SCRIPT_DIR/data.csv"
    fi
    exit 1
fi

echo -e "${BLUE}Choose an operation:${NC}"
echo ""
echo "1) Extract ALL nurses"
echo "2) Extract nurses in a specific state"
echo "3) Extract nurses in a specific city"
echo "4) Search by last name"
echo "5) Custom search (state + city)"
echo "6) Custom search (state + name)"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Extracting all nurses..."
        python process_nurses.py --output nurses_all.csv
        ;;
    2)
        read -p "Enter state code (e.g., CA, NY, TX): " state
        echo ""
        echo "Extracting nurses in $state..."
        python process_nurses.py --output "nurses_${state}.csv" --state "$state"
        ;;
    3)
        read -p "Enter city name: " city
        echo ""
        echo "Extracting nurses in $city..."
        python process_nurses.py --output "nurses_$(echo $city | tr ' ' '_').csv" --city "$city"
        ;;
    4)
        read -p "Enter last name: " lastname
        echo ""
        echo "Searching for nurses with last name $lastname..."
        python process_nurses.py --output "nurses_${lastname}.csv" --last-name "$lastname"
        ;;
    5)
        read -p "Enter state code: " state
        read -p "Enter city name: " city
        echo ""
        echo "Extracting nurses in $city, $state..."
        python process_nurses.py --output "nurses_${state}_$(echo $city | tr ' ' '_').csv" --state "$state" --city "$city"
        ;;
    6)
        read -p "Enter state code: " state
        read -p "Enter last name: " lastname
        echo ""
        echo "Extracting nurses with last name $lastname in $state..."
        python process_nurses.py --output "nurses_${lastname}_${state}.csv" --state "$state" --last-name "$lastname"
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done! Check your output file.${NC}"

