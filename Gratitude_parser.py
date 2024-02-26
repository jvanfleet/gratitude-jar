import csv
import random
from datetime import datetime
import os
import shutil

# print(random.__all__)

starting_file = "Gratitude.csv"
output_file_1 = "Gratitude_output_1.csv"
output_file_2 = "Gratitude_output_2.csv"
output_file_3 = "Gratitude_output_3.csv"

def Is_Empty(lis1):
    if not lis1:
        return 1
    else:
        return 0

def Select_Gratitude(input_file, output_file):
    # read in the csv file as a list (it has two fields: Used_flag, Gratitude)
    # print("")
    # print("Processing files.")

    list_of_avail_gratitudes = []
    # print("Initial List of available gratitudes:", list_of_avail_gratitudes)

    with open(input_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            # print(line["Used_Flag"])
            if (line["Used_Flag"]) == 'FALSE':
                # print("In the first read, this Gratitude was already used: ", line)
                # print("Current Line Num:", csv_reader.line_num-1)
                list_of_avail_gratitudes.append(csv_reader.line_num-1)
                # print("Current List of available gratitudes:", list_of_avail_gratitudes)

# JEFF - Account for the situation when the list of available gratitudes is empty
        if Is_Empty(list_of_avail_gratitudes):
            print('WARNING - out of Gratitudes')
            return False
        else:
            todays_gratitude_num = random.choice(list_of_avail_gratitudes)
            # print("Today's Gratitude Number is:", todays_gratitude_num)

    with open(input_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open(output_file, 'w', newline='') as new_file:
            fieldnames = ['Used_Flag', 'Gratitude']
            csv_writer = csv.DictWriter(new_file, fieldnames)

            csv_writer.writeheader()

            for line in csv_reader:
                # print("Gratitude line in read file is:", csv_reader.line_num-1, line)
                if(line['Used_Flag']) == 'TRUE':
                    # print("this Gratitude was used previously: ", line)
                    csv_writer.writerow({'Used_Flag': 'TRUE', 'Gratitude': line['Gratitude']})
                    # next(csv_reader)
                elif(csv_reader.line_num-1) == todays_gratitude_num:
                    print(line['Gratitude'])
                    csv_writer.writerow({'Used_Flag': 'TRUE', 'Gratitude': line['Gratitude']})
                else:
                    csv_writer.writerow({'Used_Flag': line['Used_Flag'], 'Gratitude': line['Gratitude']})

        # print(line)
        # for line in csv_reader:
        #     print(line)
        #     print(csv_reader.line_num)

    return True

final_file = starting_file
was_at_least_one_gratitude = False

if Select_Gratitude(starting_file, output_file_1) == True:
    # print("1st call is True")
    was_at_least_one_gratitude = True
    final_file = output_file_1
    if Select_Gratitude(output_file_1, output_file_2) == True:
        # print("2nd call is True")
        final_file = output_file_2
        if Select_Gratitude(output_file_2, output_file_3) == True:
            # print("3rd call is True")
            final_file = output_file_3

# print("Final File is: ", final_file)
# rename starting_file to "Gratitude_yyyymmdd.csv"
# rename outputfile_3 to starting_file

if was_at_least_one_gratitude: #therefore, the system needs to update the original gratitude file
    new_filename = os.path.splitext(starting_file)[0]
    extension = os.path.splitext(starting_file)[1]
    # print(new_filename)
    # print(extension)
    # print(new_filename + "_" + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + extension)

    # path
    # path = './'

    # List files and directories in path
    # print("Before copying file:")
    # print(os.listdir(path))

    # Source path
    source = starting_file

    # Destination path
    destination = new_filename + "_" + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + extension
    # _%H:%M:%S

    # Copy the content of source to destination
    dest = shutil.copyfile(source, destination)

    #rename latest file to original file
    if final_file != starting_file:
        print("Starting File:", starting_file)
        print("Final File   :", final_file)
        dest = shutil.copyfile(final_file, starting_file)

    # make a list of available gratitudes (i.e, those not marked "Used")
    # use random number to select gratitude
    # print the gratitude, mark its Used_Flag = True, such that there is one less gratitude available in the list
    # regenerate list of available gratitudes
    # then loop and grab the next gratitude until we have printed and used all 3
    # end loop and write the file back out
