#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def lightbox(images, titles=None, labels=None, column_num=5, **kwargs):
    """
    Show the images labels in a table

    Parameters
    ----------
    images: array-like or PIL images
            images to show

    titles: list of str
            the titles of the images

    labels: list of str
            the labels of the images

    column_num: int
                the number of columns, the default is 5

    Return
    ------
    None


    Other parameters
    ----------------
    **kwargs: the parameters for matplotlib.pyplot.figure()

    ### Output
    <matplotlib object>

    """
    def ceildiv(a, b):
        return -(-a // b)

    size = len(images)

    if titles is None:
        titles = [''] * size

    if labels is None:
        labels = [''] * size

    rownumber = ceildiv(len(images), column_num)

    fig = plt.figure(**kwargs)
    fig.set_size_inches(12, 2.8 * rownumber)

    for n, (img, title, label) in enumerate(zip(images, titles, labels)):
        ax = plt.subplot(rownumber, column_num, n+1)
        cmap = None
        ax.imshow(img, cmap='gray')
        ax.set_title(label, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel(title)
