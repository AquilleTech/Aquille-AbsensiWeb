#!/usr/bin/env python3
"""
Migration Script: Convert Plain Text Passwords to Hashed Passwords
Run this script ONCE if you're upgrading from the old version
"""

import json
import os
from werkzeug.security import generate_password_hash

USERS_FILE = 'users.json'
BACKUP_FILE = 'users.json.backup'

def migrate_passwords():
    """Migrate plain text passwords to hashed passwords"""
    
    # Check if users.json exists
    if not os.path.exists(USERS_FILE):
        print("❌ users.json not found. No migration needed.")
        return
    
    # Load current users
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Error reading users.json. File might be corrupted.")
        return
    
    if not users_data.get('users'):
        print("ℹ️  No users found. No migration needed.")
        return
    
    # Backup original file
    print("📦 Creating backup...")
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=4)
    print(f"✅ Backup created: {BACKUP_FILE}")
    
    # Check if passwords are already hashed
    first_user = users_data['users'][0]
    if first_user['password'].startswith('pbkdf2:sha256:'):
        print("ℹ️  Passwords are already hashed. No migration needed.")
        return
    
    # Migrate passwords
    print("\n🔄 Migrating passwords...")
    migrated_count = 0
    
    for user in users_data['users']:
        old_password = user['password']
        
        # Check if already hashed
        if old_password.startswith('pbkdf2:sha256:'):
            print(f"  ⏭️  Skipping {user['username']} (already hashed)")
            continue
        
        # Hash the password
        user['password'] = generate_password_hash(old_password)
        migrated_count += 1
        print(f"  ✅ Migrated {user['username']}")
    
    # Save migrated data
    if migrated_count > 0:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=4)
        
        print(f"\n🎉 Migration completed! {migrated_count} password(s) migrated.")
        print(f"📁 Original file backed up to: {BACKUP_FILE}")
        print("\n⚠️  IMPORTANT: Save your backup file in case you need to rollback!")
    else:
        print("\nℹ️  No passwords needed migration.")

def verify_migration():
    """Verify that migration was successful"""
    print("\n🔍 Verifying migration...")
    
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    all_hashed = True
    for user in users_data['users']:
        if not user['password'].startswith('pbkdf2:sha256:'):
            print(f"  ❌ {user['username']}: Password NOT hashed")
            all_hashed = False
        else:
            print(f"  ✅ {user['username']}: Password properly hashed")
    
    if all_hashed:
        print("\n✅ All passwords are properly hashed!")
    else:
        print("\n❌ Some passwords are not hashed. Please check.")

if __name__ == '__main__':
    print("="*60)
    print("🔐 Password Migration Script")
    print("="*60)
    print("\nThis script will convert plain text passwords to hashed passwords.")
    print("Your original users.json will be backed up to users.json.backup")
    print()
    
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        migrate_passwords()
        verify_migration()
        print("\n" + "="*60)
        print("Migration process completed!")
        print("="*60)
    else:
        print("\n❌ Migration cancelled.")
