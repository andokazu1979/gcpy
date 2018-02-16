subroutine scaling(num, arr, size_)
  integer, intent(in) :: num
  integer, intent(in) :: size_
  integer, intent(inout) :: arr(size_)
  integer i

  do i = 1, size_
     arr(i) = arr(i) * num;
  enddo
end subroutine
