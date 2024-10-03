import pandas as pd
import mysql.connector as mysql

# Database configuration
db_user = 'avnadmin'
db_password = 'AVNS_592DGU0nSa5ssouh1tg'
db_host = 'mysql-group11-p1-shivambavaria1313-2f9c.b.aivencloud.com'
db_port = '28090'
db_schema = 'GROUP11P1'

files = ['./datafiles/Badges.csv', './datafiles/Comments.csv','./datafiles/PostTypes.csv','./datafiles/Posts.csv','./datafiles/PostTags.csv','./datafiles/Tags.csv','./datafiles/Users.csv','./datafiles/Votes.csv']

table_etl_meta = {
    # "Tags": dict(source_file="Tags", dest_columns=["tag_id", "tag_name"], source_columns=["Id", "TagName"]),
    # "Users": dict(source_file="Users", dest_columns=["id", "reputation"], source_columns=["Id", "Reputation"]),
    # "PostTypes": dict(source_file="PostTypes", dest_columns=["id", "type_title"], source_columns=["Id", "Type_name"]),
    # "Badges": dict(source_file="Badges", dest_columns=["id", "badge_title", "badge_class"], source_columns=["Id", "Name", "Class"]),
    # "Posts": dict(source_file="Posts", dest_columns=["id", "created_date", "post_score", "created_by", "post_type_id"], source_columns=["Id", "CreationDate", "Score", "OwnerUserId", "PostTypeId"]),
    # "Votes": dict(source_file="Votes", dest_columns=["vote_id", "post_id"], source_columns=["Id", "PostId"]),
    "Comments": dict(source_file="Comments", dest_columns=["id", "user_id", "created_at", "score"], source_columns=["Id", "UserId", "CreationDate", "Score"]),
    "BadgeEarns": dict(source_file="Badges", dest_columns=["user_id", "badge_id", "allowted_date"], source_columns=["UserId", "Id", "Date"]),
    "PostTags": dict(source_file="PostTags", dest_columns=["tag_id", "post_id"], source_columns=["Id_y", "Id_x"])
}

print("---Reading CSV files----")
data_df = dict()
for each in files:
  data_df[each.split("/")[-1].split(".")[0]] = pd.read_csv(each)
print("---Completed reading CSV files----")

def generate_insert_query(table, columns):
    column_names = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    return f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"


def start_etl():
    print("Making Connection!!")
    conn = mysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_schema,
        port=db_port,
    )
    print("Connection Successful")

    for table, _meta in table_etl_meta.items():
        _query = generate_insert_query(table, _meta["dest_columns"])
        print(f"---INSERT Query:  {_query}")
        prepared_data = data_df[_meta["source_file"]][_meta["source_columns"]]
        prepared_data = list(prepared_data.itertuples(index=False, name=None))
        cursor = conn.cursor()
        cursor.executemany(_query, prepared_data)
        conn.commit()
        print(f"{cursor.rowcount} rows were inserted into {table} successfully!")
        cursor.close()

    conn.close()
    print("Connection Closed...")

print("Starting Script!!")
start_etl()
print("Ran Script!!")
