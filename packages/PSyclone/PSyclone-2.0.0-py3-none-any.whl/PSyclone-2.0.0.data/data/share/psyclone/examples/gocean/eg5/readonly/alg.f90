PROGRAM test
  USE psy_test, ONLY: invoke_1_update_field
  USE psy_test, ONLY: invoke_0
  USE field_mod
  USE grid_mod
  USE decomposition_mod, ONLY: decomposition_type
  USE parallel_mod, ONLY: parallel_init
  USE init_field_mod, ONLY: init_field
  USE update_field_mod, ONLY: update_field
  USE read_only_verify_psy_data_mod, ONLY: read_only_verify_PSyDataInit, read_only_verify_PSyDataShutdown, &
&read_only_verify_PSyDataStart
  TYPE(r2d_field) :: a_fld, b_fld, c_fld, d_fld
  DOUBLE PRECISION :: x, y, z
  TYPE(grid_type), TARGET :: grid
  CALL parallel_init
  CALL read_only_verify_PSyDataInit
  CALL read_only_verify_PSyDataStart
  grid = grid_type(GO_ARAKAWA_C, (/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/), GO_OFFSET_SW)
  CALL grid % decompose(3, 3, 1, 1, 1, halo_width = 1)
  CALL grid_init(grid, 1.0_8, 1.0_8)
  a_fld = r2d_field(grid, GO_T_POINTS)
  b_fld = r2d_field(grid, GO_T_POINTS)
  c_fld = r2d_field(grid, GO_T_POINTS)
  d_fld = r2d_field(grid, GO_T_POINTS)
  CALL invoke_0(a_fld, b_fld, c_fld, d_fld)
  x = 0.0D0
  z = 1.0D0
  CALL invoke_1_update_field(a_fld, b_fld, c_fld, d_fld, x, y, z)
  CALL read_only_verify_PSyDataShutdown
END PROGRAM test