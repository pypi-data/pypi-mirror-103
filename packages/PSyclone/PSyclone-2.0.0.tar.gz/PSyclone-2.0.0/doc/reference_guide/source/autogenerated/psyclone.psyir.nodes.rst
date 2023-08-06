========================
``psyclone.psyir.nodes``
========================

.. automodule:: psyclone.psyir.nodes

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.psyir.nodes.array_member
   psyclone.psyir.nodes.array_mixin
   psyclone.psyir.nodes.array_of_structures_member
   psyclone.psyir.nodes.array_of_structures_mixin
   psyclone.psyir.nodes.array_of_structures_reference
   psyclone.psyir.nodes.array_reference
   psyclone.psyir.nodes.assignment
   psyclone.psyir.nodes.call
   psyclone.psyir.nodes.codeblock
   psyclone.psyir.nodes.container
   psyclone.psyir.nodes.datanode
   psyclone.psyir.nodes.extract_node
   psyclone.psyir.nodes.ifblock
   psyclone.psyir.nodes.kernel_schedule
   psyclone.psyir.nodes.literal
   psyclone.psyir.nodes.loop
   psyclone.psyir.nodes.member
   psyclone.psyir.nodes.nan_test_node
   psyclone.psyir.nodes.node
   psyclone.psyir.nodes.operation
   psyclone.psyir.nodes.profile_node
   psyclone.psyir.nodes.psy_data_node
   psyclone.psyir.nodes.ranges
   psyclone.psyir.nodes.read_only_verify_node
   psyclone.psyir.nodes.reference
   psyclone.psyir.nodes.return_stmt
   psyclone.psyir.nodes.routine
   psyclone.psyir.nodes.schedule
   psyclone.psyir.nodes.scoping_node
   psyclone.psyir.nodes.statement
   psyclone.psyir.nodes.structure_member
   psyclone.psyir.nodes.structure_reference

.. currentmodule:: psyclone.psyir.nodes


Functions
=========

- :py:func:`colored`:
  Colorize text.


.. autofunction:: colored


Classes
=======

- :py:class:`ArrayMember`:
  Node representing an access to the element(s) of an array that is a

- :py:class:`ArrayReference`:
  Node representing a reference to an element or elements of an Array.

- :py:class:`ArrayOfStructuresMember`:
  Node representing a membership expression of a parent structure where the

- :py:class:`ArrayOfStructuresReference`:
  Node representing an access to a member of one or more elements of an

- :py:class:`Assignment`:
  Node representing an Assignment statement. As such it has a LHS and RHS

- :py:class:`BinaryOperation`:
  Node representing a BinaryOperation expression. As such it has two operands

- :py:class:`Call`:
  Node representing a Call.

- :py:class:`CodeBlock`:
  Node representing some generic Fortran code that PSyclone does not

- :py:class:`Container`:
  Node representing a set of KernelSchedule and/or Container nodes,

- :py:class:`DataNode`:
  Abstract node representing a general PSyIR expression that represents a

- :py:class:`ExtractNode`:
  This class can be inserted into a Schedule to mark Nodes for     code extraction using the ExtractRegionTrans transformation. By     applying the transformation the Nodes marked for extraction become     children of (the Schedule of) an ExtractNode.

- :py:class:`IfBlock`:
  Node representing an if-block within the PSyIR. It has two mandatory

- :py:class:`KernelSchedule`:
  A KernelSchedule is the parent node of the PSyIR for Kernel source code.

- :py:class:`Literal`:
  Node representing a Literal. The value and datatype properties of

- :py:class:`Loop`:
  Node representing a loop within the PSyIR. It has 4 mandatory children:

- :py:class:`Member`:
  Node representing a membership expression of a structure.

- :py:class:`NanTestNode`:
  This class can be inserted into a Schedule to mark Nodes for

- :py:class:`NaryOperation`:
  Node representing a n-ary operation expression. The n operands are the

- :py:class:`Node`:
  Base class for a PSyIR node.

- :py:class:`Operation`:
  Abstract base class for PSyIR nodes representing operators.

- :py:class:`ProfileNode`:
  This class can be inserted into a schedule to create profiling code.

- :py:class:`PSyDataNode`:
  This class can be inserted into a schedule to instrument a set of nodes.

- :py:class:`Range`:
  The ``Range`` node is used to capture a range of integers via

- :py:class:`ReadOnlyVerifyNode`:
  This class can be inserted into a Schedule to mark Nodes for

- :py:class:`Reference`:
  Node representing a Reference Expression.

- :py:class:`Return`:
  Node representing a Return statement (subroutine break without return

- :py:class:`Routine`:
  A sub-class of a Schedule that represents a subroutine, function or

- :py:class:`Schedule`:
  Stores schedule information for a sequence of statements (supplied

- :py:class:`Statement`:
  Abstract node representing a general PSyIR Statement.

- :py:class:`StructureMember`:
  Node representing a membership expression of the parent's Reference that

- :py:class:`StructureReference`:
  Node representing a reference to a component of a structure. As such

- :py:class:`UnaryOperation`:
  Node representing a UnaryOperation expression. As such it has one operand

- :py:class:`ScopingNode`:
  Abstract node that has an associated Symbol Table to keep track of


.. autoclass:: ArrayMember
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayMember
      :parts: 1

.. autoclass:: ArrayReference
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayReference
      :parts: 1

.. autoclass:: ArrayOfStructuresMember
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayOfStructuresMember
      :parts: 1

.. autoclass:: ArrayOfStructuresReference
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayOfStructuresReference
      :parts: 1

.. autoclass:: Assignment
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Assignment
      :parts: 1

.. autoclass:: BinaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: BinaryOperation
      :parts: 1

.. autoclass:: Call
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Call
      :parts: 1

.. autoclass:: CodeBlock
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CodeBlock
      :parts: 1

.. autoclass:: Container
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Container
      :parts: 1

.. autoclass:: DataNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataNode
      :parts: 1

.. autoclass:: ExtractNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ExtractNode
      :parts: 1

.. autoclass:: IfBlock
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: IfBlock
      :parts: 1

.. autoclass:: KernelSchedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernelSchedule
      :parts: 1

.. autoclass:: Literal
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Literal
      :parts: 1

.. autoclass:: Loop
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Loop
      :parts: 1

.. autoclass:: Member
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Member
      :parts: 1

.. autoclass:: NanTestNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NanTestNode
      :parts: 1

.. autoclass:: NaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NaryOperation
      :parts: 1

.. autoclass:: Node
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Node
      :parts: 1

.. autoclass:: Operation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Operation
      :parts: 1

.. autoclass:: ProfileNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ProfileNode
      :parts: 1

.. autoclass:: PSyDataNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: PSyDataNode
      :parts: 1

.. autoclass:: Range
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Range
      :parts: 1

.. autoclass:: ReadOnlyVerifyNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ReadOnlyVerifyNode
      :parts: 1

.. autoclass:: Reference
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Reference
      :parts: 1

.. autoclass:: Return
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Return
      :parts: 1

.. autoclass:: Routine
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Routine
      :parts: 1

.. autoclass:: Schedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Schedule
      :parts: 1

.. autoclass:: Statement
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Statement
      :parts: 1

.. autoclass:: StructureMember
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StructureMember
      :parts: 1

.. autoclass:: StructureReference
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StructureReference
      :parts: 1

.. autoclass:: UnaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnaryOperation
      :parts: 1

.. autoclass:: ScopingNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ScopingNode
      :parts: 1
