subroutine scaling(num, arr, nx, ny, nz)
  integer, intent(in) :: num
  integer, intent(in) :: nx
  integer, intent(in) :: ny
  integer, intent(in) :: nz
  real(4), intent(inout) :: arr(nx,ny,nz)
  integer i

  do k = 1, nz
  do j = 1, ny
  do i = 1, nx
     arr(i,j,k) = arr(i,j,k) * num;
  enddo
  enddo
  enddo
end subroutine
