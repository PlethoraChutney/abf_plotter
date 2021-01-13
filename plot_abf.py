import pyabf
import sys
import pyabf.plot
import matplotlib.pyplot as plt
import argparse
import glob
import pandas as pd

def make_plot(abf_name, no_annot):
    try:
        abf = pyabf.ABF(abf_name)
    except IndexError:
        print('Must include name of file to analyze')
        sys.exit(1)

    fig, ax = plt.subplots()
    ax.plot(abf.sweepX, abf.sweepY, color = 'black')

    if not no_annot:
        # add horizontal tag lines
        yvals = []
        xmins = []
        xmaxes = []
        colors = []
        legends = []
        for i, tagTimeSec in enumerate(abf.tagTimesSec):
            start_x = abf.tagTimesSec[i]
            try:
                end_x = abf.tagTimesSec[i+1]
            except IndexError:
                end_x = max(abf.sweepX)
            comment = abf.tagComments[i]
            color = 'C%d' % (int(comment[-3]))
            yvals.append(10)
            xmins.append(start_x)
            xmaxes.append(end_x)
            colors.append(color)
            legends.append(comment[-3])

        ax.hlines(yvals, xmins, xmaxes, colors = colors, linewidths = 3)

        for y, xmin, xmax, color in zip(yvals, xmins, xmaxes, colors):
            mid = (xmin + xmax) / 2
            ax.text(mid, y + 7, color[-1], horizontalalignment = 'center')

    # this also hides the frame and axes
    pyabf.plot.scalebar(abf = abf)
    return (plt, abf)

def graphs_from_files(filenames, no_annot, filetype, save_csv):
    globs = []
    for file in filenames:
        globs.extend(glob.glob(file))

    globs = set(globs)

    for file in globs:
        plt, abf = make_plot(file, no_annot)
        plt.savefig(
            f'{file[:-4]}.{filetype}',
            dpi = 300,
            transparent = True
        )

        if save_csv:
            df = pd.DataFrame({
                'Time': abf.sweepX,
                'Signal': abf.sweepY
            })

            df['Barrel'] = 1
            for i, tagTimeSec in enumerate(abf.tagTimesSec):
                df.loc[df['Time'] > tagTimeSec, 'Barrel'] = abf.tagComments[i][-3]

            print(df)
            df.to_csv(f'{file[:-4]}.csv', index = False)

def main():
    args = parser.parse_args()
    graphs_from_files(args.files, args.no_annotations, args.filetype, args.save_csv)

parser = argparse.ArgumentParser(description='Plot ABF binary files')
parser.add_argument(
    'files',
    help = 'ABF files to analyze',
    type = str,
    nargs = '+'
)
parser.add_argument(
    '-a', '--no-annotations',
    help = 'Do not annotate with voltage levels',
    action = 'store_true'
)
parser.add_argument(
    '-f', '--filetype',
    help = 'Type of plot to save. Default pdf.',
    type = str.lower,
    choices = ['pdf', 'png', 'svg'],
    default = 'pdf'
)
parser.add_argument(
    '-c', '--save-csv',
    help = 'Save X, Y, and barrel to csv format.',
    action = 'store_true'
)

if __name__ == '__main__':
    main()
