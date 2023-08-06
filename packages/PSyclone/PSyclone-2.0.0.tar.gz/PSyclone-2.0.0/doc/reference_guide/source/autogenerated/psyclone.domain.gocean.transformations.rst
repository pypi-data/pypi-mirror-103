==========================================
``psyclone.domain.gocean.transformations``
==========================================

.. automodule:: psyclone.domain.gocean.transformations

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.domain.gocean.transformations.gocean_extract_trans
   psyclone.domain.gocean.transformations.gocean_loop_fuse_trans
   psyclone.domain.gocean.transformations.gocean_move_iteration_boundaries_inside_kernel_trans

.. currentmodule:: psyclone.domain.gocean.transformations


Classes
=======

- :py:class:`GOceanExtractTrans`:
  GOcean1.0 API application of ExtractTrans transformation     to extract code into a stand-alone program. For example:

- :py:class:`GOMoveIterationBoundariesInsideKernelTrans`:
  Provides a transformation that moves iteration boundaries that are

- :py:class:`GOceanLoopFuseTrans`:
  GOcean API specialisation of the :py:class:`base class <LoopFuseTrans>`


.. autoclass:: GOceanExtractTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOceanExtractTrans
      :parts: 1

.. autoclass:: GOMoveIterationBoundariesInsideKernelTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOMoveIterationBoundariesInsideKernelTrans
      :parts: 1

.. autoclass:: GOceanLoopFuseTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOceanLoopFuseTrans
      :parts: 1
