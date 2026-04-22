import json
import os
import hashlib

# Yeh file data folder ke andar store hogi
MEMORY_FILE = "data/alert_memory.json"

def get_news_hash(news_list):
    """News items ki list ka ek unique fingerprint (hash) banata hai."""
    content = " ".join(news_list)
    return hashlib.md5(content.encode()).hexdigest()

def is_duplicate_alert(news_list):
    """Check karta hai ki kya ye exact news pehle report ho chuki hai."""
    if not news_list:
        return False
        
    if not os.path.exists(MEMORY_FILE):
        return False
    
    try:
        with open(MEMORY_FILE, "r") as f:
            seen_hashes = json.load(f)
        
        current_hash = get_news_hash(news_list)
        return current_hash in seen_hashes
    except:
        return False

def save_to_memory(news_list):
    """Nayi news ke hash ko JSON file mein save karta hai."""
    if not news_list:
        return
        
    current_hash = get_news_hash(news_list)
    
    seen_hashes = []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                seen_hashes = json.load(f)
        except:
            seen_hashes = []
            
    if current_hash not in seen_hashes:
        seen_hashes.append(current_hash)
        # Sirf last 100 entries rakhte hain taaki file zyada badi na ho
        seen_hashes = seen_hashes[-100:]
        
        with open(MEMORY_FILE, "w") as f:
            json.dump(seen_hashes, f)