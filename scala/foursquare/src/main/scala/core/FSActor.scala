package core

import akka.actor.Actor

class FSActor extends Actor {
  def receive: Receive = {
    case t: String => println (t)
  }
}
