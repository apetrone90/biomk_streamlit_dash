class DataHandler:

    def __init__(self, db_name):
        self.db_name = db_name

    def create_database(self):
        return sqlite3.connect(self.db_name)

    def read_and_write_data(self, data_file_path):
        with self.create_database() as conn:
            data_dict = self.read_data(data_file_path)
            self.write_data_to_database(data_dict, data_file_path, conn)

    def read_data(self, data_file_path):
        print(f"Reading data from: {data_file_path}")  # Debugging line
        if data_file_path.endswith('.csv'):
            data = pd.read_csv(data_file_path, encoding='utf-8')
            print(f"Read CSV with shape: {data.shape}")  # Debugging line
        elif data_file_path.endswith('.xlsx'):
            data = pd.read_excel(data_file_path, sheet_name=None)
            print(f"Read Excel with sheet names: {list(data.keys())}")  # Debugging line
            print({sheet: df.shape for sheet, df in data.items()})  # Debugging line
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")

        return data
    

    def write_data_to_database(self, data_dict, data_file_path, conn):
        db_handler = DatabaseHandler(conn)
        if isinstance(data_dict, dict):  # Handling Excel with multiple sheets
            for table_name, df in data_dict.items():
                if not df.empty:  # Skip empty DataFrames
                    db_handler.write_df_to_sql(df, table_name)
                    db_handler.add_table_metadata(table_name, data_file_path)
                else:
                    print(f"Skipping empty sheet: {table_name}")  # Debugging line
        else:
            if not data_dict.empty:
                table_name = data_file_path.split('/')[-1].split('.')[0]
                db_handler.write_df_to_sql(data_dict, table_name)
                db_handler.add_table_metadata(table_name, data_file_path)
            else:
                print("Skipping empty DataFrame")
class DatabaseHandler:
    def __init__(self, conn):
        self.conn = conn

    def write_df_to_sql(self, df, table_name, if_exists='replace'):
        # Ensure the table name is also sanitized
        table_name = self.sanitize_name(table_name, default="table")
        
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("DataFrame is empty.")
        
        # Sanitize the DataFrame column names to be SQL friendly and ensure they are unique
        sanitized_columns = {}
        for i, col in enumerate(df.columns):
            sanitized = self.sanitize_name(col, default=f"column_{i+1}")
            while sanitized in sanitized_columns.values():
                sanitized += f"_{i}"
            sanitized_columns[col] = sanitized

        df.rename(columns=sanitized_columns, inplace=True)
        
        df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)

    def sanitize_name(self, name, default):
        # Remove problematic characters and ensure the name is not a reserved SQL keyword
        sanitized = ''.join(char for char in name if char.isalnum() or char in ['_', ' ']).strip().replace(' ', '_')
        if not sanitized or sanitized.isnumeric() or sanitized.upper() in ["SELECT", "FROM", "WHERE"]:
            sanitized = default
        return sanitized

    def add_table_metadata(self, table_name, file_path):
        metadata = {"table_name": table_name, "file_path": file_path}
        df_metadata = pd.DataFrame([metadata])
        self.write_df_to_sql(df_metadata, 'table_metadata', if_exists='append')

