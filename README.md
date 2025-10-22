# TON Jettons Index

Automated synchronization and conversion of TON jetton metadata from YAML to JSON format.

## Overview

This repository automatically syncs jetton metadata from the [tonkeeper/ton-assets](https://github.com/tonkeeper/ton-assets) repository, converts YAML files to a single consolidated JSON file for easy consumption across applications.

## Data Format

The source data from ton-assets contains YAML files with the following structure:

```yaml
name: AssassinoTON
symbol: ASSA
address: EQACKFv2jcRfO89mSUtY-xY4BMpmGdFhDNaocTUr7vWUj0XQ
image: "https://cdn.dexscreener.com/..."
description: |
  Token description
websites:
  - "https://example.com/"
social:
  - "https://x.com/example"
  - "https://t.me/example"
```

This is converted to a JSON object in `jettons.json` where each jetton is keyed by its **symbol**.

## Usage

### Consuming the Data

You can fetch the jettons data directly from this repository:

```javascript
// Fetch the jettons data
const response = await fetch('https://raw.githubusercontent.com/YOUR_USERNAME/jetton-index/main/jettons.json');
const jettons = await response.json();

// Access a specific jetton by its symbol
console.log(jettons['ASSA']);  // AssassinoTON
console.log(jettons['DOGS']);  // DOGS token
console.log(jettons['NOT']);   // Notcoin

// List all available symbols
console.log(Object.keys(jettons));
```

### Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the sync script:
```bash
python sync_jettons.py
```

This will:
- Clone the ton-assets repository
- Convert all YAML jetton files to JSON
- Save the result to `jettons.json`

## Automation

The repository uses GitHub Actions to automatically sync the data:

- **Daily Schedule**: Runs once per day at 00:00 UTC
- **Manual Trigger**: Can be triggered manually via the Actions tab

When changes are detected, the workflow:
1. Creates a new staging branch
2. Commits the updated `jettons.json`
3. Opens a pull request for review

## Contributing

This is an automated repository. If you need to modify the sync logic:

1. Edit `sync_jettons.py` for conversion logic changes
2. Edit `.github/workflows/sync-jettons.yml` for workflow changes
3. Submit a pull request

## License

This repository contains data sourced from [tonkeeper/ton-assets](https://github.com/tonkeeper/ton-assets). Please refer to their repository for licensing information on the jetton metadata.

