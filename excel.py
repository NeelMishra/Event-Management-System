from openpyxl import load_workbook

def return_excel_info(workbook_name):
    #Loading the source sheet

    wb = load_workbook(workbook_name)


    #Referencing the first sheet

    sheet = wb.worksheets[0]

    #Initializing the list which has to be returned.

    return_list = []

    #Initializing the number of rows, cols, and the location of initial cell

    row = 0
    col = 0
    cell = 'A' + str(row+1)

    #Initializing the logic of the excel module

    while(sheet[cell].value != None ):

    #Addition of new cell in our list data structure is done.

        return_list.append([])
    #Iterative logic to reiterate until the value of corresponding column is none

        while(sheet[cell].value != None):
            return_list[row].append(sheet[cell].value)
            cell = chr(65+ col + 1) + str(row+1)
            col += 1

    #Iterative initialization of col no to 0, cell to the value of A + row, and row is incremented.

        col = 0
        row += 1
        cell = 'A' + str(row+1) 

    return return_list, return_list[0]
