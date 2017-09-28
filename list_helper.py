#! /usr/bin/env python

def output_2D_list(list2d):
    output = ""
    for item in list2d:
        for cell in item:
            output += str(cell) + ","
        output += "\n"
    return output


def c_get(lst, column):
    outlist = []
    for item in lst:
        outlist.append(item[column])
    return outlist


# add a column to the right
def c_bind(list1, list2):
    outlist = []
    if len(list1) == len(list2):
        for i in range(0, len(list1)):
            if not isinstance(list1[i], list):
                temp1 = [list1[i]]
            else:
                temp1 = list1[i]

            if not isinstance(list2[i], list):
                temp2 = [list2[i]]
            else:
                temp2 = list2[i]

            temp1.extend(temp2)
            outlist.append(temp1)
    else:
        print "fail: lists have different lengths"

    return outlist


# delete a column
def c_del(lst, column):
    outlist = []

    for item in lst:
        outitem = item[:column]
        outitem.extend(item[column + 1:])
        outlist.append(outitem)

    return outlist


# create list with residue@atom_type and occupancies
def reformat_occupancies(occupancies):
    occ_list = []
    for item in occupancies:
        if not occ_list:
            occ_list = c_get(item, 0)
        occ_list = c_bind(occ_list, c_get(item, 1))

    res_numb = c_get(occ_list, 0)
    occ_list = c_del(occ_list, 0)
    occ_list = c_bind(res_numb, occ_list)
    occ_list = sorted(occ_list)

    top_header = ["", "", "Occupancies", ""]
    header = ["Atom", "#0", "#1", "#2"]

    occ_list = [header] + occ_list
    occ_list = [top_header] + occ_list
    return occ_list
