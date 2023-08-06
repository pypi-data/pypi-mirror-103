__attribute__((reqd_work_group_size(4, 1, 1)))
__kernel void compute_h_code(
  __global double * restrict h,
  __global double * restrict p,
  __global double * restrict u,
  __global double * restrict v,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  int hLEN1 = get_global_size(0);
  int hLEN2 = get_global_size(1);
  int pLEN1 = get_global_size(0);
  int pLEN2 = get_global_size(1);
  int uLEN1 = get_global_size(0);
  int uLEN2 = get_global_size(1);
  int vLEN1 = get_global_size(0);
  int vLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((!(((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop))))) {
    h[j * hLEN1 + i] = (p[j * pLEN1 + i] + (0.25e0 * ((((u[j * uLEN1 + (i + 1)] * u[j * uLEN1 + (i + 1)]) + (u[j * uLEN1 + i] * u[j * uLEN1 + i])) + (v[(j + 1) * vLEN1 + i] * v[(j + 1) * vLEN1 + i])) + (v[j * vLEN1 + i] * v[j * vLEN1 + i]))));
  }
}

