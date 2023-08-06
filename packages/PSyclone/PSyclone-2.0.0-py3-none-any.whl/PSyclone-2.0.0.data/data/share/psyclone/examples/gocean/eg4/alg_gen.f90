PROGRAM alg
  USE psy_alg, ONLY: invoke_0_kern_use_var
  USE field_mod, ONLY: r2d_field
  USE kern_use_var_mod, ONLY: kern_use_var
  IMPLICIT NONE
  TYPE(r2d_field) :: fld1
  CALL invoke_0_kern_use_var(fld1)
END PROGRAM alg