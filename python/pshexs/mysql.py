import pymysql
from pshconfig import Config
import traceback, sys


def test_output():

    # Create a new Config object to ease reading the Platform.sh environment variables.
    # You can alternatively use os.environ yourself.
    config = Config()

    # The 'database' relationship is generally the name of primary SQL database of an application.
    # That's not required, but much of our default automation code assumes it.' \
    credentials = config.credentials('database')

    try:

        # credentials = {'username': 'user', 'scheme': 'mysql', 'service': 'mysql',
        # 'fragment': None, 'ip': '169.254.226.182',
        # 'hostname': 'nwqutumgmypgceiua3kbrlb4ie.mysql.service._.eu-3.platformsh.site',
        # 'public': False, 'cluster': 'rjify4yjcwxaa-pythonexs-y2koaha',
        # 'host': 'database.internal', 'rel': 'mysql', 'query': {'is_master': True},
        # 'path': 'main', 'password': '', 'type': 'mysql:10.2', 'port': 3306}

        # Connect to the database using PDO. If using some other abstraction layer you would inject the values
        # from `database` into whatever your abstraction layer asks for.
        conn = pymysql.connect(host=credentials['host'],
                               port=credentials['port'],
                               database=credentials['path'],
                               user=credentials['username'],
                               password=credentials['password'])

        # Create a table.
        sql = "CREATE TABLE People (" \
              "id SERIAL PRIMARY KEY," \
              "name VARCHAR(30) NOT NULL," \
              "city VARCHAR(30) NOT NULL" \
              ")"

        cur = conn.cursor()
        cur.execute(sql)

        # Insert data.
        sql = "INSERT INTO People (name, city) VALUES" \
              "('Neil Armstrong', 'Moon')," \
              "('Buzz Aldrin', 'Glen Ridge')," \
              "('Sally Ride', 'La Jolla');"

        cur.execute(sql)

        # Show table.
        sql = "SELECT * FROM People"
        cur.execute(sql)
        result = cur.fetchall()

        table = "<table>" \
                "<thead>" \
                "<tr><th>Name</th><th>City</th></tr>" \
                "</thead>" \
                "<tbody>"

        if result:
            for record in result:
                table += "<tr><td>{0}</td><td>{1}</td><tr>\n".format(record[1], record[2])

            table += "</tbody>\n</table>\n"

        # Close communication with the database
        cur.close()
        conn.close()

        return table

        # return credentials

    except Exception as e:
        return traceback.format_exc(), sys.exc_info()[0]
#
# try:
#     pass
#     # Connect to the database using PDO.  If using some other abstraction layer you would
#     # inject the values from $database into whatever your abstraction layer asks for.
#     dsn = 'mysql:host={};port={};dbname={}'.format(
#         credentials['host'],
#         credentials['port'],
#         credentials['path']
#     )
# #     $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s', $credentials['host'], $credentials['port'], $credentials['path']);
#     conn = pymysql.connect(dsn, user=credentials['username'], password=credentials['password'])
# #     $conn = new \PDO($dsn, $credentials['username'], $credentials['password'], [
# #         // Always use Exception error mode with PDO, as it's more reliable.
# #         \PDO::ATTR_ERRMODE => \PDO::ERRMODE_EXCEPTION,
# #         // So we don't have to mess around with cursors and unbuffered queries by default.
# #         \PDO::MYSQL_ATTR_USE_BUFFERED_QUERY => TRUE,
# #         // Make sure MySQL returns all matched rows on update queries including
# #         // rows that actually didn't have to be updated because the values didn't
# #         // change. This matches common behavior among other database systems.
# #         \PDO::MYSQL_ATTR_FOUND_ROWS => TRUE,
# #     ]);
#
#     # Creating a table.
#     sql = "CREATE TABLE People(id int, name, city)"
# #
# #     // Creating a table.
# #     $sql = "CREATE TABLE People (
# #       id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
# #       name VARCHAR(30) NOT NULL,
# #       city VARCHAR(30) NOT NULL
# #       )";
#     conn.query(sql)
# #     $conn->query($sql);
# #
#     # Insert data.
#     sql = "INSERT INTO People (name, city) VALUES" \
#           "('Neil Armstrong', 'Moon')," \
#           "('Buzz Aldrin', 'Glen Ridge')," \
#           "('Sally Ride', 'La Jolla')"
# #     $sql = "INSERT INTO People (name, city) VALUES
# #         ('Neil Armstrong', 'Moon'),
# #         ('Buzz Aldrin', 'Glen Ridge'),
# #         ('Sally Ride', 'La Jolla');";
#     conn.query(sql)
# #     $conn->query($sql);
# #
#     # Show table.
#     sql = "SELECT * FROM People"
#     result = conn.query(sql)
#     # result.setFetchMode(\PDO::FETCH_OBJ)
#
# #     // Show table.
# #     $sql = "SELECT * FROM People";
# #     $result = $conn->query($sql);
# #     $result->setFetchMode(\PDO::FETCH_OBJ);
# #
#     if result:
#         print('<<<TABLE'
#               '<table>'
#               '<thead>'
#               '<tr><th>Name</th><th>City</th></tr>'
#               '</thead>'
#               '<tbody>'
#               'TABLE;')
# #     if ($result) {
# #         print <<<TABLE
# # <table>
# # <thead>
# # <tr><th>Name</th><th>City</th></tr>
# # </thead>
# # <tbody>
# # TABLE;
#
#     for record in result:
#         print('<tr><td>{}</td><td?{}'.format(record.name, record.city))
#         print('</tbody>\n</table>\n')
# #         foreach ($result as $record) {
# #             printf("<tr><td>%s</td><td>%s</td></tr>\n", $record->name, $record->city);
# #         }
# #         print "</tbody>\n</table>\n";
# #     }
# #
# #     // Drop table
#     sql = "DROP TABLE People"
#     conn.query(sql)
# #     $conn->query($sql);
# #
# except Exception as e:
#     print(e)
# # } catch (\Exception $e) {
# #     print $e->getMessage();
# # }
