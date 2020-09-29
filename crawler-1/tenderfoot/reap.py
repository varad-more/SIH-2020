"""Reaper module

This module is the initial ranker for the CA scraping bot.
"""

import mysql.connector

error_string = """
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n
Exception : {}\n
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n
"""

class text_color:
    HEADER_COLOR = '\033[95m'
    BLUE_COLOR = '\033[94m'
    GREEN_COLOR = '\033[92m'
    WARNING_COLOR = '\033[93m'
    FAILED_COLOR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Reaper(object):
    """Reaper class ranks the links"""

    def __init__(self, iterations,connection,cursor):
        self.iterations = iterations
        self.connection = connection
        self.cursor = cursor
        print(text_color.HEADER_COLOR
              + "Initialized Reaper object"
              + text_color.ENDC)
        super(Reaper, self).__init__()

    # Connect to database
    def connect_database(self):
        try:
            self.connection = mysql.connector.connect(
                     host="database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com",
                     user="admin",
                     password="SIH_2020",
                     database="pythanos_main"
                   )

            self.cursor = self.connection.cursor(buffered=True)
            print(text_color.GREEN_COLOR + "Database connected" + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Get From ids
    def get_fromids(self):
        try:
            print(text_color.WARNING_COLOR + "Getting from ids" + text_color.ENDC)
            self.cursor.execute('''SELECT DISTINCT from_id FROM links''')
            self.from_ids = list()
            for row in self.cursor:
                self.from_ids.append(row[0])
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Get to ids
    def get_toids(self):
        try:
            print(text_color.WARNING_COLOR + "Getting to ids" + text_color.ENDC)
            # Find the ids that receive page rank
            self.to_ids = list()
            self.links = list()
            self.cursor.execute('''SELECT DISTINCT from_id, to_id FROM links''')
            for row in self.cursor:
                from_id = row[0]
                to_id = row[1]
                if from_id == to_id:
                    continue
                if from_id not in self.from_ids:
                    continue
                if to_id not in self.from_ids:
                    continue
                self.links.append(row)
                if to_id not in self.to_ids:
                    self.to_ids.append(to_id)
        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format(ex)
                  + text_color.ENDC)

    # Get page ranks
    def get_page_ranks(self):
        try:
            # Get latest page ranks for strongly connected component
            self.prev_ranks = dict()
            for node in self.from_ids:
                self.cursor.execute('''SELECT new_rank FROM pages WHERE pages_id = %s''', (node, ))
                row = self.cursor.fetchone()
                self.prev_ranks[node] = row[0]
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # calculate new ranks in memory rather than saving it in db to speed up execution
    def calculate_new_ranks(self):
        try:
            sval = self.iterations
            many = 1
            if (len(sval) > 0):
                many = round(int(sval))

            # Sanity check
            if len(self.prev_ranks) < 1:
                print(text_color.FAILED_COLOR
                      + "Nothing to reap. Check your data."
                      + text_color.ENDC)
                return

            # Page Rank loop
            for i in range(many):
                self.next_ranks = dict()
                total = 0.0
                for (node, old_rank) in list(self.prev_ranks.items()):
                    total = total + old_rank
                    self.next_ranks[node] = 0.0

                # Find the number of outbound links and sent the page rank down each
                for (node, old_rank) in list(self.prev_ranks.items()):
                    self.give_ids = list()
                    for (from_id, to_id) in self.links:
                        if from_id != node:
                            continue
                        if to_id not in self.to_ids:
                            continue
                        self.give_ids.append(to_id)
                    if (len(self.give_ids) < 1):
                        continue
                    amount = old_rank / len(self.give_ids)

                    for id in self.give_ids:
                        self.next_ranks[id] = self.next_ranks[id] + amount

                newtot = 0
                for (node, self.next_rank) in list(self.next_ranks.items()):
                    newtot = newtot + self.next_rank
                evap = (total - newtot) / len(self.next_ranks)

                for node in self.next_ranks:
                    self.next_ranks[node] = self.next_ranks[node] + evap

                newtot = 0
                for (node, next_rank) in list(self.next_ranks.items()):
                    newtot = newtot + next_rank

                total_difference = 0
                for (node, old_rank) in list(self.prev_ranks.items()):
                    new_rank = self.next_ranks[node]
                    diff = abs(old_rank-new_rank)
                    total_difference = total_difference + diff

                average_difference = total_difference / len(self.prev_ranks)
                # rotate
                self.prev_ranks = self.next_ranks
            print(text_color.WARNING_COLOR + "{} {}".format(i+1, average_difference) + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Put the final ranks back into the database
    def update_new_ranks(self):
        try:
            self.cursor.execute('''UPDATE pages SET old_rank=new_rank''')
            for (id, new_rank) in list(self.next_ranks.items()):
                self.cursor.execute('''UPDATE pages SET new_rank=%s WHERE pages_id=%s''', (new_rank, id))
            self.connection.commit()
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Close connection
    def close_cur(self):
        try:
            self.cursor.close()
            print(text_color.GREEN_COLOR + "Connection closed" + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    def reap(self):
        self.get_fromids()
        self.get_toids()
        self.get_page_ranks()
        self.calculate_new_ranks()
        self.update_new_ranks()
