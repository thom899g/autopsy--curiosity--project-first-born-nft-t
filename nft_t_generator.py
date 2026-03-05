#!/usr/bin/env python3
"""
CURIOSITY: Project First-Born NFT-T Generator
Fixed and Enhanced Version

Architectural Rigor Applied:
1. Robust error handling with fallback mechanisms
2. Type hinting throughout
3. Comprehensive logging system
4. Firebase integration for state persistence
5. Web3.py for Ethereum interaction
6. Time-lock functionality with schedule tracking
"""

import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path

# Third-party imports with error handling
try:
    from web3 import Web3
    from web3.exceptions import ContractLogicError, TransactionNotFound
    from eth_account import Account
    import firebase_admin
    from firebase_admin import credentials, firestore, exceptions
    from PIL import Image
    from dotenv import load_dotenv
    import requests
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Please install required packages:")
    print("pip install web3 eth-account firebase-admin pillow python-dotenv requests")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nft_t_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class NFTTGenerator:
    """NFT-T Generator with time-lock functionality and Firebase state management"""
    
    def __init__(self, network: str = "sepolia"):
        """Initialize the NFT-T Generator with network configuration"""
        self.network = network
        self.w3 = None
        self.contract = None
        self.db = None
        self.account = None
        self.initialized = False
        
        # Configuration based on network
        self.network_configs = {
            "sepolia": {
                "rpc_url": os.getenv("SEPOLIA_RPC_URL", "https://rpc.sepolia.org"),
                "explorer": "https://sepolia.etherscan.io/tx/",
                "chain_id": 11155111
            },
            "mainnet":