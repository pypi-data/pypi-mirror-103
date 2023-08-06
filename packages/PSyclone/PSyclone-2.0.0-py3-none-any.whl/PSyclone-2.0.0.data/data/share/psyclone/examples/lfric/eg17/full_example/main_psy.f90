  MODULE main_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_initialise_fields(field1, field2)
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER df
      TYPE(field_proxy_type) field1_proxy, field2_proxy
      !
      ! Initialise field and/or operator proxies
      !
      field1_proxy = field1%get_proxy()
      field2_proxy = field2%get_proxy()
      !
      ! Call kernels and communication routines
      !
      DO df=1,field1_proxy%vspace%get_last_dof_owned()
        field1_proxy%data(df) = 0.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field1_proxy%set_dirty()
      !
      DO df=1,field2_proxy%vspace%get_last_dof_owned()
        field2_proxy%data(df) = 1.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field2_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_initialise_fields
    SUBROUTINE invoke_testkern_w0(field1, field2)
      USE testkern_w0_kernel_mod, ONLY: testkern_w0_code
      USE mesh_mod, ONLY: mesh_type
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER(KIND=i_def) cell
      INTEGER(KIND=i_def) nlayers
      TYPE(field_proxy_type) field1_proxy, field2_proxy
      INTEGER(KIND=i_def), pointer :: map_w0(:,:) => null()
      INTEGER(KIND=i_def) ndf_w0, undf_w0
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      field1_proxy = field1%get_proxy()
      field2_proxy = field2%get_proxy()
      !
      ! Initialise number of layers
      !
      nlayers = field1_proxy%vspace%get_nlayers()
      !
      ! Create a mesh object
      !
      mesh => field1_proxy%vspace%get_mesh()
      !
      ! Look-up dofmaps for each function space
      !
      map_w0 => field1_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for w0
      !
      ndf_w0 = field1_proxy%vspace%get_ndf()
      undf_w0 = field1_proxy%vspace%get_undf()
      !
      ! Call kernels and communication routines
      !
      IF (field1_proxy%is_dirty(depth=1)) THEN
        CALL field1_proxy%halo_exchange(depth=1)
      END IF
      !
      IF (field2_proxy%is_dirty(depth=1)) THEN
        CALL field2_proxy%halo_exchange(depth=1)
      END IF
      !
      DO cell=1,mesh%get_last_halo_cell(1)
        !
        CALL testkern_w0_code(nlayers, field1_proxy%data, field2_proxy%data, ndf_w0, undf_w0, map_w0(:,cell))
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL field1_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_testkern_w0
  END MODULE main_psy