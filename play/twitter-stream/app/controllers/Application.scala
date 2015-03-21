package controllers

import play.api.libs.iteratee._
import play.api.libs.json._
import play.extras.iteratees._
import play.api.libs.oauth._
import play.api._
import play.api.libs.ws.WS
import play.api.mvc._
import play.api.Play.current
import scala.concurrent.ExecutionContext.Implicits.global

import scala.concurrent.Future

object Application extends Controller {

  def index = Action {
    Ok(views.html.index("Your new application is ready."))
  }

  def credentials: Option[(ConsumerKey, RequestToken)] = {
    for {
      apiKey <- Play.configuration.getString("twitter.apiKey")
      apiSecret <- Play.configuration.getString("twitter.apiSecret")
      token <- Play.configuration.getString("twitter.token")
      tokenSecret <- Play.configuration.getString("twitter.tokenSecret")
    } yield (
      ConsumerKey(apiKey, apiSecret),
      RequestToken(token, tokenSecret)
      )
  }

  def tweets = Action.async {
    credentials.map {
      case (consumerKey: ConsumerKey, requestToken: RequestToken) => {
        val (iteratee, enumerator) = Concurrent.joined[Array[Byte]]

        val jsonStream: Enumerator[JsValue] =
          enumerator &>
          Encoding.decode() &>
          Enumeratee.grouped(JsonIteratees.jsSimpleObject)

        val loggingIteratee = Iteratee.foreach[JsObject] { value =>
          Logger.info(value.toString)
        }
        // jsonStream run loggingIteratee

        WS
          .url("https://stream.twitter.com/1.1/statuses/filter.json")
          .sign(OAuthCalculator(consumerKey, requestToken))
          .withQueryString("track" -> "box")
          .get { response =>
            Logger.info("Status: " + response.status)
            loggingIteratee
          }.map { response =>
            Ok("Stream closed")
          }
      }
    } getOrElse {
      Future { InternalServerError("Twitter credentials missing") }
    }
  }
}