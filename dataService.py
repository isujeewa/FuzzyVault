from db_connection import connect_to_database
import json

def insert_profile_data(GUID, name, email, encoded_data):
    conn = connect_to_database()
    if conn is not None:
        try:
            cur = conn.cursor()

            print(cur.statusmessage)
            
            # Check if the email already exists
            cur.execute("SELECT COUNT(*) FROM ProfileMaster WHERE email = %s", (email,))
            result = cur.fetchone()
            if result[0] > 0:
                print("Email already exists. Skipping insertion.")
                return "Email already exists"
            
            # If email doesn't exist, insert the new record
            cur.execute(
                "INSERT INTO ProfileMaster (GUID, name, email, encoded_data) VALUES (%s, %s, %s, %s)",
                (GUID, name, email, encoded_data)
            )
            conn.commit()
            print("Data inserted successfully.")
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting data:", error)
        finally:
            if conn:
                cur.close()
                conn.close()

def get_profile_data_by_email(email):
    conn = connect_to_database()
    if conn is not None:
        try:
            cur = conn.cursor()

            # Execute SQL query to fetch record by email
            cur.execute("SELECT * FROM ProfileMaster WHERE email = %s", (email,))
            profile_data = cur.fetchone()
            
            if profile_data:
                print("Profile data found:")
                print(profile_data)
                return profile_data
            else:
                print("No profile data found for email:", email)
                return None

        except (Exception, psycopg2.Error) as error:
            print("Error while retrieving profile data:", error)
        finally:
            if conn:
                cur.close()
                conn.close()

def get_profile_data_by_guid(guid):
    conn = connect_to_database()
    if conn is not None:
        try:
            cur = conn.cursor()

            # Execute SQL query to fetch record by GUID
            cur.execute("SELECT * FROM ProfileMaster WHERE guid = %s", (guid,))
            profile_data = cur.fetchone()
            
            if profile_data:
                print("Profile data found:")
      
                return profile_data
            else:
                print("No profile data found for GUID:", guid)
                return None

        except (Exception, psycopg2.Error) as error:
            print("Error while retrieving profile data:", error)
        finally:
            if conn:
                cur.close()
                conn.close()


def get_all_profiles():
    conn = connect_to_database()
    if conn is not None:
        try:
            cur = conn.cursor()

            # Execute SQL query to fetch all profiles
            cur.execute("SELECT guid, name FROM ProfileMaster")
            profile_data = cur.fetchall()

            if profile_data:
                print("Profile data found:")
                profiles = []
                for profile in profile_data:
                    profiles.append({
                        'guid': profile[0],
                        'name': profile[1]
                    })
                    print(f"ID: {profile[0]}, Name: {profile[1]}")
                return json.dumps(profiles)  # Convert to JSON
            else:
                print("No profile data found.")
                return None

        except (Exception, psycopg2.Error) as error:
            print("Error while retrieving profile data:", error)
        finally:
            if conn:
                cur.close()
                conn.close()

# Example usage
profiles = get_all_profiles()
