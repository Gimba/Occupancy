from os import remove

import cairo
from PyPDF2 import PdfFileMerger


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


# merges to list using the given key_columns
def c_merge_list(lst):
    # Convert outer sublists to dictionaries
    dicts = list(map(dict, lst))

    # Get all the keys
    keys = set()
    for d in dicts:
        keys.update(d.keys())

    # Get data for each key from each dict, using 0 if a key is missing
    out_list = []
    for k in sorted(keys):
        out_list.append([k] + [d.get(k, 0) for d in dicts])

    return out_list


# create list with residue@atom_type and occupancies
def reformat_occupancies_list(occupancies):
    occ_list = []
    occupancies = tuples_list_to_list_list(occupancies)
    # for i in range(0, len(occupancies)):
    #     if not i:
    #         occ_list = occupancies[i]
    #     else:
    #         occ_list = c_merge_list(occ_list, occupancies[i], 0, 0, -1)

    occ_list = c_merge_list(occupancies)
    res_numb = c_get(occ_list, 0)
    occ_list = c_del(occ_list, 0)
    occ_list = c_bind(res_numb, occ_list)
    occ_list = sorted(occ_list)

    return occ_list


# convert tuple items of a list or a list of lists to a list
def tuples_list_to_list_list(tuples_list):
    out_list_top = []
    for item in tuples_list:
        if isinstance(item, tuple):
            out_list_top.append(list(item))
        else:
            out_list_sub = []
            for item1 in item:
                if isinstance(item1, tuple):
                    out_list_sub.append(list(item1))
            out_list_top.append(out_list_sub)
    return out_list_top

# calculate percentages and total values of occupancies
def prepare_output(output, avrgs):
    output = output.splitlines()
    init_tot = 0
    muta_tot = 0
    sim_tot = 0
    init_res = 0
    muta_res = 0
    sim_res = 0

    if avrgs:
        avg_init_tot = 0
        avg_sim_tot = 0
        avg_muta_tot = 0
        avg_init_res = 0
        avg_sim_res = 0
        avg_muta_res = 0

    last_res = ""
    out = ""

    for line in output:
        l = line
        if line[0].isdigit():
            line = line.split(',')
            init_tot += float(line[1])
            muta_tot += float(line[2])
            sim_tot += float(line[3])

            if avrgs:
                avg_init_tot += float(line[4])
                avg_muta_tot += float(line[5])
                avg_sim_tot += float(line[6])

            res = line[0].split('@')[0]
            if last_res == "":
                last_res = res

            # behavior if a new residue starts
            if last_res != res:
                last_res = res

                # add line with sum of contacts a selected residue
                out += "SUM," + str(init_res) + "," + str(muta_res) + "," + str(sim_res)
                if avrgs:
                    out += "," + str(avg_init_res) + "," + str(avg_muta_res) + "," + str(avg_sim_res)
                out += "\n"

                # add line with percentage values
                muta_res_per = (init_res - muta_res) * 100 / init_res
                sim_res_per = (init_res - sim_res) * 100 / init_res

                out += ",," + str(round(muta_res_per, 2)) + "%," + str(round(sim_res_per, 2)) + "%"
                if avrgs:
                    avg_muta_res_per = (avg_init_res - avg_muta_res) * 100 / avg_init_res
                    avg_sim_res_per = (avg_init_res - avg_sim_res) * 100 / avg_init_res
                    out += ",," + str(round(avg_muta_res_per, 2)) + "%," + str(round(avg_sim_res_per, 2)) + "%"
                out += "\n\n"

                # reset values for summing up residue contacts to start from first values of new residue
                init_res = float(line[1])
                muta_res = float(line[2])
                sim_res = float(line[3])
                if avrgs:
                    avg_init_res = float(line[4])
                    avg_muta_res = float(line[5])
                    avg_sim_res = float(line[6])
            else:
                # add up values for the current residue
                init_res += float(line[1])
                muta_res += float(line[2])
                sim_res += float(line[3])

                if avrgs:
                    avg_init_res += float(line[4])
                    avg_muta_res += float(line[5])
                    avg_sim_res += float(line[6])

        out += l + "\n"

    # handling of last residue
    out += "SUM," + str(init_res) + "," + str(muta_res) + "," + str(sim_res)
    if avrgs:
        out += "," + str(avg_init_res) + "," + str(avg_muta_res) + "," + str(avg_sim_res)
    out += "\n"

    # add line with percentage values
    muta_res_per = (init_res - muta_res) * 100 / init_res
    sim_res_per = (init_res - sim_res) * 100 / init_res
    out += ",," + str(round(muta_res_per, 2)) + "%," + str(round(sim_res_per, 2)) + "%"
    if avrgs:
        avg_muta_res_per = (avg_init_res - avg_muta_res) * 100 / avg_init_res
        avg_sim_res_per = (avg_init_res - avg_sim_res) * 100 / avg_init_res
        out += ",," + str(round(avg_muta_res_per, 2)) + "%," + str(round(avg_sim_res_per, 2)) + "%"
    out += "\n\n"

    # total values at the end of document
    out += "total," + str(init_tot) + "," + str(muta_tot) + "," + str(sim_tot)
    if avrgs:
        out += "," + str(round(avg_init_tot, 2)) + "," + str(round(avg_muta_tot, 2)) + "," + str(round(avg_sim_tot, 2))
    out += "\n"

    # total percentages
    muta_tot_per = (init_tot - muta_tot) * 100 / init_tot
    sim_tot_per = (init_tot - sim_tot) * 100 / init_tot

    out += ",," + str(round(muta_tot_per, 2)) + "%," + str(round(sim_tot_per, 2)) + "%"
    if avrgs:
        avg_muta_tot_per = (avg_init_tot - avg_muta_tot) * 100 / avg_init_tot
        avg_sim_tot_per = (avg_init_tot - avg_sim_tot) * 100 / avg_init_tot
        out += ",," + str(round(avg_muta_tot_per, 2)) + "%," + str(
            round(avg_sim_tot_per, 2)) + "%"
    out += "\n"

    return out


# write occupancy data as text file
def write_output(output, file_name):
    with open(file_name, 'w') as f:
        f.write(output)


def write_percentages_quotients(output, file_name):
    residue = 0
    output = output.split('\n')
    temp = []
    for item in output:
        line = []
        item = item.split(',')
        if len(item[0]) > 0:
            if item[0][0].isdigit():
                residue = item[0].split('@')[0]
            elif item[0] == 'total':
                residue = 'total'
        if len(item) > 2 and '%' in item[2]:
            line.append(residue)
            line.extend(item)
            temp.append(filter(None, line))
    out = []
    print temp
    for item in temp:
        muta = item[1].strip('%')
        muta_avg = item[3].strip('%')
        quot_muta = float(muta) - float(muta_avg)
        sim = item[2].strip('%')
        sim_avg = item[4].strip('%')
        quot_sim = float(sim) - float(sim_avg)
        line = item[0] + " " + str(quot_muta) + " " + str(quot_sim)
        out.append(line)
    print out
    with open(file_name, 'w') as f:
        for item in out:
            f.write(item + "\n")


# write occupancy data to pdf file
def output_to_pdf(output, file_name, avrgs, wat, hydro, input_list, investigated_residue):
    file_name = investigated_residue
    f = file_name + '0_occupancies.pdf'
    surface = cairo.PDFSurface(f, 595, 842)
    ctx = cairo.Context(surface)

    # title
    ctx.set_font_size(20)
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(20, 30)
    title = investigated_residue

    if hydro:
        title += " - hydrogen stripped"

    if wat:
        title += " - water stripped"

    ctx.show_text(title)

    ctx.set_font_size(12)
    y = 50
    counter = 0
    for item in input_list:
        ctx.move_to(20, y)
        ctx.show_text("#" + str(counter) + " " + ''.join(item))
        y += 14
        counter += 1

    ctx.set_font_size(20)
    x = 20
    y = y + 15
    ctx.set_font_size(14)
    output = output.splitlines()
    pages = 0
    files = []

    for line in output:
        line = line.split(',')
        ctx.set_source_rgb(0, 0, 0)

        ctx.move_to(x, y)
        ctx.show_text(line[0])
        x += 120

        # coloring
        if len(line[0]) > 0 and line[0][0].isdigit() or line[0] == 'SUM':
            ctx.move_to(x, y)
            ctx.show_text(line[1])
            x += 75
            ctx.set_source_rgb(0, 0, 0)

            if float(line[1]) > float(line[2]):
                ctx.set_source_rgb(0.9, 0, 0)
            if float(line[1]) < float(line[2]):
                ctx.set_source_rgb(0, 0.7, 0)
            ctx.move_to(x, y)
            ctx.show_text(line[2])
            x += 75
            ctx.set_source_rgb(0, 0, 0)

            if float(line[1]) > float(line[3]):
                ctx.set_source_rgb(0.9, 0, 0)
            if float(line[1]) < float(line[3]):
                ctx.set_source_rgb(0, 0.7, 0)
            ctx.move_to(x, y)
            ctx.show_text(line[3])
            x += 75
            ctx.set_source_rgb(0, 0, 0)

            if avrgs:
                ctx.move_to(x, y)
                ctx.show_text(str(round(float(line[4]), 2)))
                x += 75
                ctx.move_to(x, y)
                ctx.show_text(str(round(float(line[5]), 2)))
                x += 75
                ctx.move_to(x, y)
                ctx.show_text(str(round(float(line[6]), 2)))
                x += 75
        else:
            for item in line[1:]:
                ctx.move_to(x, y)
                ctx.show_text(item)
                x += 75

        y += 16
        x = 20
        if y > 820:
            pages += 1
            files.append(f)
            surface.finish()
            surface.flush()
            f = file_name + str(pages) + '_occupancies.pdf'
            files.append(f)
            surface = cairo.PDFSurface(f, 595, 842)
            ctx = cairo.Context(surface)
            ctx.set_font_size(14)
            y = 30

    surface.finish()
    surface.flush()

    merger = PdfFileMerger()
    for f in files:
        merger.append(f, 'rb')
    merger.write(file_name + '_occupancies.pdf')

    # remove merged pdf files
    for item in files:
        remove(item)



# add columns of averages to a given list
def add_averages_column(lst, avrgs):
    outlist = []
    for item in lst:
        if '@' in item[0]:
            for avrg in avrgs:
                if item[0].split('@')[1] == avrg[0]:
                    item.append(avrg[1])
                    outlist.append(item)
    return outlist


# adds header to output list, TODO headers for arbitrary many inputs
def add_headers(lst, avrgs):
    top_header = ["", "", "Occupancies", ""]
    if avrgs:
        top_header.extend(["", "Averages", "", ""])
    header = ["Atom", "#0", "#1", "#2"]
    if avrgs:
        header.extend(["#0", "#1", "#2"])

    lst = [header] + lst
    lst = [top_header] + lst
    return lst
