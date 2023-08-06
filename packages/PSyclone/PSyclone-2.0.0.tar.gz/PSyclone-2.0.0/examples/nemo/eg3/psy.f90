PROGRAM tra_adv
  USE iso_c_binding, ONLY: C_INT64_T
  INTEGER, PARAMETER :: wp = 8
  REAL(KIND = wp), ALLOCATABLE, SAVE, DIMENSION(:, :, :, :) :: t3sn, t3ns, t3ew, t3we
  REAL(KIND = wp), ALLOCATABLE, SAVE, DIMENSION(:, :, :) :: tsn
  REAL(KIND = wp), ALLOCATABLE, SAVE, DIMENSION(:, :, :) :: pun, pvn, pwn
  REAL(KIND = wp), ALLOCATABLE, SAVE, DIMENSION(:, :, :) :: mydomain, zslpx, zslpy, zwx, zwy, umask, vmask, tmask, zind
  REAL(KIND = wp), ALLOCATABLE, SAVE, DIMENSION(:, :) :: ztfreez, rnfmsk, upsmsk
  REAL(KIND = wp), ALLOCATABLE, SAVE, DIMENSION(:) :: rnfmsk_z
  REAL(KIND = wp) :: zice, zu, z0u, zzwx, zv, z0v, zzwy, ztra, zbtr, zdt, zalpha
  REAL(KIND = wp) :: r
  REAL(KIND = wp) :: zw, z0w
  INTEGER :: jpi, jpj, jpk, ji, jj, jk, jt
  INTEGER(KIND = C_INT64_T) :: it
  CHARACTER(LEN = 10) :: env
  CALL get_environment_variable("JPI", env)
  READ(env, FMT = '(i10)') jpi
  CALL get_environment_variable("JPJ", env)
  READ(env, FMT = '(i10)') jpj
  CALL get_environment_variable("JPK", env)
  READ(env, FMT = '(i10)') jpk
  CALL get_environment_variable("IT", env)
  READ(env, FMT = '(i10)') it
  ALLOCATE(mydomain(jpi, jpj, jpk))
  ALLOCATE(zwx(jpi, jpj, jpk))
  ALLOCATE(zwy(jpi, jpj, jpk))
  ALLOCATE(zslpx(jpi, jpj, jpk))
  ALLOCATE(zslpy(jpi, jpj, jpk))
  ALLOCATE(pun(jpi, jpj, jpk))
  ALLOCATE(pvn(jpi, jpj, jpk))
  ALLOCATE(pwn(jpi, jpj, jpk))
  ALLOCATE(umask(jpi, jpj, jpk))
  ALLOCATE(vmask(jpi, jpj, jpk))
  ALLOCATE(tmask(jpi, jpj, jpk))
  ALLOCATE(zind(jpi, jpj, jpk))
  ALLOCATE(ztfreez(jpi, jpj))
  ALLOCATE(rnfmsk(jpi, jpj))
  ALLOCATE(upsmsk(jpi, jpj))
  ALLOCATE(rnfmsk_z(jpk))
  ALLOCATE(tsn(jpi, jpj, jpk))
  r = jpi * jpj * jpk
  DO jk = 1, jpk
    DO jj = 1, jpj
      DO ji = 1, jpi
        umask(ji, jj, jk) = ji * jj * jk / r
        mydomain(ji, jj, jk) = ji * jj * jk / r
        pun(ji, jj, jk) = ji * jj * jk / r
        pvn(ji, jj, jk) = ji * jj * jk / r
        pwn(ji, jj, jk) = ji * jj * jk / r
        vmask(ji, jj, jk) = ji * jj * jk / r
        tsn(ji, jj, jk) = ji * jj * jk / r
        tmask(ji, jj, jk) = ji * jj * jk / r
      END DO
    END DO
  END DO
  r = jpi * jpj
  DO jj = 1, jpj
    DO ji = 1, jpi
      ztfreez(ji, jj) = ji * jj / r
      upsmsk(ji, jj) = ji * jj / r
      rnfmsk(ji, jj) = ji * jj / r
    END DO
  END DO
  DO jk = 1, jpk
    rnfmsk_z(jk) = jk / jpk
  END DO
  DO jt = 1, it
    DO jk = 1, jpk
      DO jj = 1, jpj
        DO ji = 1, jpi
          IF (tsn(ji, jj, jk) <= ztfreez(ji, jj) + 0.1D0) THEN
            zice = 1.D0
          ELSE
            zice = 0.D0
          END IF
          zind(ji, jj, jk) = MAX(rnfmsk(ji, jj) * rnfmsk_z(jk), upsmsk(ji, jj), zice) * tmask(ji, jj, jk)
          zind(ji, jj, jk) = 1 - zind(ji, jj, jk)
        END DO
      END DO
    END DO
    !$ACC DATA COPYIN(pun,pvn,pwn,tmask,umask,vmask,zind) COPYOUT(zslpx,zslpy,zwx,zwy) COPY(mydomain)
    !$ACC KERNELS DEFAULT(PRESENT)
    zwx(:, :, jpk) = 0.E0
    zwy(:, :, jpk) = 0.E0
    DO jk = 1, jpk - 1
      DO jj = 1, jpj - 1
        DO ji = 1, jpi - 1
          zwx(ji, jj, jk) = umask(ji, jj, jk) * (mydomain(ji + 1, jj, jk) - mydomain(ji, jj, jk))
          zwy(ji, jj, jk) = vmask(ji, jj, jk) * (mydomain(ji, jj + 1, jk) - mydomain(ji, jj, jk))
        END DO
      END DO
    END DO
    zslpx(:, :, jpk) = 0.E0
    zslpy(:, :, jpk) = 0.E0
    DO jk = 1, jpk - 1
      DO jj = 2, jpj
        DO ji = 2, jpi
          zslpx(ji, jj, jk) = (zwx(ji, jj, jk) + zwx(ji - 1, jj, jk)) * (0.25D0 + SIGN(0.25D0, zwx(ji, jj, jk) * zwx(ji - 1, jj, &
&jk)))
          zslpy(ji, jj, jk) = (zwy(ji, jj, jk) + zwy(ji, jj - 1, jk)) * (0.25D0 + SIGN(0.25D0, zwy(ji, jj, jk) * zwy(ji, jj - 1, &
&jk)))
        END DO
      END DO
    END DO
    DO jk = 1, jpk - 1
      DO jj = 2, jpj
        DO ji = 2, jpi
          zslpx(ji, jj, jk) = SIGN(1.D0, zslpx(ji, jj, jk)) * MIN(ABS(zslpx(ji, jj, jk)), 2.D0 * ABS(zwx(ji - 1, jj, jk)), 2.D0 * &
&ABS(zwx(ji, jj, jk)))
          zslpy(ji, jj, jk) = SIGN(1.D0, zslpy(ji, jj, jk)) * MIN(ABS(zslpy(ji, jj, jk)), 2.D0 * ABS(zwy(ji, jj - 1, jk)), 2.D0 * &
&ABS(zwy(ji, jj, jk)))
        END DO
      END DO
    END DO
    DO jk = 1, jpk - 1
      zdt = 1
      DO jj = 2, jpj - 1
        DO ji = 2, jpi - 1
          z0u = SIGN(0.5D0, pun(ji, jj, jk))
          zalpha = 0.5D0 - z0u
          zu = z0u - 0.5D0 * pun(ji, jj, jk) * zdt
          zzwx = mydomain(ji + 1, jj, jk) + zind(ji, jj, jk) * (zu * zslpx(ji + 1, jj, jk))
          zzwy = mydomain(ji, jj, jk) + zind(ji, jj, jk) * (zu * zslpx(ji, jj, jk))
          zwx(ji, jj, jk) = pun(ji, jj, jk) * (zalpha * zzwx + (1. - zalpha) * zzwy)
          z0v = SIGN(0.5D0, pvn(ji, jj, jk))
          zalpha = 0.5D0 - z0v
          zv = z0v - 0.5D0 * pvn(ji, jj, jk) * zdt
          zzwx = mydomain(ji, jj + 1, jk) + zind(ji, jj, jk) * (zv * zslpy(ji, jj + 1, jk))
          zzwy = mydomain(ji, jj, jk) + zind(ji, jj, jk) * (zv * zslpy(ji, jj, jk))
          zwy(ji, jj, jk) = pvn(ji, jj, jk) * (zalpha * zzwx + (1.D0 - zalpha) * zzwy)
        END DO
      END DO
    END DO
    DO jk = 1, jpk - 1
      DO jj = 2, jpj - 1
        DO ji = 2, jpi - 1
          zbtr = 1.
          ztra = - zbtr * (zwx(ji, jj, jk) - zwx(ji - 1, jj, jk) + zwy(ji, jj, jk) - zwy(ji, jj - 1, jk))
          mydomain(ji, jj, jk) = mydomain(ji, jj, jk) + ztra
        END DO
      END DO
    END DO
    zwx(:, :, 1) = 0.E0
    zwx(:, :, jpk) = 0.E0
    DO jk = 2, jpk - 1
      zwx(:, :, jk) = tmask(:, :, jk) * (mydomain(:, :, jk - 1) - mydomain(:, :, jk))
    END DO
    zslpx(:, :, 1) = 0.E0
    DO jk = 2, jpk - 1
      DO jj = 1, jpj
        DO ji = 1, jpi
          zslpx(ji, jj, jk) = (zwx(ji, jj, jk) + zwx(ji, jj, jk + 1)) * (0.25D0 + SIGN(0.25D0, zwx(ji, jj, jk) * zwx(ji, jj, jk + &
&1)))
        END DO
      END DO
    END DO
    DO jk = 2, jpk - 1
      DO jj = 1, jpj
        DO ji = 1, jpi
          zslpx(ji, jj, jk) = SIGN(1.D0, zslpx(ji, jj, jk)) * MIN(ABS(zslpx(ji, jj, jk)), 2.D0 * ABS(zwx(ji, jj, jk + 1)), 2.D0 * &
&ABS(zwx(ji, jj, jk)))
        END DO
      END DO
    END DO
    zwx(:, :, 1) = pwn(:, :, 1) * mydomain(:, :, 1)
    zdt = 1
    zbtr = 1.
    DO jk = 1, jpk - 1
      DO jj = 2, jpj - 1
        DO ji = 2, jpi - 1
          z0w = SIGN(0.5D0, pwn(ji, jj, jk + 1))
          zalpha = 0.5D0 + z0w
          zw = z0w - 0.5D0 * pwn(ji, jj, jk + 1) * zdt * zbtr
          zzwx = mydomain(ji, jj, jk + 1) + zind(ji, jj, jk) * (zw * zslpx(ji, jj, jk + 1))
          zzwy = mydomain(ji, jj, jk) + zind(ji, jj, jk) * (zw * zslpx(ji, jj, jk))
          zwx(ji, jj, jk + 1) = pwn(ji, jj, jk + 1) * (zalpha * zzwx + (1. - zalpha) * zzwy)
        END DO
      END DO
    END DO
    zbtr = 1.
    DO jk = 1, jpk - 1
      DO jj = 2, jpj - 1
        DO ji = 2, jpi - 1
          ztra = - zbtr * (zwx(ji, jj, jk) - zwx(ji, jj, jk + 1))
          mydomain(ji, jj, jk) = ztra
        END DO
      END DO
    END DO
    !$ACC END KERNELS
    !$ACC END DATA
  END DO
  OPEN(UNIT = 4, FILE = 'output.dat', FORM = 'formatted')
  DO jk = 1, jpk - 1
    DO jj = 2, jpj - 1
      DO ji = 2, jpi - 1
        WRITE(4, FMT = *) mydomain(ji, jj, jk)
      END DO
    END DO
  END DO
  CLOSE(UNIT = 4)
  DEALLOCATE(mydomain)
  DEALLOCATE(zwx)
  DEALLOCATE(zwy)
  DEALLOCATE(zslpx)
  DEALLOCATE(zslpy)
  DEALLOCATE(pun)
  DEALLOCATE(pvn)
  DEALLOCATE(pwn)
  DEALLOCATE(umask)
  DEALLOCATE(vmask)
  DEALLOCATE(tmask)
  DEALLOCATE(zind)
  DEALLOCATE(ztfreez)
  DEALLOCATE(rnfmsk)
  DEALLOCATE(upsmsk)
  DEALLOCATE(rnfmsk_z)
  DEALLOCATE(tsn)
END PROGRAM tra_adv