# SCRIPT TO DISPLAY ALL UserIPLog and IPDemographics tables
# Shows encrypted data (safe to view without exposing sensitive info) BECAUSE ONLY DEV HAS THE ENCRYPTION KEY
# FEEL FREE TO MODIFY OR ADD TO QUERY STUFF! OR EXPORT DATA INTO A FILE!

# TO RUN THIS DO THIS IN CONSOLE
# python display_tables.py (encrypted data)
# OR
# python display_tables.py --decrypt

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app, db
    from app.models import UserIPLog, IPDemographics, User
    from app.custom_types import decrypt_encrypted_field
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this from your project root directory")
    sys.exit(1)

def display_userip_logs(limit=20, show_decrypted=False):
    print(f"\n{'='*80}")
    print("USER IP LOGS")
    print(f"\n{'='*80}")
    print(f"{'ID':<5} {'User ID':<8} {'IP Address (Encrypted)':<50} {'Timestamp':<20}")
    print(f"\n{'-'*80}")

    logs = UserIPLog.query.order_by(UserIPLog.timestamp.desc()).limit(limit).all()

    if not logs:
        print("No IP logs found")
        return
    for log in logs:
        timestamp = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        if show_decrypted:
            try:
                decrypted_ip = decrypt_encrypted_field(log.ip_address)
                ip_display = f"{log.ip_address[:20]}... -> {decrypted_ip}"
            except Exception as e:
                ip_display = f"{log.ip_address[:20]}... (decrypt error)"
        else:
            ip_display = log.ip_address[:47] + "..." if len(log.ip_address) > 47 else log.ip_address
        
        print(f"{log.id:<5} {log.user_id:<8} {ip_display:<50} {timestamp:<20}")

        if log.user_agent and show_decrypted:
            try:
                decrypted_ua = decrypt_encrypted_field(log.user_agent)
                print(f"    User Agent: {decrypted_ua}")
            except Exception as e:
                print(f"    User Agent: (encrypt - decrypt error)" )
        elif log.user_agent:
            print(f"    User Agent: {log.user_agent[:60]}... (encrypted)")

def display_ip_demographics(limit=20, show_decrypted=False):
    print(f"\n{'='*80}")
    print("IP DEMOGRAPHICS")
    print(f"\n{'='*80}")
    print(f"{'ID':<5} {'User ID':<8} {'IP Address (Encrypted)':<50} {'Country (Encrypted)':<25} {'Country Code (Encrypted)':<8} {'Updated':<20}")
    print(f"\n{'-'*80}")

    demographics = IPDemographics.query.order_by(IPDemographics.last_updated.desc()).limit(limit).all()

    if not demographics:
        print("No demographic data found.")
        return
    for demographic in demographics:
        timestamp = demographic.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        
        if show_decrypted:
            try:
                decrypted_ip = decrypt_encrypted_field(demographic.ip_address)
                ip_display = f"{decrypted_ip}"
                
                if demographic.country:
                    decrypted_country = decrypt_encrypted_field(demographic.country)
                    country_display = decrypted_country
                else:
                    country_display = "None"
                if demographic.country_code:
                    decrypted_country_code = decrypt_encrypted_field(demographic.country_code)
                    country_code_display = decrypted_country_code
                else:
                    country_code_display = "None"
            except Exception as e:
                ip_display = f"{demographic.ip_address[:27]}..."
                country_display = f"{demographic.country[:22] if demographic.country else 'None'}..."
                country_code_display = f"{demographic.country_code[:22] if demographic.country_code else 'None'}..."
        else:
            ip_display = demographic.ip_address[:27] + "..." if len(demographic.ip_address) > 27 else demographic.ip_address
            country_display = (demographic.country[:22] + "..." if len(demographic.country) > 22 and demographic.country
                else demographic.country if demographic.country else "None")

        print(f"{demographic.id:<5} {demographic.user_id:<8} {ip_display:<30} {country_display:<25} {country_code_display:<8} {timestamp:<20}")

def display_user_summary():
    print(f"\n{'='*80}")
    print("USER SUMMARY")
    print(f"{'='*80}")
    print(f"{'User ID':<8} {'Username':<20} {'IP Logs':<10} {'Demographics':<12} {'Last Activity':<20}")
    print("-" * 80)

    users = User.query.all()

    for user in users:
        ip_log_count = UserIPLog.query.filter_by(user_id=user.id).count()
        demographic_count = IPDemographics.query.filter_by(user_id=user.id).count()

        last_log = UserIPLog.query.filter_by(user_id=user.id).order_by(UserIPLog.timestamp.desc()).first()
        last_activity = last_log.timestamp.strftime("%Y-%m-%d %H:%M:%S") if last_log else "Never"

        print(f"{user.id:<8} {user.username:<20} {ip_log_count:<10} {demographic_count:<12} {last_activity:<20}")

def main():
    app = create_app()

    with app.app_context():
        print("Database Table Display")
        print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        show_decrypted = False
        if len(sys.argv) > 1 and sys.argv[1].lower() == '--decrypt':
            show_decrypted = True
            print("\n!!!!! SHOWING DECRYPTED DATA - Use carefully!")

        display_user_summary()

        display_userip_logs(limit=20, show_decrypted=show_decrypted)

        display_ip_demographics(limit=20, show_decrypted=show_decrypted)

        print(f"\n{'='*80}")
        print("TABLE COUNTS")
        print(f"{'='*80}")
        print(f"Total Users: {User.query.count()}")
        print(f"Total IP Logs: {UserIPLog.query.count()}")
        print(f"Total Demographics: {IPDemographics.query.count()}")

        if not show_decrypted:
            print(f"\n💡 Use '--decrypt' flag to show decrypted data (be careful!)")
            print("   Example: python display_tables.py --decrypt")

if __name__ == "__main__":
    main()