package core

import com.ning.http.client.oauth.{RequestToken, ConsumerKey}

import scala.concurrent.Await
import scala.concurrent.duration._

//import akka.actor.{ActorSystem, Props}

object Main extends App {
  println("hi")
  //val system = ActorSystem()
  //val fsActor = system.actorOf(Props(new FSActor))
  //fsActor ! "xxx"

  import dispatch._, Defaults._

  val ck = new ConsumerKey("YOUR_CONSUMER_KEY", "YOUR_CONSUMER_TOKEN")

  private def buildReq(searchTerm: String, lat: Double, long: Double): Req = {
    val consumer = new ConsumerKey(consumerKey, consumerSecret)
    val requestToken = new RequestToken(token, tokenSecret)
    val req = url(searchUrl)
      .addQueryParameter("term", searchTerm)
      .addQueryParameter("radius_filter", "40000")
      .addQueryParameter("ll", s"$lat,$long")
    new SigningVerbs(req).sign(consumer, requestToken)
  }

  //val svc: Req = url("http://api.hostip.info/get_json.php?ip=12.215.42.19")
  val svc: Req = url("https://api.foursquare.com/v2/venues/search?client_id=EJ4FSWGQXEFLNBEWRLKN4L5M0NNJH3OVOU1ZFXSORP23BUOM&client_secret=E1V3FK3LBD3YUI3H5CDI4MFQCOVBAVBX1N00IBSP3F1EEJEJ&v=20130815&near='Campbell, CA'&query='restaurant'")
  val country: Future[String] = Http(svc OK as.String)

  //for (c <- country)
  val r: String = Await.result(country, 1500 millis)
  println(r)

  System.exit(0)
}
