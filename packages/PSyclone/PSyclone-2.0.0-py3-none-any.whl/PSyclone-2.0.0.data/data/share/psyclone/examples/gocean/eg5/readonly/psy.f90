  MODULE psy_test
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(a_fld, b_fld, c_fld, d_fld)
      USE init_field_mod, ONLY: init_field_code
      USE read_only_verify_psy_data_mod, ONLY: read_only_verify_PSyDataType
      TYPE(r2d_field), intent(inout) :: a_fld, b_fld, c_fld, d_fld
      INTEGER j
      INTEGER i
      TYPE(read_only_verify_PSyDataType), target, save :: read_only_verify_psy_data
      !
      ! ReadOnlyVerifyStart
      !
      CALL read_only_verify_psy_data%PreStart("main", "init", 4, 4)
      CALL read_only_verify_psy_data%PreDeclareVariable("a_fld%grid%gphiu", a_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreDeclareVariable("b_fld%grid%gphiu", b_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreDeclareVariable("c_fld%grid%gphiu", c_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreDeclareVariable("d_fld%grid%gphiu", d_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreDeclareVariable("a_fld%grid%gphiu", a_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreDeclareVariable("b_fld%grid%gphiu", b_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreDeclareVariable("c_fld%grid%gphiu", c_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreDeclareVariable("d_fld%grid%gphiu", d_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreEndDeclaration
      CALL read_only_verify_psy_data%ProvideVariable("a_fld%grid%gphiu", a_fld%grid%gphiu)
      CALL read_only_verify_psy_data%ProvideVariable("b_fld%grid%gphiu", b_fld%grid%gphiu)
      CALL read_only_verify_psy_data%ProvideVariable("c_fld%grid%gphiu", c_fld%grid%gphiu)
      CALL read_only_verify_psy_data%ProvideVariable("d_fld%grid%gphiu", d_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PreEnd
      DO j=a_fld%whole%ystart,a_fld%whole%ystop
        DO i=a_fld%whole%xstart,a_fld%whole%xstop
          CALL init_field_code(i, j, a_fld%data, 1.0, a_fld%grid%gphiu)
        END DO
      END DO
      DO j=b_fld%whole%ystart,b_fld%whole%ystop
        DO i=b_fld%whole%xstart,b_fld%whole%xstop
          CALL init_field_code(i, j, b_fld%data, 2.0, b_fld%grid%gphiu)
        END DO
      END DO
      DO j=c_fld%whole%ystart,c_fld%whole%ystop
        DO i=c_fld%whole%xstart,c_fld%whole%xstop
          CALL init_field_code(i, j, c_fld%data, 3.0, c_fld%grid%gphiu)
        END DO
      END DO
      DO j=d_fld%whole%ystart,d_fld%whole%ystop
        DO i=d_fld%whole%xstart,d_fld%whole%xstop
          CALL init_field_code(i, j, d_fld%data, 4.0, d_fld%grid%gphiu)
        END DO
      END DO
      CALL read_only_verify_psy_data%PostStart
      CALL read_only_verify_psy_data%ProvideVariable("a_fld%grid%gphiu", a_fld%grid%gphiu)
      CALL read_only_verify_psy_data%ProvideVariable("b_fld%grid%gphiu", b_fld%grid%gphiu)
      CALL read_only_verify_psy_data%ProvideVariable("c_fld%grid%gphiu", c_fld%grid%gphiu)
      CALL read_only_verify_psy_data%ProvideVariable("d_fld%grid%gphiu", d_fld%grid%gphiu)
      CALL read_only_verify_psy_data%PostEnd
      !
      ! ReadOnlyVerifyEnd
      !
    END SUBROUTINE invoke_0
    SUBROUTINE invoke_1_update_field(a_fld, b_fld, c_fld, d_fld, x, y, z)
      USE update_field_mod, ONLY: update_field_code
      USE read_only_verify_psy_data_mod, ONLY: read_only_verify_PSyDataType
      TYPE(r2d_field), intent(inout) :: a_fld, b_fld, c_fld, d_fld
      REAL(KIND=go_wp), intent(inout) :: x, y, z
      INTEGER j
      INTEGER i
      TYPE(read_only_verify_PSyDataType), target, save :: read_only_verify_psy_data
      !
      ! ReadOnlyVerifyStart
      !
      CALL read_only_verify_psy_data%PreStart("main", "update", 5, 5)
      CALL read_only_verify_psy_data%PreDeclareVariable("b_fld", b_fld)
      CALL read_only_verify_psy_data%PreDeclareVariable("c_fld", c_fld)
      CALL read_only_verify_psy_data%PreDeclareVariable("d_fld", d_fld)
      CALL read_only_verify_psy_data%PreDeclareVariable("z", z)
      CALL read_only_verify_psy_data%PreDeclareVariable("b_fld%grid%dx", b_fld%grid%dx)
      CALL read_only_verify_psy_data%PreDeclareVariable("b_fld", b_fld)
      CALL read_only_verify_psy_data%PreDeclareVariable("c_fld", c_fld)
      CALL read_only_verify_psy_data%PreDeclareVariable("d_fld", d_fld)
      CALL read_only_verify_psy_data%PreDeclareVariable("z", z)
      CALL read_only_verify_psy_data%PreDeclareVariable("b_fld%grid%dx", b_fld%grid%dx)
      CALL read_only_verify_psy_data%PreEndDeclaration
      CALL read_only_verify_psy_data%ProvideVariable("b_fld", b_fld)
      CALL read_only_verify_psy_data%ProvideVariable("c_fld", c_fld)
      CALL read_only_verify_psy_data%ProvideVariable("d_fld", d_fld)
      CALL read_only_verify_psy_data%ProvideVariable("z", z)
      CALL read_only_verify_psy_data%ProvideVariable("b_fld%grid%dx", b_fld%grid%dx)
      CALL read_only_verify_psy_data%PreEnd
      DO j=a_fld%whole%ystart,a_fld%whole%ystop
        DO i=a_fld%whole%xstart,a_fld%whole%xstop
          CALL update_field_code(i, j, a_fld%data, b_fld%data, c_fld%data, d_fld%data, x, y, z, b_fld%grid%dx)
        END DO
      END DO
      CALL read_only_verify_psy_data%PostStart
      CALL read_only_verify_psy_data%ProvideVariable("b_fld", b_fld)
      CALL read_only_verify_psy_data%ProvideVariable("c_fld", c_fld)
      CALL read_only_verify_psy_data%ProvideVariable("d_fld", d_fld)
      CALL read_only_verify_psy_data%ProvideVariable("z", z)
      CALL read_only_verify_psy_data%ProvideVariable("b_fld%grid%dx", b_fld%grid%dx)
      CALL read_only_verify_psy_data%PostEnd
      !
      ! ReadOnlyVerifyEnd
      !
    END SUBROUTINE invoke_1_update_field
  END MODULE psy_test