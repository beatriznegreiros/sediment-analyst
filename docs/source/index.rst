.. sedimentanalyst documentation parent file


sedimentanalyst
===========================================
Sediment Analyst is a modularized Python package and dash app that enables sedimentological analyses. By using sieving datasets as input, Sediment Analyst computes sediment statistics. For a complete list of computed statistics see section below (*Outputs*). For using our app, please watch our video tutorial `here <https://youtu.be/zXfN9-M12i0>`_.


.. important::

	Checkout the package `requirements <https://github.com/beatriznegreiros/sediment-analyst/blob/master/requirements.txt>`_ file in the `Github repository <https://github.com/federicascolari8/Sediment-Analyst>`_ for installing the necessary processing libraries. 
	
Outputs and Capabilities
########################

Sediment Analyst computes the following:

* A summary of sediment characteristics, which can be exported as csv:
    * d10, d16, d25, d30, d50, d84, d90.
    * Mean grain size, geometric mean grain size `(Bunte and Abt, 2001) <https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1752-1688.2001.tb05528.x>`_, grain size standard deviation, geometric standard deviation `(Frings et al., 2011) <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010WR009690>`_.
    * Sorting index, Fredle index.
    * Skewness and kurtosis.
    * Coefficient of uniformity, curvature coefficient.
    * Porosity estimators according to empirical equations available in the literature:
        * `Carling and Reader (1982) <https://onlinelibrary.wiley.com/doi/abs/10.1002/esp.3290070407>`_
        * `Wu and Wang (2006) <https://ascelibrary.org/doi/full/10.1061/%28ASCE%290733-9429%282006%29132%3A8%28858%29>`_
        * `Wooster et al. (2008) <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2006WR005815>`_: recommended for gravel-beds with geometric standard deviation between 0.004 m and 0.018 m.
        * `Frings et al. (2011) <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010WR009690>`_
    * Hydraulic conductivity estimators computed with the `Kozeny-Carman Equation <https://link.springer.com/content/pdf/10.1007%2F978-3-642-40872-4_1995-1.pdf>`_. Hydraulic Conductivity (kf) is computed in m/s with each of the above-mentioned computed porosity values.
    * Cumulative percentages according to the `Wentworth scale <https://www.planetary.org/space-images/wentworth-1922-grain-size>`_.
 * Cumulative grain size distribution curves, which are available as:
    * Static plots per sample with the *analyzer* subpackage.
    * Interactive plots with user-selected samples using the *app* subpackage.

.. toctree::
   :maxdepth: 2
   :caption: Contents
   
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
