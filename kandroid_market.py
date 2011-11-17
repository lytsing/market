import os
import httplib, urllib
import market_pb2
import base64
import sys
import StringIO
import gzip
from google.protobuf import text_format

class Auth(object):
 
 def __init__(self,param="null"):
	self.param = param

 def __get__(self, instance, owner):
	if os.path.isfile("/home/deli/api/auth.token"):
		f = open("/home/deli/api/auth.token", "rb")
		authToken = f.read()
		f.close()
	else:
		loginform_fields = {
			"Email":"your_name@gmail.com",
			"Passwd":"your_passwod",
			"service":"android",
			"accountType":"HOSTED_OR_GOOGLE" }

		loginform_data = urllib.urlencode(loginform_fields)

		login_headers = {"Content-type": "application/x-www-form-urlencoded"}
		conn = httplib.HTTPSConnection("www.google.com")
		conn.request("POST", "/accounts/ClientLogin", loginform_data, login_headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()

		retValues = data.split()
		for retValue in retValues:
			(key,value) = retValue.split('=')
			if key == "Auth":
				authToken = value
		f = open("/home/deli/api/auth.token", "wb")
		f.write(authToken)
		f.close()
	return authToken


class Session(object):
	authToken = Auth()

class Request(object):

 def __init__(self,param):
   self.req = param
   self.authToken = Session().authToken
   request = market_pb2.Request()
   requestContext = request.context
   requestContext.authSubToken = self.authToken
   requestContext.unknown1 = 0
   requestContext.version = 1002
   requestContext.deviceId = "0000000000000000"
#  requestContext.deviceId = "4205715879096915934"
   requestContext.deviceAndSdkVersion = "sapphire:8"
   requestContext.userLanguage = "zh"
   requestContext.userCountry = "cn"
   requestContext.operatorAlpha = "T-Mobile USA"
   requestContext.simOperatorAlpha = "T-Mobile USA"
   requestContext.operatorNumeric = "310260"
   requestContext.simOperatorNumeric = "310260"


#   requestContext.operatorAlpha = "CMCC"
#   requestContext.simOperatorAlpha = "CMCC"
#   requestContext.operatorNumeric = "46000"
#   requestContext.simOperatorNumeric = "46000"

   self.request = request

 def executeHttpQuery(self):
   requestData = base64.encodestring(self.request.SerializeToString())

   market_headers = {
      "Cookie": "ANDROID=" + self.authToken,
      "User-Agent": "Android-Market/2 (sapphire PLAT-RC33); gzip",
      "Content-type": "application/x-www-form-urlencoded",
      "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.7",
      "Connection": "keep-alive"
   }

   marketform_data = "version=2&request=" + requestData

   conn = httplib.HTTPConnection("android.clients.google.com")
   conn.request("POST", "/market/api/ApiRequest", marketform_data, market_headers)

   response = conn.getresponse()

   if response.status == 200 :
      raw_data = response.read()
      stream = StringIO.StringIO(raw_data)
      decompressor = gzip.GzipFile(fileobj=stream)
      data = decompressor.read()	
   else :
      data = ""
	
   conn.close

   return data

 def appRequest(self, query, startIdx):

   class AppType:
      NONE = 0
      APPLICATION = 1
      RINGTONE = 2
      WALLPAPER = 3
      GAME = 4

   request = self.request
   requestGroup = request.requestgroup.add()

   requestGroup.appsRequest.appType = AppType.NONE
   requestGroup.appsRequest.query = unicode(query, "utf-8")
   requestGroup.appsRequest.withExtendedInfo = 1
   requestGroup.appsRequest.orderType = market_pb2.AppsRequest.POPULAR
   requestGroup.appsRequest.startIndex = (startIdx - 1) * 10
   requestGroup.appsRequest.entriesCount = 10
   requestGroup.appsRequest.viewType = market_pb2.AppsRequest.ALL

 def allAppRequest(self, startIdx, orderType, viewType):
   class AppType:
      NONE = 0
      APPLICATION = 1
      RINGTONE = 2
      WALLPAPER = 3
      GAME = 4

   request = self.request
   requestGroup = request.requestgroup.add()

   requestGroup.appsRequest.appType = AppType.APPLICATION
   requestGroup.appsRequest.startIndex = (startIdx - 1) * 10
   requestGroup.appsRequest.entriesCount = 10

   if viewType == "PAID":
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.PAID
   elif viewType == "FREE":
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.FREE
   else:
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.ALL

   if orderType == "POPULAR":
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.POPULAR
   elif orderType == "NEWEST":
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.NEWEST
   else:
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.NONE

 def allGameRequest(self, startIdx, orderType, viewType):
   class AppType:
      NONE = 0
      APPLICATION = 1
      RINGTONE = 2
      WALLPAPER = 3
      GAME = 4

   request = self.request
   requestGroup = request.requestgroup.add()

   requestGroup.appsRequest.appType = AppType.GAME
   requestGroup.appsRequest.startIndex = (startIdx - 1) * 10
   requestGroup.appsRequest.entriesCount = 10

   if viewType == "PAID":
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.PAID
   elif viewType == "FREE":
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.FREE
   else:
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.ALL

   if orderType == "POPULAR":
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.POPULAR
   elif orderType == "NEWEST":
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.NEWEST
   else:
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.NONE

 def featuredAppRequest(self, startIdx):

   class AppType:
      NONE = 0
      APPLICATION = 1
      RINGTONE = 2
      WALLPAPER = 3
      GAME = 4

   request = self.request
   requestGroup = request.requestgroup.add()

   requestGroup.appsRequest.withExtendedInfo = 1
   requestGroup.appsRequest.orderType = market_pb2.AppsRequest.FEATURED
   requestGroup.appsRequest.startIndex = (startIdx - 1) * 10
   requestGroup.appsRequest.entriesCount = 20
   requestGroup.appsRequest.viewType = market_pb2.AppsRequest.ALL

 def categoryAppRequest(self, categoryId, startIdx, orderType, viewType):

   class AppType:
      NONE = 0
      APPLICATION = 1
      RINGTONE = 2
      WALLPAPER = 3
      GAME = 4

   request = self.request
   requestGroup = request.requestgroup.add()

   requestGroup.appsRequest.categoryId = categoryId
   requestGroup.appsRequest.startIndex = (startIdx - 1) * 10
   requestGroup.appsRequest.entriesCount = 10
   if viewType == "PAID":
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.PAID
   elif viewType == "FREE":
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.FREE
   else:
      requestGroup.appsRequest.viewType = market_pb2.AppsRequest.ALL

   if orderType == "POPULAR":
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.POPULAR
   elif orderType == "NEWEST":
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.NEWEST
   else:
      requestGroup.appsRequest.orderType = market_pb2.AppsRequest.NONE

#   requestGroup.appsRequest.appType = AppType.NONE
#   requestGroup.appsRequest.appType = AppType.APPLICATION
#   requestGroup.appsRequest.appType = AppType.GAME
#   requestGroup.appsRequest.categoryId = categoryId


 def iconRequest(self, appId):

   request = self.request
   requestGroup = request.requestgroup.add()

   requestGroup.imageRequest.appId = appId
   requestGroup.imageRequest.imageUsage = requestGroup.imageRequest.ICON

 def assetRequest(self, appId):

   request = self.request
   requestGroup = request.requestgroup.add()

   requestGroup.appsRequest.appId = appId
   requestGroup.appsRequest.withExtendedInfo = 1

 def screenshotRequest(self, appId, id, thumbnail):

   request = self.request
   requestGroup = request.requestgroup.add()

   requestGroup.imageRequest.appId = appId
   if thumbnail == 1:
      requestGroup.imageRequest.imageUsage = requestGroup.imageRequest.SCREENSHOT_THUMBNAIL
   else :
      requestGroup.imageRequest.imageUsage = requestGroup.imageRequest.SCREENSHOT
   requestGroup.imageRequest.imageId = str(id)


 def categoryRequest(self, categoryId):

   request = self.request
   requestGroup = request.requestgroup.add()
 
   requestGroup.subCategoriesRequest.appType = categoryId

 def downloadRequest(self, appId, packageName):

   market_headers = {
        "Cookie": "ANDROID=" + Session().authToken,
        "User-Agent": "AndroidDownloadManager",
#       "Content-type": "application/x-www-form-urlencoded",
#       "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Connection": "keep-alive"
   }

   userId = "09236914634784898072"
   deviceId = "4119349832741326678"

   marketform_data = "?assetId=" + appId + "&userId=" + userId + "&deviceId=" + deviceId

   conn = httplib.HTTPConnection("android.clients.google.com")
   conn.request("GET", "/market/download/Download" + marketform_data, "", market_headers)

   response = conn.getresponse()
   if response.status != 200 :
       self.req.write("%d" % response.status)
       self.req.write("Sorry : Service unavailable")
   else :
       data = response.read()
       filename = "/home/deli/market/apk_download/" + packageName + ".apk"
       f = open(filename, "wb") 
       f.write(data) 
       f.close() 
       self.req.write("<meta http-equiv=\"refresh\" content=\"0;url=http://localhost/market/apk_download/%s.apk\">" % packageName)
   conn.close()

