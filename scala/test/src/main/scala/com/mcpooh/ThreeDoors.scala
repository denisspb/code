package com.mcpooh

import scala.collection.mutable.ListBuffer

object ThreeDoors {
  def genArray: Array[Boolean] = {
    val z = Array(false, false, false)

    z(scala.util.Random.nextInt(z.size)) = true

    z
  }

  def openOne(except : Int, z : Array[Boolean]) : Int = {
    val list = new ListBuffer[Int]()

    for( i <- 0 to z.size - 1) {
      if ((except != i) && (!z(i))) {
        list += i
      }
    }

    if (list.size == 1) {
      list.head
    } else {
      if (scala.util.Random.nextInt(2) == 0)
        list.head
      else
        list.tail.head
    }
  }

  def main(args: Array[String]) {
    val verbose = false
    val attempts = 1000000

    var success = 0

    for( a <- 1 to attempts){
      val z = genArray
      if (verbose) print("[ " + z(0) + "." + z(1) + "." + z(2) + ", ")

      val first = scala.util.Random.nextInt(z.size)
      if (verbose) print(" first=" + z(first) + "(" + first + "), ")

      val open = openOne(first, z)
      if (verbose) print(" open=" + z(open) + "(" + open + "), ")

      val second = (0 + 1 + 2) - (first + open)
      if (verbose) print(" second=" + z(second) + "(" + second + "), ")

      if (verbose) println("]")

      if (z(second))
        success = success + 1
    }

    println("")
    println("")
    println("successful " + success + " of " + attempts)
  }
}
