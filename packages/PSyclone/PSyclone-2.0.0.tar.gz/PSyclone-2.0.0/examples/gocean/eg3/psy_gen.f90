  MODULE psy_simple
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE compute_cu_code_set_args(kernel_obj, cu_fld, p_fld, u_fld, xstart, xstop, ystart, ystop)
      USE clfortran, ONLY: clSetKernelArg
      USE iso_c_binding, ONLY: c_sizeof, c_loc, c_intptr_t
      USE ocl_utils_mod, ONLY: check_status
      INTEGER(KIND=c_intptr_t), intent(in), target :: cu_fld, p_fld, u_fld
      INTEGER, intent(in), target :: xstart, xstop, ystart, ystop
      INTEGER ierr
      INTEGER(KIND=c_intptr_t), target :: kernel_obj
      ! Set the arguments for the compute_cu_code OpenCL Kernel
      ierr = clSetKernelArg(kernel_obj, 0, C_SIZEOF(cu_fld), C_LOC(cu_fld))
      CALL check_status('clSetKernelArg: arg 0 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 1, C_SIZEOF(p_fld), C_LOC(p_fld))
      CALL check_status('clSetKernelArg: arg 1 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 2, C_SIZEOF(u_fld), C_LOC(u_fld))
      CALL check_status('clSetKernelArg: arg 2 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 3, C_SIZEOF(xstart), C_LOC(xstart))
      CALL check_status('clSetKernelArg: arg 3 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 4, C_SIZEOF(xstop), C_LOC(xstop))
      CALL check_status('clSetKernelArg: arg 4 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 5, C_SIZEOF(ystart), C_LOC(ystart))
      CALL check_status('clSetKernelArg: arg 5 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 6, C_SIZEOF(ystop), C_LOC(ystop))
      CALL check_status('clSetKernelArg: arg 6 of compute_cu_code', ierr)
    END SUBROUTINE compute_cu_code_set_args
    SUBROUTINE compute_cv_code_set_args(kernel_obj, cv_fld, p_fld, v_fld, xstart_1, xstop_1, ystart_1, ystop_1)
      USE clfortran, ONLY: clSetKernelArg
      USE iso_c_binding, ONLY: c_sizeof, c_loc, c_intptr_t
      USE ocl_utils_mod, ONLY: check_status
      INTEGER(KIND=c_intptr_t), intent(in), target :: cv_fld, p_fld, v_fld
      INTEGER, intent(in), target :: xstart_1, xstop_1, ystart_1, ystop_1
      INTEGER ierr
      INTEGER(KIND=c_intptr_t), target :: kernel_obj
      ! Set the arguments for the compute_cv_code OpenCL Kernel
      ierr = clSetKernelArg(kernel_obj, 0, C_SIZEOF(cv_fld), C_LOC(cv_fld))
      CALL check_status('clSetKernelArg: arg 0 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 1, C_SIZEOF(p_fld), C_LOC(p_fld))
      CALL check_status('clSetKernelArg: arg 1 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 2, C_SIZEOF(v_fld), C_LOC(v_fld))
      CALL check_status('clSetKernelArg: arg 2 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 3, C_SIZEOF(xstart_1), C_LOC(xstart_1))
      CALL check_status('clSetKernelArg: arg 3 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 4, C_SIZEOF(xstop_1), C_LOC(xstop_1))
      CALL check_status('clSetKernelArg: arg 4 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 5, C_SIZEOF(ystart_1), C_LOC(ystart_1))
      CALL check_status('clSetKernelArg: arg 5 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 6, C_SIZEOF(ystop_1), C_LOC(ystop_1))
      CALL check_status('clSetKernelArg: arg 6 of compute_cv_code', ierr)
    END SUBROUTINE compute_cv_code_set_args
    SUBROUTINE compute_z_code_set_args(kernel_obj, z_fld, p_fld, u_fld, v_fld, dx, dy, xstart_2, xstop_2, ystart_2, ystop_2)
      USE clfortran, ONLY: clSetKernelArg
      USE iso_c_binding, ONLY: c_sizeof, c_loc, c_intptr_t
      USE ocl_utils_mod, ONLY: check_status
      INTEGER(KIND=c_intptr_t), intent(in), target :: z_fld, p_fld, u_fld, v_fld
      REAL(KIND=go_wp), intent(in), target :: dx, dy
      INTEGER, intent(in), target :: xstart_2, xstop_2, ystart_2, ystop_2
      INTEGER ierr
      INTEGER(KIND=c_intptr_t), target :: kernel_obj
      ! Set the arguments for the compute_z_code OpenCL Kernel
      ierr = clSetKernelArg(kernel_obj, 0, C_SIZEOF(z_fld), C_LOC(z_fld))
      CALL check_status('clSetKernelArg: arg 0 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 1, C_SIZEOF(p_fld), C_LOC(p_fld))
      CALL check_status('clSetKernelArg: arg 1 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 2, C_SIZEOF(u_fld), C_LOC(u_fld))
      CALL check_status('clSetKernelArg: arg 2 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 3, C_SIZEOF(v_fld), C_LOC(v_fld))
      CALL check_status('clSetKernelArg: arg 3 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 4, C_SIZEOF(dx), C_LOC(dx))
      CALL check_status('clSetKernelArg: arg 4 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 5, C_SIZEOF(dy), C_LOC(dy))
      CALL check_status('clSetKernelArg: arg 5 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 6, C_SIZEOF(xstart_2), C_LOC(xstart_2))
      CALL check_status('clSetKernelArg: arg 6 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 7, C_SIZEOF(xstop_2), C_LOC(xstop_2))
      CALL check_status('clSetKernelArg: arg 7 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 8, C_SIZEOF(ystart_2), C_LOC(ystart_2))
      CALL check_status('clSetKernelArg: arg 8 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 9, C_SIZEOF(ystop_2), C_LOC(ystop_2))
      CALL check_status('clSetKernelArg: arg 9 of compute_z_code', ierr)
    END SUBROUTINE compute_z_code_set_args
    SUBROUTINE compute_h_code_set_args(kernel_obj, h_fld, p_fld, u_fld, v_fld, xstart_3, xstop_3, ystart_3, ystop_3)
      USE clfortran, ONLY: clSetKernelArg
      USE iso_c_binding, ONLY: c_sizeof, c_loc, c_intptr_t
      USE ocl_utils_mod, ONLY: check_status
      INTEGER(KIND=c_intptr_t), intent(in), target :: h_fld, p_fld, u_fld, v_fld
      INTEGER, intent(in), target :: xstart_3, xstop_3, ystart_3, ystop_3
      INTEGER ierr
      INTEGER(KIND=c_intptr_t), target :: kernel_obj
      ! Set the arguments for the compute_h_code OpenCL Kernel
      ierr = clSetKernelArg(kernel_obj, 0, C_SIZEOF(h_fld), C_LOC(h_fld))
      CALL check_status('clSetKernelArg: arg 0 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 1, C_SIZEOF(p_fld), C_LOC(p_fld))
      CALL check_status('clSetKernelArg: arg 1 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 2, C_SIZEOF(u_fld), C_LOC(u_fld))
      CALL check_status('clSetKernelArg: arg 2 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 3, C_SIZEOF(v_fld), C_LOC(v_fld))
      CALL check_status('clSetKernelArg: arg 3 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 4, C_SIZEOF(xstart_3), C_LOC(xstart_3))
      CALL check_status('clSetKernelArg: arg 4 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 5, C_SIZEOF(xstop_3), C_LOC(xstop_3))
      CALL check_status('clSetKernelArg: arg 5 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 6, C_SIZEOF(ystart_3), C_LOC(ystart_3))
      CALL check_status('clSetKernelArg: arg 6 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 7, C_SIZEOF(ystop_3), C_LOC(ystop_3))
      CALL check_status('clSetKernelArg: arg 7 of compute_h_code', ierr)
    END SUBROUTINE compute_h_code_set_args
    SUBROUTINE invoke_0(cu_fld, p_fld, u_fld, cv_fld, v_fld, z_fld, h_fld)
      USE fortcl, ONLY: get_num_cmd_queues, get_cmd_queues, get_kernel_by_name
      USE clfortran
      USE iso_c_binding
      TYPE(r2d_field), intent(inout), target :: cu_fld, p_fld, u_fld, cv_fld, v_fld, z_fld, h_fld
      INTEGER xstart, xstop, ystart, ystop, xstart_1, xstop_1, ystart_1, ystop_1, xstart_2, xstop_2, ystart_2, ystop_2, xstart_3, &
&xstop_3, ystart_3, ystop_3
      INTEGER(KIND=c_size_t), target :: localsize_3(2)
      INTEGER(KIND=c_size_t), target :: globalsize_3(2)
      INTEGER(KIND=c_intptr_t) h_fld_cl_mem
      INTEGER(KIND=c_size_t), target :: localsize_2(2)
      INTEGER(KIND=c_size_t), target :: globalsize_2(2)
      INTEGER(KIND=c_intptr_t) z_fld_cl_mem
      INTEGER(KIND=c_size_t), target :: localsize_1(2)
      INTEGER(KIND=c_size_t), target :: globalsize_1(2)
      INTEGER(KIND=c_intptr_t) v_fld_cl_mem
      INTEGER(KIND=c_intptr_t) cv_fld_cl_mem
      INTEGER(KIND=c_size_t), target :: localsize(2)
      INTEGER(KIND=c_size_t), target :: globalsize(2)
      INTEGER(KIND=c_intptr_t) u_fld_cl_mem
      INTEGER(KIND=c_intptr_t) p_fld_cl_mem
      INTEGER(KIND=c_intptr_t) cu_fld_cl_mem
      INTEGER(KIND=c_intptr_t), target, save :: kernel_compute_h_code
      INTEGER(KIND=c_intptr_t), target, save :: kernel_compute_z_code
      INTEGER(KIND=c_intptr_t), target, save :: kernel_compute_cv_code
      INTEGER(KIND=c_intptr_t), target, save :: kernel_compute_cu_code
      LOGICAL, save :: first_time=.true.
      INTEGER ierr
      INTEGER(KIND=c_intptr_t), pointer, save :: cmd_queues(:)
      INTEGER, save :: num_cmd_queues
      IF (first_time) THEN
        first_time = .false.
        ! Ensure OpenCL run-time is initialised for this PSy-layer module
        CALL psy_init
        num_cmd_queues = get_num_cmd_queues()
        cmd_queues => get_cmd_queues()
        kernel_compute_cu_code = get_kernel_by_name("compute_cu_code")
        kernel_compute_cv_code = get_kernel_by_name("compute_cv_code")
        kernel_compute_z_code = get_kernel_by_name("compute_z_code")
        kernel_compute_h_code = get_kernel_by_name("compute_h_code")
        CALL initialise_device_buffer(cu_fld)
        CALL initialise_device_buffer(p_fld)
        CALL initialise_device_buffer(u_fld)
        xstart = cu_fld%internal%xstart
        xstop = cu_fld%internal%xstop
        ystart = cu_fld%internal%ystart
        ystop = cu_fld%internal%ystop
      cu_fld_cl_mem = TRANSFER(cu_fld%device_ptr, cu_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
        CALL compute_cu_code_set_args(kernel_compute_cu_code, cu_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, xstart - 1, xstop - 1, &
&ystart - 1, ystop - 1)
        CALL cu_fld%write_to_device()
        CALL p_fld%write_to_device()
        CALL u_fld%write_to_device()
        CALL initialise_device_buffer(cv_fld)
        CALL initialise_device_buffer(p_fld)
        CALL initialise_device_buffer(v_fld)
        xstart_1 = cv_fld%internal%xstart
        xstop_1 = cv_fld%internal%xstop
        ystart_1 = cv_fld%internal%ystart
        ystop_1 = cv_fld%internal%ystop
      cv_fld_cl_mem = TRANSFER(cv_fld%device_ptr, cv_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
        CALL compute_cv_code_set_args(kernel_compute_cv_code, cv_fld_cl_mem, p_fld_cl_mem, v_fld_cl_mem, xstart_1 - 1, &
&xstop_1 - 1, ystart_1 - 1, ystop_1 - 1)
        CALL cv_fld%write_to_device()
        CALL p_fld%write_to_device()
        CALL v_fld%write_to_device()
        CALL initialise_device_buffer(z_fld)
        CALL initialise_device_buffer(p_fld)
        CALL initialise_device_buffer(u_fld)
        CALL initialise_device_buffer(v_fld)
        xstart_2 = z_fld%internal%xstart
        xstop_2 = z_fld%internal%xstop
        ystart_2 = z_fld%internal%ystart
        ystop_2 = z_fld%internal%ystop
      z_fld_cl_mem = TRANSFER(z_fld%device_ptr, z_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
        CALL compute_z_code_set_args(kernel_compute_z_code, z_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, v_fld_cl_mem, p_fld%grid%dx, &
&p_fld%grid%dy, xstart_2 - 1, xstop_2 - 1, ystart_2 - 1, ystop_2 - 1)
        CALL z_fld%write_to_device()
        CALL p_fld%write_to_device()
        CALL u_fld%write_to_device()
        CALL v_fld%write_to_device()
        CALL initialise_device_buffer(h_fld)
        CALL initialise_device_buffer(p_fld)
        CALL initialise_device_buffer(u_fld)
        CALL initialise_device_buffer(v_fld)
        xstart_3 = h_fld%internal%xstart
        xstop_3 = h_fld%internal%xstop
        ystart_3 = h_fld%internal%ystart
        ystop_3 = h_fld%internal%ystop
      h_fld_cl_mem = TRANSFER(h_fld%device_ptr, h_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
        CALL compute_h_code_set_args(kernel_compute_h_code, h_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, v_fld_cl_mem, xstart_3 - 1, &
&xstop_3 - 1, ystart_3 - 1, ystop_3 - 1)
        CALL h_fld%write_to_device()
        CALL p_fld%write_to_device()
        CALL u_fld%write_to_device()
        CALL v_fld%write_to_device()
      END IF
        xstart = cu_fld%internal%xstart
        xstop = cu_fld%internal%xstop
        ystart = cu_fld%internal%ystart
        ystop = cu_fld%internal%ystop
      cu_fld_cl_mem = TRANSFER(cu_fld%device_ptr, cu_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
      CALL compute_cu_code_set_args(kernel_compute_cu_code, cu_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, xstart - 1, xstop - 1, &
&ystart - 1, ystop - 1)
      globalsize = (/p_fld%grid%nx, p_fld%grid%ny/)
      localsize = (/4, 1/)
      ! Launch the kernel
      ierr = clEnqueueNDRangeKernel(cmd_queues(1), kernel_compute_cu_code, 2, C_NULL_PTR, C_LOC(globalsize), C_LOC(localsize), 0, &
&C_NULL_PTR, C_NULL_PTR)
      !
        xstart_1 = cv_fld%internal%xstart
        xstop_1 = cv_fld%internal%xstop
        ystart_1 = cv_fld%internal%ystart
        ystop_1 = cv_fld%internal%ystop
      cv_fld_cl_mem = TRANSFER(cv_fld%device_ptr, cv_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
      CALL compute_cv_code_set_args(kernel_compute_cv_code, cv_fld_cl_mem, p_fld_cl_mem, v_fld_cl_mem, xstart_1 - 1, xstop_1 - 1, &
&ystart_1 - 1, ystop_1 - 1)
      globalsize_1 = (/p_fld%grid%nx, p_fld%grid%ny/)
      localsize_1 = (/4, 1/)
      ! Launch the kernel
      ierr = clEnqueueNDRangeKernel(cmd_queues(1), kernel_compute_cv_code, 2, C_NULL_PTR, C_LOC(globalsize_1), C_LOC(localsize_1), &
&0, C_NULL_PTR, C_NULL_PTR)
      !
        xstart_2 = z_fld%internal%xstart
        xstop_2 = z_fld%internal%xstop
        ystart_2 = z_fld%internal%ystart
        ystop_2 = z_fld%internal%ystop
      z_fld_cl_mem = TRANSFER(z_fld%device_ptr, z_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
      CALL compute_z_code_set_args(kernel_compute_z_code, z_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, v_fld_cl_mem, p_fld%grid%dx, &
&p_fld%grid%dy, xstart_2 - 1, xstop_2 - 1, ystart_2 - 1, ystop_2 - 1)
      globalsize_2 = (/p_fld%grid%nx, p_fld%grid%ny/)
      localsize_2 = (/4, 1/)
      ! Launch the kernel
      ierr = clEnqueueNDRangeKernel(cmd_queues(1), kernel_compute_z_code, 2, C_NULL_PTR, C_LOC(globalsize_2), C_LOC(localsize_2), &
&0, C_NULL_PTR, C_NULL_PTR)
      !
        xstart_3 = h_fld%internal%xstart
        xstop_3 = h_fld%internal%xstop
        ystart_3 = h_fld%internal%ystart
        ystop_3 = h_fld%internal%ystop
      h_fld_cl_mem = TRANSFER(h_fld%device_ptr, h_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
      CALL compute_h_code_set_args(kernel_compute_h_code, h_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, v_fld_cl_mem, xstart_3 - 1, &
&xstop_3 - 1, ystart_3 - 1, ystop_3 - 1)
      globalsize_3 = (/p_fld%grid%nx, p_fld%grid%ny/)
      localsize_3 = (/4, 1/)
      ! Launch the kernel
      ierr = clEnqueueNDRangeKernel(cmd_queues(1), kernel_compute_h_code, 2, C_NULL_PTR, C_LOC(globalsize_3), C_LOC(localsize_3), &
&0, C_NULL_PTR, C_NULL_PTR)
      !
      ! Block until all kernels have finished
      ierr = clFinish(cmd_queues(1))
    END SUBROUTINE invoke_0
    SUBROUTINE read_from_device(from, to, startx, starty, nx, ny, blocking)
      USE iso_c_binding, ONLY: c_intptr_t, c_ptr, c_size_t, c_sizeof
      USE ocl_utils_mod, ONLY: check_status
      USE kind_params_mod, ONLY: go_wp
      USE clfortran
      USE fortcl, ONLY: get_cmd_queues
      TYPE(c_ptr), intent(in) :: from
      REAL(KIND=go_wp), INTENT(INOUT), DIMENSION(:, :), TARGET :: to
      INTEGER, intent(in) :: startx
      INTEGER, intent(in) :: starty
      INTEGER, intent(in) :: nx
      INTEGER, intent(in) :: ny
      LOGICAL, intent(in) :: blocking
      INTEGER(KIND=c_size_t) size_in_bytes
      INTEGER(KIND=c_size_t) offset_in_bytes
      INTEGER(KIND=c_intptr_t) cl_mem
      INTEGER(KIND=c_intptr_t), POINTER :: cmd_queues(:)
      INTEGER ierr
      INTEGER i

      cl_mem = TRANSFER(from, cl_mem)
      cmd_queues => get_cmd_queues()
      IF (nx < SIZE(to, 1) / 2) THEN
        DO i = starty, starty + ny, 1
          size_in_bytes = INT(nx, 8) * c_sizeof(to(1,1))
          offset_in_bytes = INT(SIZE(to, 1) * (i - 1) + (startx - 1)) * c_sizeof(to(1,1))
          ierr = &
&clenqueuereadbuffer(cmd_queues(1),cl_mem,CL_FALSE,offset_in_bytes,size_in_bytes,c_loc(to(startx,i)),0,C_NULL_PTR,C_NULL_PTR)
          CALL check_status('"clEnqueueReadBuffer"', ierr)
        END DO
        IF (blocking) THEN
          CALL check_status('"clFinish on read"', clfinish(cmd_queues(1)))
        END IF
      ELSE
        size_in_bytes = INT(SIZE(to, 1) * ny, 8) * c_sizeof(to(1,1))
        offset_in_bytes = INT(SIZE(to, 1) * (starty - 1), 8) * c_sizeof(to(1,1))
        ierr = &
&clenqueuereadbuffer(cmd_queues(1),cl_mem,CL_TRUE,offset_in_bytes,size_in_bytes,c_loc(to(1,starty)),0,C_NULL_PTR,C_NULL_PTR)
        CALL check_status('"clEnqueueReadBuffer"', ierr)
      END IF

    END SUBROUTINE read_from_device
    SUBROUTINE write_to_device(from, to, startx, starty, nx, ny, blocking)
      USE iso_c_binding, ONLY: c_intptr_t, c_ptr, c_size_t, c_sizeof
      USE ocl_utils_mod, ONLY: check_status
      USE kind_params_mod, ONLY: go_wp
      USE clfortran
      USE fortcl, ONLY: get_cmd_queues
      REAL(KIND=go_wp), INTENT(IN), DIMENSION(:, :), TARGET :: from
      TYPE(c_ptr), intent(in) :: to
      INTEGER, intent(in) :: startx
      INTEGER, intent(in) :: starty
      INTEGER, intent(in) :: nx
      INTEGER, intent(in) :: ny
      LOGICAL, intent(in) :: blocking
      INTEGER(KIND=c_intptr_t) cl_mem
      INTEGER(KIND=c_size_t) size_in_bytes
      INTEGER(KIND=c_size_t) offset_in_bytes
      INTEGER(KIND=c_intptr_t), POINTER :: cmd_queues(:)
      INTEGER ierr
      INTEGER i

      cl_mem = TRANSFER(to, cl_mem)
      cmd_queues => get_cmd_queues()
      IF (nx < SIZE(from, 1) / 2) THEN
        DO i = starty, starty + ny, 1
          size_in_bytes = INT(nx, 8) * c_sizeof(from(1,1))
          offset_in_bytes = INT(SIZE(from, 1) * (i - 1) + (startx - 1)) * c_sizeof(from(1,1))
          ierr = &
&clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_FALSE,offset_in_bytes,size_in_bytes,c_loc(from(startx,i)),0,C_NULL_PTR,C_NULL_PTR)
          CALL check_status('"clEnqueueWriteBuffer"', ierr)
        END DO
        IF (blocking) THEN
          CALL check_status('"clFinish on write"', clfinish(cmd_queues(1)))
        END IF
      ELSE
        size_in_bytes = INT(SIZE(from, 1) * ny, 8) * c_sizeof(from(1,1))
        offset_in_bytes = INT(SIZE(from, 1) * (starty - 1)) * c_sizeof(from(1,1))
        ierr = &
&clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,offset_in_bytes,size_in_bytes,c_loc(from(1,starty)),0,C_NULL_PTR,C_NULL_PTR)
        CALL check_status('"clEnqueueWriteBuffer"', ierr)
      END IF

    END SUBROUTINE write_to_device
    SUBROUTINE initialise_device_buffer(field)
      USE fortcl, ONLY: create_rw_buffer
      USE field_mod
      TYPE(r2d_field), INTENT(INOUT), TARGET :: field
      INTEGER(KIND=c_size_t) size_in_bytes

      IF (.NOT.field%data_on_device) THEN
        size_in_bytes = INT(field%grid%nx * field%grid%ny, 8) * c_sizeof(field%data(1,1))
        field%device_ptr = TRANSFER(create_rw_buffer(size_in_bytes), field%device_ptr)
        field%data_on_device = .true.
        field%read_from_device_f => read_from_device
        field%write_to_device_f => write_to_device
      END IF

    END SUBROUTINE initialise_device_buffer
    SUBROUTINE psy_init()
      USE fortcl, ONLY: ocl_env_init, add_kernels
      CHARACTER(LEN=30) kernel_names(4)
      INTEGER :: ocl_device_num=1
      LOGICAL, save :: initialised=.False.
      ! Check to make sure we only execute this routine once
      IF (.not. initialised) THEN
        initialised = .True.
        ! Initialise the OpenCL environment/device
        CALL ocl_env_init(1, ocl_device_num, .False., .False.)
        ! The kernels this PSy layer module requires
        kernel_names(1) = "compute_cu_code"
        kernel_names(2) = "compute_cv_code"
        kernel_names(3) = "compute_z_code"
        kernel_names(4) = "compute_h_code"
        ! Create the OpenCL kernel objects. Expects to find all of the compiled
        ! kernels in FORTCL_KERNELS_FILE.
        CALL add_kernels(4, kernel_names)
      END IF
    END SUBROUTINE psy_init
  END MODULE psy_simple