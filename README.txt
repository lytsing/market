
Web-based Android Market Client

Original source from: http://www.kandroid.org/board/board.php?board=androidmarket&command=body&no=31

About PSP (Python Server Pages), please refer: http://modpython.org/live/current/doc-html/pyapi-psp.html

How to install:

1. http://code.google.com/p/protobuf/ After downloading, install it.

2. suppose that your web dir is /var/www/html/
$ grep deli *
$ for i in `grep "deli" * -l`; do sed -i 's/home\/deli/var\/www\/html/g' $i; done

3. Shell prompt to run as follows:
$ protoc --python_out=. market.proto
Results: market_pb2.py

4. market_pb2.py API created as a result of using the Android Market will create a client library.
    kandroid_market.py 
	- modify loginform_fields Password value to specify the value of the Email.
	- define downloadRequest in addition to specify the value of userId and deviceId.
	(To specify this value, check out the database table within the Android DownloadProvider 
		$ adb pull /data/data/com.android.providers.downloads/databases/downloads.db .
		$ sqlite3 downloads.db
		sqlite> .schema
		sqlite> select * from android_metadata;
	)

5. Run and specify the apk mimetype psp for the apache configuration

LoadModule python_module modules/mod_python.so

Alias /market "/home/deli/market"
<Directory /home/deli/market>
    AddHandler mod_python .psp .py
    PythonHandler mod_python.psp |.psp
    PythonHandler mod_python.publisher |.py
</Directory>

AddType application/vnd.android.package-archive .apk

6. Browse:
http://127.0.0.1/market/allAppItem.psp 

Note: The Android Market to cause an overload on the server, the used a Gmail account can be blocked.
Attention is required.

ChangeLog:
2010-10-19 Lytsing Huang (hlqing@gmail.com)
	* Translate Kerea to Chinese.
	* Fix asset.psp can't display Chinese code.
	* Make the web fit for w3c.
	* Add Google docs style theme

