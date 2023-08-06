__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void compute_pnew_code(
  __global double * restrict pnew,
  __global double * restrict pold,
  __global double * restrict cu,
  __global double * restrict cv,
  double tdt,
  double dx,
  double dy,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  double tdtsdx;
  double tdtsdy;
  int pnewLEN1 = get_global_size(0);
  int pnewLEN2 = get_global_size(1);
  int poldLEN1 = get_global_size(0);
  int poldLEN2 = get_global_size(1);
  int cuLEN1 = get_global_size(0);
  int cuLEN2 = get_global_size(1);
  int cvLEN1 = get_global_size(0);
  int cvLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  tdtsdx = (tdt / dx);
  tdtsdy = (tdt / dy);
  pnew[j * pnewLEN1 + i] = ((pold[j * poldLEN1 + i] - (tdtsdx * (cu[j * cuLEN1 + (i + 1)] - cu[j * cuLEN1 + i]))) - (tdtsdy * (cv[(j + 1) * cvLEN1 + i] - cv[j * cvLEN1 + i])));
}

