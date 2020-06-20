# -*- coding: utf-8 -*-

import json
from tkinter import messagebox


class FilePipeline:
    """
    This is the pipeline that will write the scraped data to the files that were saved by the user
    """

    json_file = None   # the name of the file that will store output in json format
    csv_file = None    # the name of the file that will store output in csv format
    tsv_file = None    # the name of the file that will store output in tsv format
    psv_file = None    # the name of the file that will store output in psv format

    def open_spider(self, spider):
        """
        Prepares a spider to have its data processed by this pipeline
        Gets the paths of this spider's output files so that the data the spider retireves can be written to those files
        :param spider: the spider that will have its data processed by this pipeline
        :return: void
        """
        for file in spider.file_dict:
            if file == "json":
                self.json_file = spider.file_dict[file]

            elif file == "csv":
                self.csv_file = spider.file_dict[file]

            elif file == "tsv":
                self.tsv_file = spider.file_dict[file]

            elif file == "psv":
                self.psv_file = spider.file_dict[file]

    def process_item(self, item, spider):
        """
        Processes the dictionary containing the data that was scraped from a particular url
        This data is formatted and written to one or more files
        :param item: the dictionary containing the data that was scraped from a particular url
        :param spider: the spider that scraped the data from the url
        :return: void
        """
        # get the url of this target and remove the url from the item
        url = item["url"]
        del item["url"]

        # check to see if we need a csv tsv or psv file
        table_file = self.csv_file is not None or self.tsv_file is not None or self.psv_file is not None
        fields = []
        good_data = True
        if table_file:
            # check if the data is compatible with csv psv and tsv format
            match_len = None
            for key in item:
                if match_len is not None:
                    if match_len != len(item[key]):
                        good_data = False
                        break
                else:
                    match_len = len(item[key])

            if good_data:
                # add each list to the list of fields
                key_list = spider.target_dict[url]
                for key in key_list:
                    fields.append(key[0])
            else:
                messagebox.showerror("Error", "There are not an equal number of items for each css selector "
                                              "you have provided; the data cannot be converted into csv tsv "
                                              "or psv format.")

        if self.json_file is not None:
            self.write_json(item)

        if self.csv_file is not None and good_data and len(fields) > 0:
            self.write_csv(item, fields)

        if self.tsv_file is not None and good_data and len(fields) > 0:
            self.write_tsv(item, fields)

        if self.psv_file is not None and good_data and len(fields) > 0:
            self.write_psv(item, fields)

        return item

    def close_spider(self, spider):
        """
        Removes the names of the files from this pipeline when it is done processing the data sent to it by the spider
        :param spider: the spider that retrieved the data in item (this parameter will not be used)
        :return: void
        """
        self.json_file = None
        self.csv_file = None
        self.tsv_file = None
        self.psv_file = None

    def write_json(self, item):
        """
        Writes the data in the item dictionary to a file in json format
        :param item: the dictionary containing the data that was scraped from a particular url
        :return: void
        """
        with open(self.json_file, "a") as json_file:
            json_obj = json.dumps(item, indent=4)
            json_file.write(json_obj)
            json_file.write("\n")

    def write_csv(self, item, fields):
        """
        Writes the data in the item dictionary to a file in csv format
        :param item: the dictionary containing the data that was scraped from a particular url
        :param fields: the keys that corresponded to the css selectors that were used
        :return: void
        """
        with open(self.csv_file, "a") as csv_file:
            # write the header
            for i in range(len(fields)):
                if i < len(fields) - 1:
                    csv_file.write(fields[i] + ",")
                else:
                    csv_file.write(fields[i] + "\n")

            # get the length of all of the lists of data for each field
            # since we are writing to a csv file, all of the lengths will be equal so we can just grab the
            # length of the data that corresponds to the first field
            length = len(item[fields[0]])

            # write the body of the file
            for i in range(length):
                for j in range(len(fields)):
                    if j < len(fields) - 1:
                        csv_file.write(item[fields[j]][i] + ",")
                    else:
                        csv_file.write(item[fields[j]][i] + "\n")
            csv_file.write("\n")

    def write_tsv(self, item, fields):
        """
        Writes the data in the item dictionary to a file in tsv format
        :param item: the dictionary containing the data that was scraped from a particular url
        :param fields: the keys that corresponded to the css selectors that were used
        :return: void
        """
        with open(self.tsv_file, "a") as tsv_file:
            # write the header
            for i in range(len(fields)):
                if i < len(fields) - 1:
                    tsv_file.write(fields[i] + "\t")
                else:
                    tsv_file.write(fields[i] + "\n")

            # get the length of all of the lists of data for each field
            # since we are writing to a tsv file, all of the lengths will be equal so we can just grab the
            # length of the data that corresponds to the first field
            length = len(item[fields[0]])

            # write the body of the file
            for i in range(length):
                for j in range(len(fields)):
                    if j < len(fields) - 1:
                        tsv_file.write(item[fields[j]][i] + "\t")
                    else:
                        tsv_file.write(item[fields[j]][i] + "\n")
            tsv_file.write("\n")

    def write_psv(self, item, fields):
        """
        Writes the data in the item dictionary to a file in psv format
        :param item: the dictionary containing the data that was scraped from a particular url
        :param fields: the keys that corresponded to the css selectors that were used
        :return: void
        """
        with open(self.psv_file, "a") as psv_file:
            # write the header
            for i in range(len(fields)):
                if i < len(fields) - 1:
                    psv_file.write(fields[i] + "|")
                else:
                    psv_file.write(fields[i] + "\n")

            # get the length of all of the lists of data for each field
            # since we are writing to a psv file, all of the lengths will be equal so we can just grab the
            # length of the data that corresponds to the first field
            length = len(item[fields[0]])

            # write the body of the file
            for i in range(length):
                for j in range(len(fields)):
                    if j < len(fields) - 1:
                        psv_file.write(item[fields[j]][i] + "|")
                    else:
                        psv_file.write(item[fields[j]][i] + "\n")
            psv_file.write("\n")



