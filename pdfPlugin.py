from fpdf import FPDF
from imagePlugin import generateImageFromText


def add_cell(pdf, width, line_height, content, border, align, lowest_point, highest_point):
    pdf.multi_cell(width, line_height, content, border=border,
                   align=align, ln=0, max_line_height=pdf.font_size*1.25)
    current_x = pdf.get_x()
    current_y = pdf.get_y()
    if current_y > lowest_point:
        lowest_point = current_y
        print("new lowest point:", lowest_point)
    pdf.set_xy(current_x, highest_point)
    print("row x", pdf.get_x(), "row y", pdf.get_y())
    return lowest_point


def create_table(pdf: FPDF, table_data, title='', footer='', data_size=10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default', emphasize_data=[], emphasize_style=None, emphasize_color=(0, 0, 0)):
    """
    table_data: 
                list of lists with first element being list of headers
    # language_data: 
    #             list of languages of questions
    title: 
                (Optional) title of table (optional)
    footer: 
                (Optional) footer of table (optional)
    data_size: 
                the font size of table data
    title_size: 
                the font size fo the title and footer of the table
    align_data: 
                align table data
                L = left align
                C = center align
                R = right align
    align_header: 
                align table data
                L = left align
                C = center align
                R = right align
    cell_width: 
                even: evenly distribute cell/column width
                uneven: base cell size on lenght of cell/column items
                int: int value for width of each cell/column
                list of ints: list equal to number of columns with the widht of each cell / column
    x_start: 
                where the left edge of table should start
    emphasize_data:  
                which data elements are to be emphasized - pass as list 
                emphasize_style: the font style you want emphaized data to take
                emphasize_color: emphasize color (if other than black) 

    """
    default_style = pdf.font_style
    if emphasize_style == None:
        emphasize_style = default_style
    # default_font = pdf.font_family
    # default_size = pdf.font_size_pt
    # default_style = pdf.font_style
    # default_color = pdf.color # This does not work

    # Get Width of Columns
    def get_col_widths():
        col_width = cell_width
        if col_width == 'even':
            # distribute content evenly   # epw = effective page width (width of page not including margins)
            col_width = pdf.epw / len(data[0]) - 1
        elif col_width == 'uneven':
            col_widths = []

            # searching through columns for largest sized cell (not rows but cols)
            for col in range(len(table_data[0])):  # for every row
                longest = 0
                for row in range(len(table_data)):
                    cell_value = str(table_data[row][col])
                    value_length = pdf.get_string_width(cell_value)
                    if value_length > longest:
                        longest = value_length
                col_widths.append(longest + 4)  # add 4 for padding
            col_width = col_widths

            # compare columns

        elif isinstance(cell_width, list):
            col_width = cell_width  # TODO: convert all items in list to int
        else:
            # TODO: Add try catch
            col_width = int(col_width)
        return col_width

    # Convert dict to lol
    # Why? because i built it with lol first and added dict func after
    # Is there performance differences?
    if isinstance(table_data, dict):
        header = [key for key in table_data]
        data = []
        for key in table_data:
            value = table_data[key]
            data.append(value)
        # need to zip so data is in correct format (first, second, third --> not first, first, first)
        data = [list(a) for a in zip(*data)]

    else:
        header = table_data[0]
        data = table_data[1:]

    line_height = pdf.font_size * 2.5
    # line_height = pdf.font_size * 10

    col_width = get_col_widths()
    pdf.set_font('helvetica', 'B', title_size)

    # Get starting position of x
    # Determin width of table to get x starting point for centred table
    if x_start == 'C':
        table_width = 0
        if isinstance(col_width, list):
            for width in col_width:
                table_width += width
        else:  # need to multiply cell width by number of cells to get table width
            table_width = col_width * len(table_data[0])
        # Get x start by subtracting table width from pdf width and divide by 2 (margins)
        margin_width = pdf.w - table_width
        # TODO: Check if table_width is larger than pdf width

        center_table = margin_width / 2  # only want width of left margin not both
        x_start = center_table
        pdf.set_x(x_start)
    elif isinstance(x_start, int):
        pdf.set_x(x_start)
    elif x_start == 'x_default':
        x_start = pdf.set_x(pdf.l_margin)

    # TABLE CREATION #

    # add title
    if title != '':
        pdf.multi_cell(0, line_height, title, border=0,
                       align='j', ln=3, max_line_height=pdf.font_size)
        pdf.ln(line_height)  # move cursor back to the left margin
        pdf.ln(10)

    pdf.set_font('akshar', '', data_size)
    # add header
    y1 = pdf.get_y()
    if x_start:
        x_left = x_start
    else:
        x_left = pdf.get_x()
    x_right = pdf.epw + x_left

    lowest_point = pdf.get_y()
    highest_point = pdf.get_y()
    # print("header x", pdf.get_x(), "header y", pdf.get_y())

    if not isinstance(col_width, list):
        if x_start:
            pdf.set_x(x_start)
        for datum in header:
            pdf.multi_cell(col_width, line_height, datum, border=0,
                           align=align_header, ln=3, max_line_height=pdf.font_size)
            # lowest_point = add_cell(pdf, col_width, line_height, datum, 0, align_header, lowest_point, highest_point)
            x_right = pdf.get_x()
        pdf.ln(line_height)  # move cursor back to the left margin
        y2 = pdf.get_y()
        # pdf.line(x_left, y1, x_right, y1)
        # pdf.line(x_left, y2, x_right, y2)
        lowest_point += line_height/2.0

        # pdf.line(x_left, highest_point, x_right, highest_point)
        # pdf.line(x_left, lowest_point, x_right, lowest_point)
        for row in data:
            if x_start:  # not sure if I need this
                pdf.set_xy(x_start, lowest_point)
            highest_point = lowest_point
            for datum in row:
                if datum in emphasize_data:
                    pdf.set_text_color(*emphasize_color)
                    pdf.set_font(style=emphasize_style)
                    pdf.multi_cell(col_width, line_height, datum, border=0,
                                   align=align_data, ln=3, max_line_height=pdf.font_size)
                    # lowest_point = add_cell(pdf, col_width, line_height, datum, 0, align_header, lowest_point, highest_point)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font(style=default_style)
                else:
                    # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
                    pdf.multi_cell(col_width, line_height, datum, border=0,
                                   align=align_data, ln=3, max_line_height=pdf.font_size)
                    # lowest_point = add_cell(pdf, col_width, line_height, datum, 0, align_header, lowest_point, highest_point)
            pdf.ln(line_height)  # move cursor back to the left margin
            pdf.ln(line_height)
            lowest_point += line_height/2.0
            # pdf.line(x_left, lowest_point, x_right, lowest_point)
            print("making line at", lowest_point)
        pdf.set_xy(x_left, lowest_point)
    else:
        if x_start:
            pdf.set_x(x_start)
        for i in range(len(header)):
            datum = header[i]
            pdf.multi_cell(col_width[i], line_height, datum, border=0,
                           align=align_header, ln=3, max_line_height=pdf.font_size)
            # lowest_point = add_cell(pdf, col_width[i], line_height, datum, 0, align_header, lowest_point, highest_point)
            x_right = pdf.get_x()
        pdf.ln(line_height)  # move cursor back to the left margin
        # y2 = pdf.get_y()
        # pdf.line(x_left, y1, x_right, y1)
        # pdf.line(x_left, y2, x_right, y2)
        # lowest_point += line_height/2.0

        # pdf.line(x_left, highest_point, x_right, highest_point)
        # pdf.line(x_left, lowest_point, x_right, lowest_point)
        for j in range(len(data)):
            if x_start:
                pdf.set_x(x_start)
                pdf.set_xy(x_start, lowest_point)
            # highest_point = lowest_point
            row = data[j]
            has_image = False
            for i in range(len(row)):
                datum = row[i]
                if not isinstance(datum, str):
                    datum = str(datum)
                adjusted_col_width = col_width[i]
                if datum in emphasize_data:
                    pdf.set_text_color(*emphasize_color)
                    pdf.set_font(style=emphasize_style)
                    pdf.multi_cell(adjusted_col_width, line_height, datum, border=0,
                                   align=align_data, ln=3, max_line_height=pdf.font_size)
                    # lowest_point = add_cell(pdf, adjusted_col_width, line_height, datum, 0, align_header, lowest_point, highest_point)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font(style=default_style)
                else:
                    # print(datum)
                    # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
                    # if len(language_data) == 0 or i != 1 or language_data[j] != "Hindi":  # j != 1 represents this col is not question name
                    if i != 1 or j % 2 == 0:  # j != 1 represents this col is not question name
                        pdf.multi_cell(adjusted_col_width, line_height, datum, border=0,
                                       align=align_data, ln=3, max_line_height=pdf.font_size)
                    else:
                        pdf.image(generateImageFromText(datum, (adjusted_col_width - 4) * 10, line_height * 10), pdf.get_x(
                        ), pdf.get_y(), adjusted_col_width - 4, line_height)
                        pdf.multi_cell(adjusted_col_width, line_height, "", border=0,
                                       align=align_data, ln=3, max_line_height=pdf.font_size)
                        has_image = True
            if has_image:
                pdf.ln(5)
                # lowest_point = add_cell(pdf, adjusted_col_width, line_height, datum, 0, align_header, lowest_point, highest_point)
            pdf.ln(line_height)
            # lowest_point += line_height/2.0
            # pdf.line(x_left, lowest_point, x_right, lowest_point)
        # pdf.set_xy(x_left, lowest_point)
    y3 = pdf.get_y()
    # pdf.line(x_left, y3, x_right, y3)
    pdf.ln()
    pdf.multi_cell(0, line_height, footer, border=0,
                   align='j', ln=3, max_line_height=pdf.font_size)
    pdf.ln(line_height)
