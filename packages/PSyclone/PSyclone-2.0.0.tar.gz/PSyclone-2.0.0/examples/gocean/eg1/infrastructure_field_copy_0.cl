__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void field_copy_code(
  __global double * restrict output,
  __global double * restrict input
  ){
  int outputLEN1 = get_global_size(0);
  int outputLEN2 = get_global_size(1);
  int inputLEN1 = get_global_size(0);
  int inputLEN2 = get_global_size(1);
  int ji = get_global_id(0);
  int jj = get_global_id(1);
  output[jj * outputLEN1 + ji] = input[jj * inputLEN1 + ji];
}

