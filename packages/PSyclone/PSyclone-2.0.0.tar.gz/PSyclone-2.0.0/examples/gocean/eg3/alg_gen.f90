PROGRAM simple
  USE psy_simple, ONLY: invoke_0
  USE kind_params_mod, ONLY: go_wp
  USE grid_mod
  USE field_mod
  USE gocean_mod, ONLY: gocean_initialise
  USE compute_cu_mod, ONLY: compute_cu
  USE compute_cv_mod, ONLY: compute_cv
  USE compute_z_mod, ONLY: compute_z
  USE compute_h_mod, ONLY: compute_h
  IMPLICIT NONE
  TYPE(grid_type), TARGET :: model_grid
  INTEGER, ALLOCATABLE, DIMENSION(:, :) :: tmask
  TYPE(r2d_field) :: p_fld
  TYPE(r2d_field) :: u_fld, v_fld
  TYPE(r2d_field) :: cu_fld, cv_fld
  TYPE(r2d_field) :: z_fld
  TYPE(r2d_field) :: h_fld
  INTEGER :: ncycle, ierr
  INTEGER :: jpiglo, jpjglo
  jpiglo = 50
  jpjglo = 50
  CALL gocean_initialise
  model_grid = grid_type(GO_ARAKAWA_C, (/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/), GO_OFFSET_SW)
  CALL model_grid % decompose(jpiglo, jpjglo)
  ALLOCATE(tmask(model_grid % subdomain % global % nx, model_grid % subdomain % global % ny), STAT = ierr)
  IF (ierr /= 0) THEN
    STOP 'Failed to allocate T mask'
  END IF
  tmask(:, :) = 0
  CALL grid_init(model_grid, 1000.0_go_wp, 1000.0_go_wp, tmask)
  p_fld = r2d_field(model_grid, GO_T_POINTS)
  u_fld = r2d_field(model_grid, GO_U_POINTS)
  v_fld = r2d_field(model_grid, GO_V_POINTS)
  cu_fld = r2d_field(model_grid, GO_U_POINTS)
  cv_fld = r2d_field(model_grid, GO_V_POINTS)
  z_fld = r2d_field(model_grid, GO_F_POINTS)
  h_fld = r2d_field(model_grid, GO_T_POINTS)
  WRITE(*, FMT = *) "Simulation start"
  DO ncycle = 1, 100
    CALL invoke_0(cu_fld, p_fld, u_fld, cv_fld, v_fld, z_fld, h_fld)
  END DO
  WRITE(*, FMT = *) "Simulation end"
END PROGRAM simple