========================================
``psyclone.domain.nemo.transformations``
========================================

.. automodule:: psyclone.domain.nemo.transformations

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.domain.nemo.transformations.create_nemo_kernel_trans
   psyclone.domain.nemo.transformations.nemo_allarrayrange2loop_trans
   psyclone.domain.nemo.transformations.nemo_arrayrange2loop_trans
   psyclone.domain.nemo.transformations.nemo_outerarrayrange2loop_trans

.. currentmodule:: psyclone.domain.nemo.transformations


Classes
=======

- :py:class:`CreateNemoKernelTrans`:
  Transform a generic PSyIR Schedule into a NEMO Kernel. For example:

- :py:class:`NemoAllArrayRange2LoopTrans`:
  Provides a transformation for all PSyIR Array Ranges in an

- :py:class:`NemoArrayRange2LoopTrans`:
  Provides a transformation from a PSyIR ArrayReference Range to a

- :py:class:`NemoOuterArrayRange2LoopTrans`:
  Provides a transformation from the outermost PSyIR ArrayReference


.. autoclass:: CreateNemoKernelTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CreateNemoKernelTrans
      :parts: 1

.. autoclass:: NemoAllArrayRange2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoAllArrayRange2LoopTrans
      :parts: 1

.. autoclass:: NemoArrayRange2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoArrayRange2LoopTrans
      :parts: 1

.. autoclass:: NemoOuterArrayRange2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoOuterArrayRange2LoopTrans
      :parts: 1
