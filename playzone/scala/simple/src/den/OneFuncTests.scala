package den

object OneFuncTests {
  def gcd(num1 : Int, num2 : Int) : Int = {
    if (num2 == 0) {
      num1
    } else {
      gcd(num2, num1 % num2)
    }
  }
}
