import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
import mpl_toolkits.axisartist.grid_finder as GF
import mpl_toolkits.axisartist.angle_helper as AH
import mpl_toolkits.axisartist.floating_axes as FA
from matplotlib.projections import PolarAxes
import numpy as np
from matplotlib.transforms import Affine2D
from matplotlib.ticker import FixedLocator, MultipleLocator, MaxNLocator
import dask.dataframe as dd


class PerformanceDiagram:
    """
    pass
    """

    def __init__(self, ax, ref, samples, markers=[], colors=[], threshold=0.1, bounds=[0, 1, 0, 1], pkwargs={}):
        self.fig = plt.gcf()
        self.ax = ax
        self.pkwargs = pkwargs
        self.threshold = threshold
        self.ref = ref
        self.markers = markers if len(markers) else ['o', 's', 'v', 'o', 's', 'v']
        self.colors = colors if len(colors) else ['tab:red', 'tab:red', 'tab:red', 'tab:green', 'tab:green', 'tab:green']
        self.samples = samples
        self.xmin, self.xmax, self.ymin, self.ymax = bounds
        self.set_up()
        self.points = []
        self.calc_draw()
        
    def set_up(self):
        rect = self.ax.get_position()
        self.ax.set_xlim([self.xmin, self.xmax])
        self.ax.set_ylim([self.ymin, self.ymax])
        self.ax.xaxis.set_major_locator(MaxNLocator(10))
        self.ax.xaxis.set_minor_locator(MaxNLocator(20))
        self.ax.yaxis.set_major_locator(MaxNLocator(10))
        self.ax.yaxis.set_minor_locator(MaxNLocator(20))
        tr = PolarAxes.PolarTransform() + Affine2D().translate(self.xmin, -self.ymin) + Affine2D().scale(self.xmax-self.xmin, self.ymax-self.ymin)
        extreme_finder = AH.ExtremeFinderCycle(20, 20,
                                               lon_cycle=10,
                                               lat_cycle=None,
                                               lon_minmax=(0, np.pi / 2),
                                               lat_minmax=(0, np.inf)
                                               )
        Blocs = [10, 5, 3, 2, 1.5, 1.3, 1, 0.8, 0.5, 0.3]
        Tlocs = np.arctan(Blocs)
        gl1 = GF.FixedLocator(Tlocs)
        gl2 = GF.FixedLocator([])
        tf1 = GF.DictFormatter(dict(zip(Tlocs, np.array(Blocs))))
        grid_helper = AA.GridHelperCurveLinear(tr,
                                            extreme_finder=extreme_finder,
                                            grid_locator1=gl1,
                                            grid_locator2=gl2,
                                            tick_formatter1=tf1
                                            )
        ax = self.fig.add_axes(rect, axes_class=AA.Axes, grid_helper=grid_helper, facecolor='none')
        ax.grid(True, linestyle='--')
        ax.axis['top'].get_helper().nth_coord_ticks = 0
        ax.axis['right'].get_helper().nth_coord_ticks = 0
        ax.axis["top"].toggle(all=True)
        ax.axis["right"].toggle(all=True)
        ax.axis["right", "top"].major_ticklabels.set_pad(8)
        ax.axis["left", "bottom"].toggle(all=False)
        # CSI
        sr, pod = np.linspace(self.xmin, self.xmax)[1:], np.linspace(self.ymin, self.ymax)[1:]  # 避免出现0作分母
        SR, POD = np.meshgrid(sr, pod)
        CSI = 1 / (1/SR + 1/POD - 1)
        cs = self.ax.contour(SR, POD, CSI, colors='gray', linestyles='--', linewidths=0.5)
        self.ax.clabel(cs, levels=cs.levels, colors='gray')
        
    
    def calc_draw(self):
        mask_ref = self.ref >= self.threshold
        for col, marker, color in zip(self.samples.columns, self.markers, self.colors):
            mask_sample = self.samples[col] > self.threshold
            A = mask_ref[mask_sample].sum()
            B = mask_sample[~mask_ref].sum()
            C = mask_ref[~mask_sample].sum()
            POD = A / (A + C)
            SR = A / (A + B)
            print(SR, POD)
            p, = self.ax.plot(SR, POD, linestyle='', marker=marker, color=color, markersize=8, zorder=12, **self.pkwargs)
            p.set_label(col)
            self.points.append(p)

if __name__ == "__main__":
    print('read data')
    df = dd.read_csv(
        'F:/MeteorologicalData/point-grid/station-6satellite-pure-BeijingTime-New.csv').head(1000000000)
    print(df)
    fig, ax = plt.subplots(dpi=123)
    dia = PerformanceDiagram(ax, df.iloc[:, 5], df.iloc[:, 6:], bounds=[0, 1, 0, 1])
    fig.legend(dia.points, [p.get_label() for p in dia.points], loc='lower center',
               ncol=7, frameon=False, bbox_to_anchor=(0.1, 0, 0.8, 0.1))
    plt.show()
