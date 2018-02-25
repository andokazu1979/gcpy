subroutine scaling(num, arr, nx, ny, nz, nt)
  integer, intent(in) :: num
  integer, intent(in) :: nx
  integer, intent(in) :: ny
  integer, intent(in) :: nz
  integer, intent(in) :: nt
  real(4), intent(inout) :: arr(nx,ny,nz,nt)
  integer i,j,k,t

  do t = 1, nt
  do k = 1, nz
  do j = 1, ny
  do i = 1, nx
     arr(i,j,k,t) = arr(i,j,k,t) * num;
  enddo
  enddo
  enddo
  enddo
end subroutine
