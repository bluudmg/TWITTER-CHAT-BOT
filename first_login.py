#!/usr/bin/env python3
"""
Run this ONCE to log into X and save your session cookies.
After this you never need to enter your password again.
"""

import asyncio
from twikit import Client
from config import X_USERNAME, X_EMAIL, X_PASSWORD

async def login():
    client = Client('en-US')
    print(f"Logging in as @{X_USERNAME}...")
    
    try:
        await client.login(
            auth_info_1=X_USERNAME,
            auth_info_2=X_EMAIL,
            password=X_PASSWORD
        )
        client.save_cookies('cookies.json')
        print("✓ Login successful. cookies.json saved.")
        print("  You can now run: ./start.sh")
    except Exception as e:
        print(f"✗ Login failed: {e}")
        print("  Check your credentials in config.py")

asyncio.run(login())
