PROGRAM alg
  USE psy_alg, ONLY: invoke_0_inc_field
  USE kind_params_mod, ONLY: go_wp
  USE parallel_mod
  USE grid_mod
  USE field_mod, ONLY: r2d_field, GO_T_POINTS
  USE gocean_mod, ONLY: gocean_initialise
  USE inc_field_mod, ONLY: inc_field
  IMPLICIT NONE
  TYPE(decomposition_type) :: decomp
  INTEGER :: my_rank
  INTEGER :: istp, ierr, this_step
  INTEGER :: jpiglo, jpjglo
  INTEGER, PARAMETER :: nsteps = 10
  INTEGER, ALLOCATABLE, DIMENSION(:, :) :: tmask
  TYPE(r2d_field) :: fld1
  TYPE(grid_type), TARGET :: grid1
  INTEGER :: nx, ny
  jpiglo = 50
  jpjglo = 50
  CALL gocean_initialise
  grid1 = grid_type(GO_ARAKAWA_C, (/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/), GO_OFFSET_SW)
  CALL grid1 % decompose(jpiglo, jpjglo)
  my_rank = get_rank()
  ALLOCATE(tmask(grid1 % subdomain % global % nx, grid1 % subdomain % global % ny), STAT = ierr)
  IF (ierr /= 0) THEN
    STOP 'Failed to allocate T mask'
  END IF
  tmask(:, :) = 0
  CALL grid_init(grid1, 1000.0_go_wp, 1000.0_go_wp, tmask)
  fld1 = r2d_field(grid1, GO_T_POINTS)
  fld1 % data(:, :) = 0.0_go_wp
  nx = fld1 % whole % nx
  ny = fld1 % whole % ny
  DO istp = 1, nsteps
    this_step = istp
    CALL invoke_0_inc_field(fld1, nx, ny, this_step)
  END DO
  WRITE(*, FMT = *) "nsteps = ", nsteps, "field(2,2) = ", fld1 % data(2, 2)
END PROGRAM alg