import os
import subprocess

# Define SQL Server connection details
server = os.environ['MAINTENANCE_DB_CONNECTION_URL']
database = os.environ['MAINTENANCE_DB_NAME']

# Creating procedure in DB
def procedure_execution_on_db(query_name):
    try:
        procedure_execution = subprocess.run(
            query_name,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if procedure_execution.returncode == 0:
            print("Procedure has been executed successfully")
        else:
            print("Error Occurred:")
            print(procedure_execution.stderr)

    except subprocess.CalledProcessError as e:
        print("Error running sqlcmd command:")
        print(e.stderr)

def main():

    # Creating procedure in DB
    procedure_creation_from_file = os.path.abspath("/app/AzureSQLMaintenance.txt")

    creating_procedure_command = [
        "/opt/mssql-tools18/bin/sqlcmd",
        "-S", server,
        "-d", database,
        "-G",
        "-i", procedure_creation_from_file,
        "-t", "65534",
        "-l", "60"
    ]

    print(f"Creating procedure in DB for Server {server} and DB {database}")
    procedure_execution_on_db(creating_procedure_command)

    # Triggering maintenance procedure for indexes
    procedure_for_indexes = "exec [dbo].[AzureSQLMaintenance] @Operation='index',@mode='smart',@LogToTable=1"

    triggering_procedure_index_command = [
        "/opt/mssql-tools18/bin/sqlcmd",
        "-S", server,
        "-d", database,
        "-G",
        "-Q", procedure_for_indexes,
        "-t", "65534",
        "-l", "60"
    ]

    print(f"Triggering maintenance procedure for indexes on Server {server} and DB {database}")
    procedure_execution_on_db(triggering_procedure_index_command)

    # Triggering maintenance procedure for statistics
    procedure_for_statistics = "exec [dbo].[AzureSQLMaintenance] @Operation='statistics',@mode='dummy',@LogToTable=1"

    triggering_procedure_statistics_command = [
        "/opt/mssql-tools18/bin/sqlcmd",
        "-S", server,
        "-d", database,
        "-G",
        "-Q", procedure_for_statistics,
        "-t", "65534",
        "-l", "60"
    ]

    print(f"Triggering maintenance procedure for statistics on Server {server} and DB {database}")
    procedure_execution_on_db(triggering_procedure_statistics_command)

if __name__ == "__main__":
    main()