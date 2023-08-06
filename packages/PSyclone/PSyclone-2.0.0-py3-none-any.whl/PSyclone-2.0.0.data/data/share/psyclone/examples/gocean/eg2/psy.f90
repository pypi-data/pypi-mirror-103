  MODULE psy_alg
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0_inc_field(fld1, nx, ny, this_step)
      USE inc_field_0_mod, ONLY: inc_field_0_code
      TYPE(r2d_field), intent(inout) :: fld1
      INTEGER, intent(inout) :: nx, ny, this_step
      INTEGER j
      INTEGER i
      !$acc enter data copyin(fld1,fld1%data,nx,ny,this_step)
      fld1%data_on_device = .true.
      !
      !$acc parallel default(present)
      !$acc loop independent collapse(2)
      DO j=fld1%internal%ystart,fld1%internal%ystop
        DO i=fld1%internal%xstart,fld1%internal%xstop
          CALL inc_field_0_code(i, j, fld1%data, nx, ny, this_step)
        END DO
      END DO
      !$acc end parallel
    END SUBROUTINE invoke_0_inc_field
  END MODULE psy_alg