  MODULE psy_alg
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0_kern_use_var(fld1)
      USE data_mod, ONLY: gravity
      TYPE(r2d_field), intent(inout) :: fld1
      INTEGER j
      INTEGER i
      !$acc enter data copyin(fld1,fld1%data,gravity)
      fld1%data_on_device = .true.
      !
      !$acc parallel default(present)
      !$acc loop independent collapse(2)
      DO j=fld1%internal%ystart,fld1%internal%ystop
        DO i=fld1%internal%xstart,fld1%internal%xstop
          CALL kern_use_var_0_code(i, j, fld1%data, gravity)
        END DO
      END DO
      !$acc end parallel
    END SUBROUTINE invoke_0_kern_use_var
    SUBROUTINE kern_use_var_0_code(i, j, fld, gravity)
      INTEGER, intent(in) :: i
      INTEGER, intent(in) :: j
      REAL(KIND=go_wp), dimension(:,:), intent(inout) :: fld
      REAL(KIND=go_wp), intent(in) :: gravity

      !$acc routine
      fld(i,j) = gravity * fld(i,j)

    END SUBROUTINE kern_use_var_0_code
  END MODULE psy_alg