PROGRAM test
  USE psy_test, ONLY: invoke_1_update_field
  USE psy_test, ONLY: invoke_0
  USE field_mod
  USE grid_mod
  USE decomposition_mod, ONLY: decomposition_type
  USE parallel_mod, ONLY: parallel_init
  USE profile_psy_data_mod, ONLY: profile_PSyDataInit, profile_PSyDataShutdown
  USE init_field_mod, ONLY: init_field
  USE update_field_mod, ONLY: update_field
  TYPE(r2d_field) :: a_fld, b_fld, c_fld, d_fld
  TYPE(grid_type), TARGET :: grid
  TYPE(decomposition_type) :: decomp
  CALL profile_PSyDataInit
  CALL parallel_init
  grid = grid_type(GO_ARAKAWA_C, (/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/), GO_OFFSET_SW)
  CALL grid % decompose(3, 3, 1, 1, 1, halo_width = 1)
  CALL grid_init(grid, 1.0_8, 1.0_8)
  a_fld = r2d_field(grid, GO_T_POINTS)
  b_fld = r2d_field(grid, GO_T_POINTS)
  c_fld = r2d_field(grid, GO_T_POINTS)
  d_fld = r2d_field(grid, GO_T_POINTS)
  CALL invoke_0(a_fld, b_fld, c_fld, d_fld)
  CALL invoke_1_update_field(a_fld, b_fld, c_fld, d_fld)
  PRINT *, a_fld % data(1 : 5, 1 : 5)
  CALL profile_PSyDataShutdown
END PROGRAM test