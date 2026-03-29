import argparse
import requests
import json
import os

def main():
    parser = argparse.ArgumentParser(description="Run F1 Prediction via API")
    parser.add_argument("--season", type=int, required=True, help="F1 Season Year")
    parser.add_argument("--round", type=int, required=True, help="Round Number")
    parser.add_argument("--save", action="store_true", help="Save output to a JSON file")
    
    args = parser.parse_args()
    
    url = f"http://localhost:8000/api/predictions/pre-race/{args.season}/{args.round}"
    print(f"Fetching prediction from {url}...\n")
    
    try:
        response = requests.post(url)
        response.raise_for_status()
        
        data = response.json()
        output = json.dumps(data, indent=2)
        print("Prediction Result:")
        print(output)
        
        if args.save:
            os.makedirs("predictions", exist_ok=True)
            filename = f"predictions/round_{args.round}_{args.season}.json"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"\n[SUCCESS] Prediction saved to {filename}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")

if __name__ == "__main__":
    main()
