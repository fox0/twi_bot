# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

x = np.arange(0, 5.05, 0.1)
mfx = fuzz.trapmf(x, [2, 2.5, 3, 4.5])

labels = [u'центр масс', u'среднее максимума']
xvals = [
    fuzz.defuzz(x, mfx, 'centroid'),
    fuzz.defuzz(x, mfx, 'mom'),
]
colors = ['r', 'g']
ymax = [fuzz.interp_membership(x, mfx, i) for i in xvals]

plt.figure(figsize=(8, 5))

plt.plot(x, mfx, 'k')
for xv, y, label, color in zip(xvals, ymax, labels, colors):
    plt.vlines(xv, -1, y, label=label, color=color)

plt.xlabel('x')
plt.ylabel(r'$\mu$')
plt.ylim(-0.1, 1.1)
plt.legend(loc=2)

plt.grid()
plt.savefig('../img/fig5.png', dpi=300)

plt.show()
