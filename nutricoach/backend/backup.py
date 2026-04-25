"""
Database backup utility for NutriCoach AI
Creates timestamped backups of the SQLite database
"""
import sqlite3
import os
import shutil
import datetime
import gzip
import json


def backup_database(db_path='database.db', backup_dir='backups'):
    """
    Create a backup of the database
    Returns: path to backup file
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Generate timestamp for backup filename
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"nutricoach_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Copy database file
    shutil.copy2(db_path, backup_path)
    
    # Create compressed version
    compressed_path = backup_path + '.gz'
    with open(backup_path, 'rb') as f_in:
        with gzip.open(compressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Remove uncompressed backup
    os.remove(backup_path)
    
    print(f"✓ Database backed up to: {compressed_path}")
    return compressed_path


def restore_database(backup_path, db_path='database.db'):
    """
    Restore database from backup
    """
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup file not found: {backup_path}")
    
    # Create backup of current database before restoring
    if os.path.exists(db_path):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        current_backup = f"{db_path}.backup_{timestamp}"
        shutil.copy2(db_path, current_backup)
        print(f"✓ Current database backed up to: {current_backup}")
    
    # Restore from compressed backup
    if backup_path.endswith('.gz'):
        with gzip.open(backup_path, 'rb') as f_in:
            with open(db_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        shutil.copy2(backup_path, db_path)
    
    print(f"✓ Database restored from: {backup_path}")
    return True


def list_backups(backup_dir='backups'):
    """List all available backups"""
    if not os.path.exists(backup_dir):
        print("No backups directory found")
        return []
    
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.endswith('.db.gz'):
            filepath = os.path.join(backup_dir, filename)
            file_size = os.path.getsize(filepath)
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append({
                'filename': filename,
                'path': filepath,
                'size': f"{file_size / 1024:.1f} KB",
                'created': file_time.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    # Sort by creation time (newest first)
    backups.sort(key=lambda x: x['created'], reverse=True)
    return backups


def export_user_data(user_id, db_path='database.db'):
    """
    Export all data for a specific user as JSON
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    export_data = {
        'export_date': datetime.datetime.now().isoformat(),
        'user_id': user_id
    }
    
    # Export user profile
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    if user:
        export_data['profile'] = dict(user)
        export_data['profile'].pop('password_hash', None)  # Don't export password
    
    # Export health profile
    cur.execute('SELECT * FROM health_profiles WHERE user_id = ?', (user_id,))
    health = cur.fetchall()
    export_data['health_profiles'] = [dict(h) for h in health]
    
    # Export meals
    cur.execute('SELECT * FROM meals WHERE user_id = ? ORDER BY date DESC', (user_id,))
    meals = cur.fetchall()
    export_data['meals'] = [dict(m) for m in meals]
    
    # Export exercise logs
    cur.execute('SELECT * FROM exercise_logs WHERE user_id = ? ORDER BY date DESC', (user_id,))
    exercises = cur.fetchall()
    export_data['exercises'] = [dict(e) for e in exercises]
    
    # Export weight logs
    cur.execute('SELECT * FROM weight_logs WHERE user_id = ? ORDER BY date DESC', (user_id,))
    weights = cur.fetchall()
    export_data['weight_logs'] = [dict(w) for w in weights]
    
    # Export water logs
    cur.execute('SELECT * FROM water_logs WHERE user_id = ? ORDER BY date DESC', (user_id,))
    water = cur.fetchall()
    export_data['water_logs'] = [dict(w) for w in water]
    
    conn.close()
    
    # Save to JSON file
    export_filename = f"user_{user_id}_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    export_path = os.path.join('exports', export_filename)
    
    if not os.path.exists('exports'):
        os.makedirs('exports')
    
    with open(export_path, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    print(f"✓ User data exported to: {export_path}")
    return export_path


def cleanup_old_backups(backup_dir='backups', keep_last=10):
    """Remove old backups, keeping only the most recent ones"""
    backups = list_backups(backup_dir)
    
    if len(backups) <= keep_last:
        print(f"✓ {len(backups)} backups found (keeping last {keep_last})")
        return
    
    # Remove old backups
    for backup in backups[keep_last:]:
        os.remove(backup['path'])
        print(f"✓ Removed old backup: {backup['filename']}")
    
    print(f"✓ Cleaned up backups, keeping last {keep_last}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python backup.py [backup|restore|list|export|cleanup]")
        print("  backup         - Create database backup")
        print("  restore <file> - Restore from backup")
        print("  list           - List all backups")
        print("  export <user_id> - Export user data")
        print("  cleanup        - Remove old backups")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'backup':
        backup_database()
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Error: Please specify backup file to restore")
            sys.exit(1)
        restore_database(sys.argv[2])
    elif command == 'list':
        backups = list_backups()
        if backups:
            print(f"\n{'Filename':<50} {'Size':<10} {'Created':<20}")
            print("=" * 80)
            for backup in backups:
                print(f"{backup['filename']:<50} {backup['size']:<10} {backup['created']:<20}")
        else:
            print("No backups found")
    elif command == 'export':
        if len(sys.argv) < 3:
            print("Error: Please specify user ID to export")
            sys.exit(1)
        export_user_data(int(sys.argv[2]))
    elif command == 'cleanup':
        cleanup_old_backups()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
