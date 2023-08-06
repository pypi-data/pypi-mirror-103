===================
``psyclone.psyGen``
===================

.. automodule:: psyclone.psyGen

   .. contents::
      :local:

.. currentmodule:: psyclone.psyGen


Classes
=======

- :py:class:`PSyFactory`:
  Creates a specific version of the PSy. If a particular api is not

- :py:class:`PSy`:
  Base class to help manage and generate PSy code for a single

- :py:class:`Invokes`:
  Manage the invoke calls.

- :py:class:`Invoke`:
  Manage an individual invoke call.

- :py:class:`InvokeSchedule`:
  Stores schedule information for an invocation call. Schedules can be

- :py:class:`Directive`:
  Base class for all Directive statements.

- :py:class:`ACCDirective`:
  Base class for all OpenACC directive statements. 

- :py:class:`ACCEnterDataDirective`:
  Abstract class representing a "!$ACC enter data" OpenACC directive in

- :py:class:`ACCParallelDirective`:
  Class representing the !$ACC PARALLEL directive of OpenACC

- :py:class:`ACCLoopDirective`:
  Class managing the creation of a '!$acc loop' OpenACC directive.

- :py:class:`OMPDirective`:
  Base class for all OpenMP-related directives

- :py:class:`OMPParallelDirective`:
  Base class for all OpenMP-related directives

- :py:class:`OMPDoDirective`:
  Class representing an OpenMP DO directive in the PSyclone AST.

- :py:class:`OMPParallelDoDirective`:
  Class for the !$OMP PARALLEL DO directive. This inherits from

- :py:class:`GlobalSum`:
  Generic Global Sum class which can be added to and manipulated

- :py:class:`HaloExchange`:
  Generic Halo Exchange class which can be added to and

- :py:class:`Kern`:
  Base class representing a call to a sub-program unit from within the

- :py:class:`CodedKern`:
  Class representing a call to a PSyclone Kernel with a user-provided

- :py:class:`InlinedKern`:
  A class representing a kernel that is inlined. This is used by

- :py:class:`BuiltIn`:
  Parent class for all built-ins (field operations for which the user

- :py:class:`Arguments`:
  Arguments abstract base class.

- :py:class:`DataAccess`:
  A helper class to simplify the determination of dependencies due to

- :py:class:`Argument`:
  Argument base class

- :py:class:`KernelArgument`:
  Argument base class

- :py:class:`TransInfo`:
  This class provides information about, and access, to the available

- :py:class:`Transformation`:
  Abstract baseclass for a transformation. Uses the abc module so it

- :py:class:`DummyTransformation`:
  Dummy transformation use elsewhere to keep pyreverse happy.

- :py:class:`ACCKernelsDirective`:
  Class representing the !$ACC KERNELS directive in the PSyIR.

- :py:class:`ACCDataDirective`:
  Class representing the !$ACC DATA ... !$ACC END DATA directive


.. autoclass:: PSyFactory
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: PSyFactory
      :parts: 1

.. autoclass:: PSy
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: PSy
      :parts: 1

.. autoclass:: Invokes
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Invokes
      :parts: 1

.. autoclass:: Invoke
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Invoke
      :parts: 1

.. autoclass:: InvokeSchedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: InvokeSchedule
      :parts: 1

.. autoclass:: Directive
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Directive
      :parts: 1

.. autoclass:: ACCDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCDirective
      :parts: 1

.. autoclass:: ACCEnterDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCEnterDataDirective
      :parts: 1

.. autoclass:: ACCParallelDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCParallelDirective
      :parts: 1

.. autoclass:: ACCLoopDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCLoopDirective
      :parts: 1

.. autoclass:: OMPDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPDirective
      :parts: 1

.. autoclass:: OMPParallelDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPParallelDirective
      :parts: 1

.. autoclass:: OMPDoDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPDoDirective
      :parts: 1

.. autoclass:: OMPParallelDoDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPParallelDoDirective
      :parts: 1

.. autoclass:: GlobalSum
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GlobalSum
      :parts: 1

.. autoclass:: HaloExchange
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HaloExchange
      :parts: 1

.. autoclass:: Kern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Kern
      :parts: 1

.. autoclass:: CodedKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CodedKern
      :parts: 1

.. autoclass:: InlinedKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: InlinedKern
      :parts: 1

.. autoclass:: BuiltIn
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: BuiltIn
      :parts: 1

.. autoclass:: Arguments
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Arguments
      :parts: 1

.. autoclass:: DataAccess
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataAccess
      :parts: 1

.. autoclass:: Argument
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Argument
      :parts: 1

.. autoclass:: KernelArgument
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernelArgument
      :parts: 1

.. autoclass:: TransInfo
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TransInfo
      :parts: 1

.. autoclass:: Transformation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Transformation
      :parts: 1

.. autoclass:: DummyTransformation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DummyTransformation
      :parts: 1

.. autoclass:: ACCKernelsDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCKernelsDirective
      :parts: 1

.. autoclass:: ACCDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCDataDirective
      :parts: 1
