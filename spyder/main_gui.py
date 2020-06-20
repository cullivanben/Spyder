import webbrowser
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter.filedialog import asksaveasfile
from spyder.initiate_crawl import initiate_crawl


# CONSTANTS

LABEL_SIZE = 18                  # the size of the text on labels
BUTTON_SIZE = 16                 # the size of the text on buttons
Y_PAD = 15                       # the widget y padding (in pixels)
URL_WIDTH = 75                   # the width (in characters) of fields where urls are displayed
FONT = "Roboto"                  # the font of all the text
PRIMARY_COLOR = "#ffffff"        # the primary text color
SECONDARY_COLOR = "#f6de63"      # the secondary text color
WINDOW_BACKGROUND = "#545454"    # the background color
SELECT_COLOR = "#696969"         # the background color of list items when they are selected


# TARGET DICTIONARY
# this will hold all of the targets that the user creates
# when the user hits "crawl" these targets will all be crawled and the output will be stored in the desired file types
target_dict = {}
url_list = []


# CALLBACKS

def crawl_callback():
    """
    This function is called when the user presses "Crawl"
    It initiates the crawl process with the targets that the user has input
    :return: void
    """
    # if there are no targets
    if not target_dict or len(url_list) == 0:
        messagebox.showinfo("Targets Must Be Specified", "In order to crawl with Spyder you must specify at "
                                                         "least one target.")
        return

    # determine which file types have been selected
    json = json_selected.get() == 1
    csv = csv_selected.get() == 1
    tsv = tsv_selected.get() == 1
    psv = psv_selected.get() == 1

    if not json and not csv and not tsv and not psv:
        messagebox.showinfo("Output Format Required", "You must specify an output format.")
        return

    # create a dictionary to hold the names of the files that will be created
    file_dict = {}

    if json:
        json_file = asksaveasfile(mode="w", title="JSON file", defaultextension=".json")
        if json_file is not None:
            file_dict["json"] = json_file.name
            json_file.close()
    if csv:
        csv_file = asksaveasfile(mode="w", title="CSV file", defaultextension=".csv")
        if csv_file is not None:
            file_dict["csv"] = csv_file.name
            csv_file.close()
    if tsv:
        tsv_file = asksaveasfile(mode="w", title="TSV file", defaultextension=".tsv")
        if tsv_file is not None:
            file_dict["tsv"] = tsv_file.name
            tsv_file.close()
    if psv:
        psv_file = asksaveasfile(mode="w", title="PSV file", defaultextension=".psv")
        if psv_file is not None:
            file_dict["psv"] = psv_file.name
            psv_file.close()
        else:
            print("it was none")

    # make sure the user saved at least one file
    if not file_dict:
        messagebox.showinfo("File Must Be Provided", "You must provide a file for the output.")
        return

    # clear the list box
    list_box.delete(0, END)

    # start the Spyder
    initiate_crawl(url_list, target_dict, file_dict)

    # inform the user that crawling is finished
    messagebox.showinfo("Finished", "Done crawling, you may now view your output files as long as no errors "
                                    "have been raised.")

    # terminate the program, it is finished
    root.destroy()


def add_target_callback():
    """
    This function is called when the user presses "Add Target"
    It adds the url and the css selector key-pairs to the target dictionary: target_dict
    :return: void
    """
    # make sure the user provided input
    if len(selection_entry.get().strip()) == 0 or len(url_entry.get().strip()) == 0:
        messagebox.showinfo("Arguments Required", "You must pass in a URL and at least one CSS selector key-pair.")
        return

    # extract the url
    url = url_entry.get().strip()

    # confirm that the user only input one url
    for c in url:
        if c == " ":
            messagebox.showinfo("One URL per Target", "You can only add one url per target.")
            return

    # extract the css selectors
    selectors = parse_css_selectors(selection_entry.get())

    # if the selectors were passed in in the incorrect format
    if selectors is None:
        messagebox.showinfo("Use Proper Format", "You must pass in CSS selector groups in the Spyder "
                                                 "CSS selector format.")
        return

    # add the url and its corresponding selectors to the target dict
    target_dict[url] = selectors

    # add the url to the url list
    url_list.append(url)

    # add the url to the list box of targets
    list_box.insert(END, url)

    # clear the input fields
    url_entry.delete(0, END)
    selection_entry.delete(0, END)


def remove_target_callback():
    """
    This function is called when the user presses "Remove"
    Removes this target from the target dictionary and also removes it from the list box
    :return: void
    """
    # if the user has not selected a target to delete, do nothing
    if len(list_box.curselection()) < 1:
        return

    # get the index of the selected item
    index = list_box.curselection()[0]

    # get the url at that index in the list box
    url = list_box.get(index)

    # remove the url from the target_dict
    if url in target_dict:  # this check avoids a KeyError if the url is not found, this should always evaluate to True
        del target_dict[url]

    # remove the url from the url list
    if index < len(url_list):
        del url_list[index]

    # remove the url from the list box
    if index < list_box.size():
        list_box.delete(index)


def docs_callback():
    """
    This is called when the user clicks to view the Docs
    It opens the user's browser to the README.md containing the Spyder documentation
    :return:
    """
    webbrowser.open_new("https://github.com/cullivanben/Spyder/blob/master/README.md")


# HELPERS

def parse_css_selectors(selectors):
    """
    This function parses the css selector input
    :param selectors: a string containing the css selectors that the user wants to use
    :return: a list that contains lists of each css selector key-pair
    """
    clusters = selectors.split(", ")
    parsed = []
    for cluster in clusters:
        if len(cluster) < 2 or cluster[0] != "(" or cluster[len(cluster) - 1] != ")":
            return None
        split_list = cluster[1:len(cluster) - 1].split("=")
        if len(split_list) != 2:
            return None
        parsed.append(split_list)
    return parsed


# GUI SCRIPT

# create the window object
root = Tk()
# set the window title
root.title("Spyder")
# set the window dimensions
root.geometry("1000x600")
# configure the window properties
root["background"] = WINDOW_BACKGROUND

# create the gui application
# define the sections
target_grid = Frame(root, bg=WINDOW_BACKGROUND)
output_row = Frame(root, bg=WINDOW_BACKGROUND, pady=Y_PAD)
status_row = Frame(root, bg=WINDOW_BACKGROUND)

# set up the logo
logo = ImageTk.PhotoImage(Image.open("spyder_logo.png"))
canvas = Canvas(root, bg=WINDOW_BACKGROUND, highlightthickness=0, width=296, height=106)
canvas.create_image(148, 53, image=logo)

# set up the top row
ultimate_label = Label(root, text="The ultimate tool for efficiently crawling the web.",
                       font=(FONT, LABEL_SIZE), fg=PRIMARY_COLOR, bg=WINDOW_BACKGROUND, pady=Y_PAD)

# the add target button
add_button = Button(root, text="Add Target", command=add_target_callback, font=(FONT, BUTTON_SIZE))

# set up the target grid

# the top left sector, consisting of two labels
top_left = Frame(target_grid, bg=WINDOW_BACKGROUND, pady=Y_PAD//2)
Label(top_left, text="Target URL: ", font=(FONT, LABEL_SIZE), fg=PRIMARY_COLOR,
      bg=WINDOW_BACKGROUND).grid(row=0, column=0, sticky=W)
Label(top_left, text="CSS selectors: ", font=(FONT, LABEL_SIZE), fg=PRIMARY_COLOR,
      bg=WINDOW_BACKGROUND).grid(row=1, column=0, sticky=W)
top_left.grid(row=0, column=0)

# the top right sector, consisting of two entry fields
top_right = Frame(target_grid, bg=WINDOW_BACKGROUND, pady=Y_PAD//2)
url_entry = Entry(top_right, width=URL_WIDTH, fg=SECONDARY_COLOR, bg=WINDOW_BACKGROUND, selectbackground=SELECT_COLOR)
url_entry.grid(row=0, column=0)
selection_entry = Entry(top_right, width=URL_WIDTH, fg=SECONDARY_COLOR, bg=WINDOW_BACKGROUND,
                        selectbackground=SELECT_COLOR)
selection_entry.grid(row=1, column=0)
top_right.grid(row=0, column=1)

# the bottom left sector, consisting of one label
bottom_left = Frame(target_grid, bg=WINDOW_BACKGROUND, pady=Y_PAD)
Label(bottom_left, text="Targets: ", font=(FONT, LABEL_SIZE), fg=PRIMARY_COLOR,
      bg=WINDOW_BACKGROUND).grid(row=0, column=0, sticky=W)
Button(bottom_left, text="Remove", command=remove_target_callback,
       font=(FONT, BUTTON_SIZE)).grid(row=1, column=0)
bottom_left.grid(row=1, column=0, sticky=W)

# the bottom right sector, consisting of a list box and a scroll bar
bottom_right = Frame(target_grid, bg=WINDOW_BACKGROUND, pady=Y_PAD)
scrollbar = Scrollbar(bottom_right, orient=VERTICAL)
list_box = Listbox(bottom_right, yscrollcommand=scrollbar.set, width=URL_WIDTH, height=5, bg=WINDOW_BACKGROUND,
                   fg=SECONDARY_COLOR, selectbackground=SELECT_COLOR)
scrollbar["command"] = list_box.yview
scrollbar.pack(side=RIGHT, fill=Y)
list_box.pack(side=LEFT, fill=BOTH)
bottom_right.grid(row=1, column=1)

# set up the output row
Label(output_row, text="Select your desired output file types: ", font=(FONT, LABEL_SIZE),
      fg=PRIMARY_COLOR, bg=WINDOW_BACKGROUND).pack()
output_frame = Frame(output_row, bg=WINDOW_BACKGROUND)
json_selected = IntVar()
csv_selected = IntVar()
tsv_selected = IntVar()
psv_selected = IntVar()
Checkbutton(output_frame, text="JSON", font=(FONT, BUTTON_SIZE), bg=WINDOW_BACKGROUND, fg=PRIMARY_COLOR,
            variable=json_selected).grid(row=0, column=0)
Checkbutton(output_frame, text="CSV", font=(FONT, BUTTON_SIZE), bg=WINDOW_BACKGROUND, fg=PRIMARY_COLOR,
            variable=csv_selected).grid(row=0, column=1)
Checkbutton(output_frame, text="TSV", font=(FONT, BUTTON_SIZE), bg=WINDOW_BACKGROUND, fg=PRIMARY_COLOR,
            variable=tsv_selected).grid(row=0, column=2)
Checkbutton(output_frame, text="PSV", font=(FONT, BUTTON_SIZE), bg=WINDOW_BACKGROUND, fg=PRIMARY_COLOR,
            variable=psv_selected).grid(row=0, column=3)
output_frame.pack()

# set up the crawl button
crawl_button = Button(root, text="Crawl", command=crawl_callback, font=(FONT, BUTTON_SIZE))

# set up the instruction label
instruction_label = Label(root, text="To view the full docs including the Spyder CSS Selector format and Crawling"
                                     " rules, click below.",
                          font=(FONT, LABEL_SIZE), fg=PRIMARY_COLOR, bg=WINDOW_BACKGROUND, pady=Y_PAD)

# set up the docs button
docs_button = Button(root, text="Docs", command=docs_callback, font=(FONT, BUTTON_SIZE))

# pack the frames that have their master set to the window
canvas.pack()
ultimate_label.pack()
add_button.pack()
target_grid.pack()
output_row.pack()
crawl_button.pack()
status_row.pack()
instruction_label.pack()
docs_button.pack()

# start the application
root.mainloop()
