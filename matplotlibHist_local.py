import os
import sys
import matplotlib.pyplot as plt
import numpy as np
sys.path.append("/usr/local/lib/root")
import ROOT
#  Root.PyConfig.IgnoreCommandLineOptions = True


def matplotlib_plotting(file_name):

    x_values_list, bin_content_list, bin_width_list, binned_data_list = [], [], [], []  # List creation

    hist_folder = ROOT.TFile.Open(file_name, 'read')  # Opens histogram file
    for k in hist_folder.GetListOfKeys():
        cat = k.ReadObj()
        if isinstance(cat, ROOT.TDirectoryFile):
            for kk in cat.GetListOfKeys():
                hist_file = hist_folder.Get("plots/" + str(kk.GetName()))  # Loops through histograms for each input file

                bin_content, bin_width = [], []  # List creation

                min_bin = hist_file.GetXaxis().GetXmin()
                max_bin = hist_file.GetXaxis().GetXmax()
                print(min_bin, max_bin, hist_file.GetEntries(), hist_file.GetNbinsX())

                for i in range(1, hist_file.GetNbinsX() + 1):
                    bin_content.append(hist_file.GetBinContent(i))
                    bin_width.append(hist_file.GetXaxis().GetBinWidth(i))  # Gets the content from each bin iteratively

                if not np.all(np.array(bin_width) == np.array(bin_width)[0]):
                    print('Bins are different sizes')  # Checks bins are all the same size
                    return True

                binned_data = [hist_file.GetBinContent(0), hist_file.GetBinContent(hist_file.GetNbinsX() + 2)]

                x_values = np.linspace(min_bin, max_bin, hist_file.GetNbinsX()+1)
                bin_content = np.array(bin_content)  # Values to plot

                print('types: ', type(x_values), type(bin_content), type(bin_width), type(binned_data))

                # use dictionarys! maybe?

                x_values_list.append(x_values[:-1])
                bin_content_list.append(bin_content)
                bin_width_list.append(bin_width[0])  # Appends to lists for output of function
                binned_data_list.append(binned_data)

    return x_values_list, bin_content_list, bin_width_list, binned_data_list


def import_files():  # Find all the ROOT files in the root_to_plt folder

    files = os.listdir('root_to_plt')
    files = sorted(files)
    files.append(len(files))  # Returns a list of files and the number of files present

    return files


histogram_list = import_files()
print(histogram_list)
nRows = int(histogram_list[-1])  # Number of different ROOT files present in the folder
del histogram_list[-1]

'''Work out how many separate columns needed'''

fig, axs = plt.subplots(nRows, 2, figsize=(10,20))

n = 0
for j in range(0, nRows):  # Plotting: j is the number of
    x, bins, width, extra = matplotlib_plotting('root_to_plt/' + histogram_list[n])
    nHist = len(x)
    for i in range(0, nHist):
        axs[j, i].bar(x[i], bins[i], width[i])
        axs[j, i].title.set_text(str(histogram_list[n]))
    n += 1

#plt.bar(x, bins, width)
plt.tight_layout()
plt.savefig('Plotstest.png')
plt.show()

