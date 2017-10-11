from os import remove
from os import rename

import cairo
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileMerger


def output_2D_list(list2d):
    output = ""
    for item in list2d:
        for cell in item:
            output += str(cell) + ","
        # remove unnecessary "," at the end of each line
        output = output[:-1]
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
    residue_totals = []
    totals = []

    if avrgs:
        residue_average_totals = []
        average_totals = []

    last_res = ""
    out = ""

    for line in output:
        l = line
        if line[0].isdigit():

            res = line.split('@')[0]
            if last_res == "":
                last_res = res

            # behavior if a new residue starts
            if last_res != res:
                last_res = res
                if not totals:
                    totals = [0] * len(residue_totals)
                    if avrgs:
                        average_totals = [0] * len(residue_average_totals)


                # add line with sum of contacts a selected residue
                out += "SUM"

                for i in range(0, len(residue_totals)):
                    totals[i] += residue_totals[i]
                    out += "," + str(residue_totals[i])
                if avrgs:
                    for i in range(0, len(residue_average_totals)):
                        average_totals[i] += residue_average_totals[i]
                        out += "," + str(residue_average_totals[i])
                out += "\n"

                # add line with percentage values
                percentages = [0]
                for i in range(1, len(residue_totals)):
                    percentage = (residue_totals[0] - residue_totals[i]) * 100 / residue_totals[0]
                    percentages.append(percentage)
                if avrgs:
                    percentages.append(0)
                    for i in range(1, len(residue_average_totals)):
                        percentage = (residue_average_totals[0] - residue_average_totals[i]) * 100 / \
                                     residue_average_totals[0]
                        percentages.append(percentage)

                for item in percentages:
                    out += "," + str(round(item, 2)) + "%"
                out += "\n\n"
                residue_totals = []
                if avrgs:
                    residue_average_totals = []

            line = line.split(',')[1:]
            if avrgs:
                middle = len(line) / 2
            else:
                middle = len(line)

            if not residue_totals:
                residue_totals = [0] * middle

            for i in range(0, middle):
                residue_totals[i] += float(line[i])

            if avrgs:
                if not residue_average_totals:
                    residue_average_totals = [0] * middle
                for i in range(0, middle):
                    residue_average_totals[i] += float(line[i + middle])

        out += l + "\n"

    # handling of last residue
    out += "SUM"
    for item in residue_totals:
        out += "," + str(item)
    if avrgs:
        for item in residue_average_totals:
            out += "," + str(item)
    out += "\n"

    # add line with percentage values
    percentages = [0]
    for i in range(1, len(residue_totals)):
        percentage = (residue_totals[0] - residue_totals[i]) * 100 / residue_totals[0]
        percentages.append(percentage)
    if avrgs:
        percentages.append(0)
        for i in range(1, len(residue_average_totals)):
            percentage = (residue_average_totals[0] - residue_average_totals[i]) * 100 / residue_average_totals[0]
            percentages.append(percentage)

    for item in percentages:
        out += "," + str(round(item, 2)) + "%"
    out += "\n\nSUM"

    for item in totals:
        out += "," + str(round(item, 2))

    if avrgs:
        for item in average_totals:
            out += "," + str(round(item, 2))
    out += "\n"

    for i in range(0, len(totals)):
        percentage = (totals[0] - totals[i]) * 100 / totals[0]
        out += "," + str(round(percentage, 2)) + "%"

    if avrgs:
        for i in range(0, len(average_totals)):
            percentage = (average_totals[0] - average_totals[i]) * 100 / average_totals[0]
            out += "," + str(round(percentage, 2)) + "%"

    return out


# write occupancy data as text file
def write_output(output, file_name):
    with open(file_name, 'w') as f:
        f.write(output)


def write_percentages_quotients(output, file_name):
    residue = 0
    output = output.split('\n')
    temp = []
    totals = []
    for item in output:
        line = []
        item = item.split(',')
        if len(item[0]) > 0:
            if item[0][0].isdigit():
                residue = item[0].split('@')[0]
            elif item[0] == 'SUM':
                line.append(residue)
                line.extend(item[1:])
                totals.append(line)
                residue = ''
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
    return totals

# write occupancy data to pdf file
def output_to_pdf(output, avrgs, wat, hydro, input_list, investigated_residue):
    file_name = investigated_residue
    f = file_name + '0_occupancies.pdf'
    width = 595
    height = 842
    surface = cairo.PDFSurface(f, width, height)
    ctx = cairo.Context(surface)

    # calculate the index of the first column containing average values of the whole structure
    if avrgs:
        avrgs_start = len(input_list) + 1

    font_size = 60 / len(input_list)
    offset = (width - 70) / ((len(input_list) * 2) + 1)
    # title
    ctx.set_font_size(font_size)
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(font_size, font_size + 10)
    title = investigated_residue

    if hydro:
        title += " - hydrogen stripped"

    if wat:
        title += " - water stripped"

    ctx.show_text(title)

    ctx.set_font_size(font_size - 4)
    y = font_size + 30
    counter = 0
    for item in input_list:
        ctx.move_to(font_size, y)
        ctx.show_text("#" + str(counter) + " " + ''.join(item))
        y += font_size - 2
        counter += 1

    ctx.set_font_size(font_size)
    x = font_size
    y = y + font_size - 5
    ctx.set_font_size(font_size - 6)
    output = output.splitlines()
    pages = 0
    files = []

    for line in output:
        line = line.split(',')
        ctx.set_source_rgb(0, 0, 0)

        ctx.move_to(x, y)
        ctx.show_text(line[0])
        x += offset + 45

        # coloring, select lines with atoms as well as summation
        if len(line[0]) > 0 and line[0][0].isdigit() or line[0] == 'SUM':
            ctx.move_to(x, y)
            ctx.show_text(line[1])
            x += offset
            ctx.set_source_rgb(0, 0, 0)

            if avrgs:
                # coloring of residue contacting atom occupancies
                for i in range(2, avrgs_start):
                    value_dependent_coloring(ctx, line[1], line[i])
                    ctx.move_to(x, y)
                    ctx.show_text(line[i])
                    x += offset
                    ctx.set_source_rgb(0, 0, 0)

                # coloring of average occupancies of the whole structure
                for i in range(avrgs_start, len(line)):
                    value_dependent_coloring(ctx, line[avrgs_start], line[i])
                    ctx.move_to(x, y)
                    ctx.show_text(line[i])
                    x += offset
                    ctx.set_source_rgb(0, 0, 0)
            else:
                # coloring of residue contacting atom occupancies
                for i in range(2, len(line)):
                    value_dependent_coloring(ctx, line[1], line[i])
                    ctx.move_to(x, y)
                    ctx.show_text(line[i])
                    x += offset
                    ctx.set_source_rgb(0, 0, 0)

        else:
            for item in line[1:]:
                ctx.move_to(x, y)
                ctx.show_text(item)
                x += offset

        y += font_size - 4
        x = font_size
        if y > 820:
            pages += 1
            files.append(f)
            surface.finish()
            surface.flush()
            f = file_name + str(pages) + '_occupancies.pdf'
            files.append(f)
            surface = cairo.PDFSurface(f, 595, 842)
            ctx = cairo.Context(surface)
            ctx.set_font_size(font_size - 6)
            y = font_size + 10

    surface.finish()
    surface.flush()
    if pages > 0:
        merger = PdfFileMerger()
        for f in files:
            merger.append(f, 'rb')
        merger.write(file_name + '_occupancies.pdf')
    else:
        rename(f, file_name + '_occupancies.pdf')
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
    top_header = [""] * len(lst[0])
    header = []
    columns = len(lst[0])
    if avrgs:
        top_header[int(columns / 4)] = "Occupancies Contact Atoms"
        top_header[int(1.5 * columns / 2) - 1] = "Occupancy Averages Structure"

        for i in range(0, int(columns / 2)):
            header.append("#" + str(i))
        header = header * 2
        header = ["Atom"] + header

    else:
        top_header[int(columns / 2)] = "Occupancies Contact Atoms"
        for i in range(0, columns - 1):
            header.append("#" + str(i))
        header = ["Atom"] + header

    lst = [header] + lst
    lst = [top_header] + lst
    return lst


# defines the color of the next output
def value_dependent_coloring(ctx, value1, value2):
    if float(value1.strip("%")) > float(value2.strip("%")):
        ctx.set_source_rgb(0.9, 0, 0)
    if float(value1.strip("%")) < float(value2.strip("%")):
        ctx.set_source_rgb(0, 0.7, 0)


# plot total value
def plot_total_values(lst, trajectories, avrgs):
    fig = plt.figure()
    plt.title("Residues")
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    if avrgs:
        columns = (len(lst[0][1:]) / 2) + 1
    else:
        columns = len(lst[0][1:])

    count = 0

    NUM_COLORS = len(lst)

    cm = plt.get_cmap('Paired')
    fig = plt.figure()
    count = 1
    for item in lst[:-1]:
        color = cm(float(count) / NUM_COLORS)
        # plot residue occupancies for residue contacting atoms
        item1 = [float(x) for x in item[1:columns]]
        plt.plot(item1, c=color, label=item[0])

        # plot average values of the whole structure
        item2 = [float(x) for x in item[columns:]]
        plt.plot(item2, c=color, dashes=[30, 5, 10, 5], label='average ' + item[0])

        count += 1

    plt.xlabel('Trajectory')
    x = range(0, len(trajectories))
    plt.xticks(x, trajectories, rotation=70)
    plt.ylabel('Contacts')
    # plt.legend()

    plt.show()
