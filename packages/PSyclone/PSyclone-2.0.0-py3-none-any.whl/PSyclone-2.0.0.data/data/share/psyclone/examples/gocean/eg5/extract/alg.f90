PROGRAM test
  USE psy_test, ONLY: invoke_1_update_field
  USE psy_test, ONLY: invoke_0
  USE field_mod
  USE grid_mod
  USE decomposition_mod, ONLY: decomposition_type
  USE parallel_mod, ONLY: parallel_init
  USE init_field_mod, ONLY: init_field
  USE update_field_mod, ONLY: update_field
  USE extract_psy_data_mod, ONLY: extract_PSyDataType, extract_PSyDataInit, extract_PSyDataShutdown
  TYPE(r2d_field) :: a_fld, b_fld, c_fld, d_fld
  DOUBLE PRECISION :: x, y
  REAL(KIND = KIND(1.0D0)) :: z
  TYPE(grid_type), TARGET :: grid
  CALL parallel_init
  CALL extract_PSyDataInit
  grid = grid_type(GO_ARAKAWA_C, (/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/), GO_OFFSET_SW)
  CALL grid % decompose(3, 3, 1, 1, 1, halo_width = 1)
  CALL grid_init(grid, 1.0_8, 1.0_8)
  a_fld = r2d_field(grid, GO_T_POINTS)
  b_fld = r2d_field(grid, GO_T_POINTS)
  c_fld = r2d_field(grid, GO_T_POINTS)
  d_fld = r2d_field(grid, GO_T_POINTS)
  CALL invoke_0(a_fld, b_fld, c_fld, d_fld)
  x = 0
  z = 1
  CALL invoke_1_update_field(a_fld, b_fld, c_fld, d_fld, x, y, z)
  PRINT *, a_fld % data(1 : 5, 1 : 5)
  CALL extract_PSyDataShutdown
END PROGRAM test